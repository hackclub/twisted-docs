from __future__ import annotations

import os
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pygments.formatters import HtmlFormatter
import json


CONTENT_DIR = Path("content")
DIST_DIR = Path("dist")
STATIC_DIR = Path("static")
ASSET_DIR = Path("assets")
TEMPLATE_DIR = Path("templates")
BASE_URL = os.environ.get("BASE_URL", "").rstrip("/")

MARKDOWN_EXTENSIONS = [
    "extra",
    "tables",
    "toc",
    "fenced_code",
    "codehilite",
    "admonition",
    "attr_list",
]

MARKDOWN_EXTENSION_CONFIGS = {
    "toc": {
        "title": "On this page",
        "permalink": True,
    }
}

IMAGE_TAG_PATTERN = re.compile(
    r'(<img\b[^>]*\bsrc=")([^"]+)(")',
    re.IGNORECASE,
)


@dataclass(slots=True)
class Page:
    """A rendered documentation page and its related navigation metadata."""

    source: Path
    relative_path: Path
    slug: str
    title: str
    description: str
    order: int
    group: str | None
    icon: str | None
    cover: str | None
    tags: list[str]
    markdown: str
    nav_path: tuple[str, ...]
    html: str = ""
    toc: str = ""
    url: str = ""
    output: Path | None = None
    breadcrumbs: list[dict[str, str | None]] = field(default_factory=list)
    previous: Page | None = None
    next: Page | None = None


@dataclass(slots=True)
class NavNode:
    """A single node in the tree-based navigation model."""

    title: str
    icon: str | None = None
    page: Page | None = None
    children: list[NavNode] = field(default_factory=list)
    order: int = 9999


class Builder:
    """Builds the static documentation site into the dist directory."""

    def __init__(self) -> None:
        self.pages: list[Page] = []
        self.navigation: list[NavNode] = []

        self.environment = Environment(
            loader=FileSystemLoader(TEMPLATE_DIR),
            autoescape=select_autoescape(["html"]),
        )
        self.template = self.environment.get_template("page.html")
        self.markdown = markdown.Markdown(
            extensions=MARKDOWN_EXTENSIONS,
            extension_configs=MARKDOWN_EXTENSION_CONFIGS,
        )

    @staticmethod
    def clean_title(text: str) -> str:
        """Convert a slug-like string into a readable title."""

        return text.replace("-", " ").replace("_", " ").strip().title()

    @staticmethod
    def coerce_order(value: object) -> int:
        """Normalise frontmatter order values into integers."""

        if isinstance(value, int):
            return value

        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                return 9999

        return 9999

    @staticmethod
    def normalise_tags(value: object) -> list[str]:
        """Convert frontmatter tags into a clean list of strings."""

        if value is None:
            return []

        if isinstance(value, str):
            return [tag.strip() for tag in re.split(r"[,\s]+", value) if tag.strip()]

        if isinstance(value, (list, tuple)):
            tags: list[str] = []
            for item in value:
                text = str(item).strip()
                if text:
                    tags.append(text)
            return tags

        text = str(value).strip()
        return [text] if text else []

    @staticmethod
    def slug_for_path(path: Path) -> str:
        """Derive a clean URL slug from a content file path."""

        if path.stem == "index":
            if path.parent == Path("."):
                return ""
            return path.parent.as_posix()

        return path.with_suffix("").as_posix()

    @staticmethod
    def output_path_for_slug(slug: str) -> Path:
        """Map a slug to its final output HTML path."""

        if not slug:
            return DIST_DIR / "index.html"

        return DIST_DIR / slug / "index.html"

    @staticmethod
    def site_url_for_slug(slug: str) -> str:
        """Build a site URL that respects the configured base URL."""

        prefix = BASE_URL

        if slug:
            return f"{prefix}/{slug}/" if prefix else f"/{slug}/"

        return f"{prefix}/" if prefix else "/"

    @staticmethod
    def _to_posix_relative_path(path: Path) -> str:
        return path.as_posix().lstrip("./")

    def clean(self) -> None:
        """Remove the previous build output and create a fresh dist directory."""

        print("Cleaning dist...")

        if DIST_DIR.exists():
            shutil.rmtree(DIST_DIR)

        DIST_DIR.mkdir(parents=True, exist_ok=True)

    def scan(self) -> None:
        """Collect markdown sources and frontmatter into Page objects."""

        print("Scanning markdown...")

        self.pages.clear()

        if not CONTENT_DIR.exists():
            print("   No content directory found.")
            return

        for file in sorted(CONTENT_DIR.rglob("*")):
            if file.suffix.lower() not in {".md", ".mdx"}:
                continue

            post = frontmatter.load(file)
            relative_path = file.relative_to(CONTENT_DIR)
            slug = self.slug_for_path(relative_path)
            group = post.get("group")
            group_text = str(group).strip() if group is not None and str(group).strip() else None

            if group_text:
                nav_path = tuple(
                    self.clean_title(segment)
                    for segment in group_text.split("/")
                    if segment.strip()
                )
            else:
                nav_path = tuple(
                    self.clean_title(part)
                    for part in relative_path.parent.parts
                    if part not in {"."}
                )

            if post.get("title"):
                title = str(post.get("title")).strip()
            elif relative_path.stem == "index":
                title = self.clean_title(relative_path.parent.name) if relative_path.parent != Path(".") else "Home"
            else:
                title = self.clean_title(relative_path.stem)

            page = Page(
                source=file,
                relative_path=relative_path,
                slug=slug,
                title=title,
                description=str(post.get("description", "")).strip(),
                order=self.coerce_order(post.get("order", 9999)),
                group=group_text,
                icon=(str(post.get("icon")).strip() if post.get("icon") else None),
                cover=(str(post.get("cover")).strip() if post.get("cover") else None),
                tags=self.normalise_tags(post.get("tags")),
                markdown=post.content,
                nav_path=nav_path,
            )
            page.url = self.site_url_for_slug(slug)
            page.output = self.output_path_for_slug(slug)
            self.pages.append(page)

        print(f"Found {len(self.pages)} pages.")

    def _copy_image_reference(self, page: Page, source: str) -> str:
        """Copy a relative image into the page output directory and rewrite the URL."""

        split = urlsplit(source)

        if split.scheme in {"http", "https"} or source.startswith("//"):
            return source

        if split.path.startswith("/"):
            return source

        relative_reference = Path(split.path)
        source_file = (page.source.parent / relative_reference).resolve()

        if not source_file.exists():
            return source

        try:
            copied_relative_path = source_file.relative_to(page.source.parent.resolve())
        except ValueError:
            copied_relative_path = Path(source_file.name)

        destination = (page.output.parent if page.output else DIST_DIR) / copied_relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, destination)

        rewritten = copied_relative_path.as_posix()
        if split.query:
            rewritten = f"{rewritten}?{split.query}"
        if split.fragment:
            rewritten = f"{rewritten}#{split.fragment}"
        return rewritten

    def _rewrite_image_sources(self, page: Page, html: str) -> str:
        """Rewrite local image sources after copying them into the output tree."""

        def replace(match: re.Match[str]) -> str:
            prefix, source, suffix = match.groups()
            return f"{prefix}{self._copy_image_reference(page, source)}{suffix}"

        return IMAGE_TAG_PATTERN.sub(replace, html)

    def render_markdown(self) -> None:
        """Render markdown to HTML and capture the generated table of contents."""

        print("📝 Rendering markdown...")

        for page in self.pages:
            self.markdown.reset()
            rendered = self.markdown.convert(page.markdown)
            page.toc = self.markdown.toc
            page.html = self._rewrite_image_sources(page, rendered)

    def _insert_navigation_page(self, nodes: list[NavNode], nav_path: tuple[str, ...], page: Page) -> None:
        """Insert a page into the tree while creating any missing group nodes."""

        current_nodes = nodes

        for segment in nav_path:
            group_node = next(
                (node for node in current_nodes if node.page is None and node.title == segment),
                None,
            )
            if group_node is None:
                group_node = NavNode(title=segment)
                current_nodes.append(group_node)
            current_nodes = group_node.children

        current_nodes.append(
            NavNode(
                title=page.title,
                icon=page.icon,
                page=page,
                order=page.order,
            )
        )

    def _finalise_navigation(self, nodes: list[NavNode]) -> None:
        """Sort navigation nodes recursively and propagate section order values."""

        for node in nodes:
            if node.children:
                self._finalise_navigation(node.children)
                if node.page is None and node.children:
                    node.order = min(child.order for child in node.children)

        nodes.sort(key=lambda node: (node.order, node.title.casefold()))

    def build_navigation(self) -> None:
        """Build a tree-based navigation structure from the scanned pages."""

        print("🧭 Building navigation...")

        self.navigation = []

        for page in self.pages:
            self._insert_navigation_page(self.navigation, page.nav_path, page)

        self._finalise_navigation(self.navigation)

    def _flatten_navigation(self, nodes: list[NavNode]) -> list[Page]:
        """Flatten the navigation tree into the page order used for pagination."""

        pages: list[Page] = []

        for node in nodes:
            if node.page is not None:
                pages.append(node.page)
            pages.extend(self._flatten_navigation(node.children))

        return pages

    def build_pagination(self) -> None:
        """Assign previous and next links from the flattened navigation tree."""

        print("⬅Building pagination...")

        ordered_pages = self._flatten_navigation(self.navigation)

        for page in self.pages:
            page.previous = None
            page.next = None

        for index, page in enumerate(ordered_pages):
            if index > 0:
                page.previous = ordered_pages[index - 1]
            if index < len(ordered_pages) - 1:
                page.next = ordered_pages[index + 1]

    def _find_navigation_path(self, nodes: list[NavNode], page: Page) -> list[NavNode] | None:
        """Locate the navigation trail for a page inside the tree."""

        for node in nodes:
            trail = [node]
            if node.page is page:
                return trail

            child_path = self._find_navigation_path(node.children, page)
            if child_path is not None:
                return trail + child_path

        return None

    def build_breadcrumbs(self) -> None:
        """Build breadcrumb trails from the navigation tree."""

        print("Building breadcrumbs...")

        for page in self.pages:
            page.breadcrumbs = [{"title": "Home", "url": self.site_url_for_slug("")}]

            if page.slug == "":
                continue

            trail = self._find_navigation_path(self.navigation, page)
            if trail is None:
                if page.title:
                    page.breadcrumbs.append({"title": page.title, "url": None})
                continue

            for node in trail[:-1]:
                page.breadcrumbs.append({"title": node.title, "url": None})

            page.breadcrumbs.append({"title": trail[-1].title, "url": None})

    def copy_static(self) -> None:
        """Copy the static directory into dist/static if it exists."""

        if not STATIC_DIR.exists():
            return

        print("Copying static...")

        shutil.copytree(STATIC_DIR, DIST_DIR / "static", dirs_exist_ok=True)

    def copy_assets(self) -> None:
        """Copy the assets directory into dist/assets if it exists."""

        if not ASSET_DIR.exists():
            return

        print("Copying assets...")

        shutil.copytree(ASSET_DIR, DIST_DIR / "assets", dirs_exist_ok=True)

    def generate_pygments(self) -> None:
        """Generate the code block stylesheet used by the Jinja template."""

        print("Generating syntax highlighting...")

        css = HtmlFormatter(style="github-dark").get_style_defs(".codehilite")
        target = DIST_DIR / "static" / "pygments.css"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(css, encoding="utf-8")

    def generate_search_index(self) -> None:
        """Generate a simple JSON search index of pages for client-side searching."""

        print("Generating search index...")

        index: list[dict[str, str]] = []

        for page in self.pages:
            # Strip HTML tags to create a plaintext content field
            plain = re.sub(r'<[^>]+>', '', page.html or '')
            plain = re.sub(r'\s+', ' ', plain).strip()

            index.append({
                "title": page.title,
                "url": page.url,
                "slug": page.slug,
                "description": page.description or "",
                "content": plain,
            })

        target = DIST_DIR / "search_index.json"
        target.write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")

        print("   ✓ search_index.json")

    def page_context(self, page: Page) -> dict[str, object]:
        """Prepare the template context for a single page."""

        return {
            "title": page.title,
            "description": page.description,
            "content": page.html,
            "toc": page.toc,
            "navigation": self.navigation,
            "breadcrumbs": page.breadcrumbs,
            "previous": page.previous,
            "next": page.next,
            "current_slug": page.slug,
            "base_url": BASE_URL,
            "page": page,
        }

    def render_page(self, page: Page) -> str:
        """Render a single page with the shared Jinja template."""

        return self.template.render(**self.page_context(page))

    def write_page(self, page: Page) -> None:
        """Write one rendered page to disk using clean URLs."""

        if page.output is None:
            raise ValueError(f"Missing output path for {page.source}")

        html = self.render_page(page)
        page.output.parent.mkdir(parents=True, exist_ok=True)
        page.output.write_text(html, encoding="utf-8")

        print("   ✓", page.output.relative_to(DIST_DIR))

    def write_pages(self) -> None:
        """Render and write every page in the site."""

        print()
        print("Writing pages...")
        print()

        for page in self.pages:
            self.write_page(page)

    def build(self) -> None:
        """Run the full static site build pipeline."""

        self.clean()
        self.scan()
        self.render_markdown()
        self.build_navigation()
        self.build_breadcrumbs()
        self.build_pagination()
        self.copy_static()
        self.copy_assets()
        self.generate_pygments()
        self.generate_search_index()
        self.write_pages()

        print()
        print("=" * 60)
        print("Build completed successfully!")
        print()
        print(f"Pages          : {len(self.pages)}")
        print(f"Navigation roots: {len(self.navigation)}")
        print(f"Output         : {DIST_DIR.resolve()}")
        print("=" * 60)


def main() -> None:
    Builder().build()


if __name__ == "__main__":
    main()
