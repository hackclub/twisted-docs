#!/usr/bin/env bash
set -euo pipefail

image_name="twisted_docs:latest"
container_name="twisted_docs_site"
host_port="8080"
container_port="80"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd "$script_dir/.." && pwd)"

cd "$project_root"

docker build -t "$image_name" .

docker rm -f "$container_name" >/dev/null 2>&1 || true

docker run -d \
  --name "$container_name" \
  -p "$host_port:$container_port" \
  "$image_name" >/dev/null

printf 'Built %s and started %s on http://127.0.0.1:%s/\n' "$image_name" "$container_name" "$host_port"
