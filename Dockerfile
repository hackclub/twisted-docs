# ---------- Builder ----------
FROM python:3.13-slim AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates nodejs npm && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p static

RUN npm install --no-save tailwindcss@^4 @tailwindcss/cli@^4 @tailwindcss/typography

RUN npx --yes @tailwindcss/cli \
        -i input.css \
        -o static/output.css \
        --minify

RUN PYTHONPATH=/install/lib/python3.13/site-packages \
    python build.py

# ---------- Runtime ----------
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80