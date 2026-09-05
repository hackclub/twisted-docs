#!/usr/bin/env python3
"""One-off migration: move locally-committed images out of content/ and into
Cloudflare R2, rewriting every markdown reference to the new public URL.

This repo currently has ~500 screenshots committed straight into content/ next
to the guides that use them. This script uploads each one to R2, rewrites the
markdown (![alt](path) and <img src="..."> references) to point at the public
R2 URL instead, and (optionally) deletes the now-unused local file.

Pass --backup to also copy every uploaded file into .imgbackups/ (mirroring
its R2 object key), so that in the rare case an image disappears from R2 there
is still a local copy to re-upload from. .imgbackups/ is gitignored — it's a
local safety net, not something meant to be committed.

Setup:
    pip install boto3

Required environment variables:
    R2_ENDPOINT    full S3-compatible endpoint, e.g. https://<ACCOUNT_ID>.r2.cloudflarestorage.com
    R2_ACCESS_KEY  R2 API token access key
    R2_SECRET_KEY  R2 API token secret key
    R2_BUCKET      e.g. hackclub-twisted
    R2_PUBLIC_URL  public base URL mapped to the bucket, e.g.
                   https://twisted.hackclub-assets.com/

(R2_TOKEN, if you have one, is a Cloudflare API token for Cloudflare's own API —
it's not used here. This script only talks to R2's S3-compatible API, which
authenticates with the access/secret key pair above.)

Usage:
    # Dry run: uploads to R2 and rewrites markdown, but leaves local files in place
    # so you can diff/verify before committing to deleting anything.
    python scripts/upload_images_to_r2.py

    # Also back up every uploaded file to .imgbackups/ before anything else happens.
    python scripts/upload_images_to_r2.py --backup

    # Back up, then delete each local image file once it's been uploaded,
    # backed up, and every markdown reference to it has been rewritten.
    python scripts/upload_images_to_r2.py --backup --delete

    # Preview without uploading or writing any files.
    python scripts/upload_images_to_r2.py --dry-run
"""

from __future__ import annotations

import argparse
import hashlib
import mimetypes
import os
import re
import shutil
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import unquote

CONTENT_DIR = Path("content")
BACKUP_DIR = Path(".imgbackups")
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
OBJECT_PREFIX = "docs/"

MARKDOWN_IMAGE_PATTERN = re.compile(r'(!\[[^\]]*\]\()([^)\s]+)((?:\s+"[^"]*")?\))')
HTML_IMG_PATTERN = re.compile(r'(<img\b[^>]*\bsrc=")([^"]+)(")', re.IGNORECASE)


def is_remote(path: str) -> bool:
    return path.startswith(("http://", "https://", "//", "data:"))


def find_local_images() -> list[Path]:
    return sorted(
        p for p in CONTENT_DIR.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_key_map(images: list[Path]) -> dict[Path, str]:
    """Map each local image file to its destination object key.

    Different guides sometimes reuse the exact same pasted screenshot (e.g.
    blinky and blinkyeda share several identical JLCPCB-ordering images under
    different filenames) — dedupe by content hash so those upload once, with
    every path that has that content pointed at the same key. Guides pointing
    at genuinely different files always get distinct keys, since the key is
    derived from that file's own path relative to content/ (unique by
    construction — R2/S3 keys support "/" nesting natively).
    """

    key_map: dict[Path, str] = {}
    key_by_hash: dict[str, str] = {}

    for path in images:
        digest = sha256_of(path)
        key = key_by_hash.get(digest)
        if key is None:
            relative = path.relative_to(CONTENT_DIR).as_posix().replace(" ", "-")
            key = OBJECT_PREFIX + relative
            key_by_hash[digest] = key
        key_map[path.resolve()] = key

    return key_map


def backup_file(path: Path, key: str) -> None:
    """Copy a local image into .imgbackups/, mirroring its R2 object key.

    .imgbackups/ ends up a 1:1 local mirror of the bucket, so recovering from
    an R2 outage is just re-running the upload with BACKUP_DIR swapped in for
    CONTENT_DIR and each file's key taken from its path relative to it.
    """

    destination = BACKUP_DIR / key
    if destination.exists():
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, destination)


def upload_one(client, bucket: str, path: Path, key: str, backup: bool) -> int:
    content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    client.upload_file(
        str(path),
        bucket,
        key,
        ExtraArgs={
            "ContentType": content_type,
            "CacheControl": "public, max-age=31536000, immutable",
        },
    )
    if backup:
        backup_file(path, key)
    return path.stat().st_size


def upload_all(client, bucket: str, key_map: dict[Path, str], workers: int = 5, backup: bool = False) -> None:
    # Several local paths can share the same key (deduped identical content) —
    # only upload each distinct key once, using whichever path we saw first.
    to_upload: dict[str, Path] = {}
    for path, key in key_map.items():
        if key in to_upload:
            print(f"  skipping {path} (identical to an already-uploaded file, s3://{bucket}/{key})")
            continue
        to_upload[key] = path

    total = len(to_upload)
    done = 0
    bytes_sent = 0
    start = time.monotonic()
    print_lock = threading.Lock()

    # boto3 clients are documented as thread-safe, so a single client can be
    # shared across worker threads uploading concurrently.
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(upload_one, client, bucket, path, key, backup): (path, key)
            for key, path in to_upload.items()
        }

        for future in as_completed(futures):
            path, key = futures[future]
            size = future.result()

            with print_lock:
                done += 1
                bytes_sent += size
                elapsed = time.monotonic() - start
                mbps = (bytes_sent * 8) / elapsed / 1_000_000 if elapsed > 0 else 0.0
                print(
                    f"  [{done}/{total}, {total - done} left, {mbps:6.2f} Mbps avg] "
                    f"{path} -> s3://{bucket}/{key}"
                )

    elapsed = time.monotonic() - start
    mbps = (bytes_sent * 8) / elapsed / 1_000_000 if elapsed > 0 else 0.0
    print(f"\n  Transferred {bytes_sent / 1_000_000:.1f} MB in {elapsed:.1f}s ({mbps:.2f} Mbps avg)")


def rewrite_markdown(key_map: dict[Path, str], public_url: str, dry_run: bool) -> list[Path]:
    public_url = public_url.rstrip("/") + "/"
    changed_files: list[Path] = []

    for md_file in sorted(CONTENT_DIR.rglob("*")):
        if md_file.suffix.lower() not in {".md", ".mdx"}:
            continue

        original = md_file.read_text(encoding="utf-8")
        text = original

        def replace(match: re.Match, group: int = 2) -> str:
            raw_path = match.group(group)
            if is_remote(raw_path):
                return match.group(0)

            resolved = (md_file.parent / unquote(raw_path)).resolve()
            key = key_map.get(resolved)
            if key is None:
                return match.group(0)

            new_url = public_url + key
            return match.group(1) + new_url + match.group(3)

        text = MARKDOWN_IMAGE_PATTERN.sub(replace, text)
        text = HTML_IMG_PATTERN.sub(replace, text)

        if text != original:
            changed_files.append(md_file)
            if not dry_run:
                md_file.write_text(text, encoding="utf-8")

    return changed_files


def delete_uploaded(key_map: dict[Path, str], rewritten: set[Path]) -> None:
    for path in key_map:
        # Only delete files whose every markdown reference we actually rewrote.
        # (rewritten tracks which local paths were successfully replaced.)
        if path in rewritten:
            print(f"  deleting {path}")
            path.unlink()

    # Prune now-empty per-guide image directories.
    for dirpath in sorted(CONTENT_DIR.rglob("*"), reverse=True):
        if dirpath.is_dir():
            try:
                dirpath.rmdir()
            except OSError:
                pass


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--delete", action="store_true", help="delete local image files after a successful upload + rewrite")
    parser.add_argument("--backup", action="store_true", help="copy every uploaded file into .imgbackups/ (mirroring its R2 key) as a local safety net")
    parser.add_argument("--dry-run", action="store_true", help="don't upload or write anything, just print what would happen")
    parser.add_argument("--workers", type=int, default=5, help="number of files to upload concurrently (default: 5)")
    args = parser.parse_args()

    endpoint = os.environ.get("R2_ENDPOINT")
    access_key = os.environ.get("R2_ACCESS_KEY")
    secret_key = os.environ.get("R2_SECRET_KEY")
    bucket = os.environ.get("R2_BUCKET")
    public_url = os.environ.get("R2_PUBLIC_URL")

    missing = [
        name for name, value in [
            ("R2_ENDPOINT", endpoint),
            ("R2_ACCESS_KEY", access_key),
            ("R2_SECRET_KEY", secret_key),
            ("R2_BUCKET", bucket),
            ("R2_PUBLIC_URL", public_url),
        ] if not value
    ]
    if missing:
        sys.exit(f"Missing required environment variables: {', '.join(missing)}")

    images = find_local_images()
    if not images:
        print("No local images found under content/ — nothing to do.")
        return

    print(f"Found {len(images)} local images under {CONTENT_DIR}/")
    key_map = build_key_map(images)

    if args.dry_run:
        unique_keys = len(set(key_map.values()))
        print(f"\n--dry-run: not uploading or writing anything. Would upload {unique_keys} unique files")
        print(f"({len(key_map) - unique_keys} local files are byte-identical to another and would be deduped):")
        for path, key in key_map.items():
            print(f"  {path} -> {key}")
        changed = rewrite_markdown(key_map, public_url, dry_run=True)
        print(f"\nWould rewrite {len(changed)} markdown files:")
        for f in changed:
            print(f"  {f}")
        if args.backup:
            print(f"\nWould also copy {unique_keys} files into {BACKUP_DIR}/")
        return

    import boto3
    from botocore.config import Config

    client = boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="auto",
        config=Config(signature_version="s3v4"),
    )

    if args.backup:
        print(f"\nBacking up uploaded files to {BACKUP_DIR}/ as they upload...")

    print("\nUploading...")
    upload_all(client, bucket, key_map, workers=args.workers, backup=args.backup)

    print("\nRewriting markdown...")
    changed = rewrite_markdown(key_map, public_url, dry_run=False)
    for f in changed:
        print(f"  rewrote {f}")

    if args.delete:
        if not args.backup:
            print("\nWarning: deleting local originals without --backup — content/ was the only")
            print("other copy of these images, so R2 becomes the sole copy after this.")
        print("\nDeleting local originals...")
        # Every uploaded file is eligible for deletion — rewrite_markdown already
        # replaced every reference to it (whether or not that particular file's
        # references lived in a file we touched this run).
        delete_uploaded(key_map, set(key_map.keys()))

    print(f"\nDone. Uploaded {len(key_map)} images, rewrote {len(changed)} markdown files.")
    if args.backup:
        print(f"Local copies kept in {BACKUP_DIR}/ in case R2 ever loses these.")
    if not args.delete:
        print("Local image files were left in place — re-run with --delete once you've verified the rewrite.")


if __name__ == "__main__":
    main()
