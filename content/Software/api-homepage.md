---
title: "Learn how to use an API"
description: "Build a static homepage that pulls in NASA's picture of the day, a live clock, and real weather data"
order: 6
---

# Learn how to use an API

Made by Nico

*Adapted from [Macondo's docs](https://macondo.hackclub.com/docs/api-homepage).*

This guide teaches you to build a static homepage that integrates three REST APIs: NASA's Astronomy Picture of the Day (APOD) as a background, a JavaScript clock, and Open-Meteo for live weather. You need basic HTML/CSS/JavaScript knowledge, a code editor, and a modern browser — no build tools required.

## What you'll learn

- What REST APIs are, and how JSON responses work
- Calling APIs with `fetch` and `async`/`await`
- Error handling with `try`/`catch`
- Reading the user's location via `navigator.geolocation`
- Running code repeatedly with `setInterval`
- Full-screen CSS background layouts

## Project structure

Create three files: `index.html`, `main.css`, and `script.js`.

## Part 1 — Background image

Register a free key at [api.nasa.gov](https://api.nasa.gov) and use NASA's APOD API, which returns JSON containing an image URL. Use `fetch` to retrieve the data, parse the JSON, confirm the media type is actually an image (APOD occasionally returns a video), and apply the result as a full-screen CSS background.

**Security note:** there is no safe way to hide an API key in a static HTML/CSS/JS site — keep that in mind for anything more sensitive than a rate-limited public API key.

## Part 2 — Clock

Build a live clock by converting the current Unix timestamp into readable hours, minutes, and seconds, then use `setInterval` to update it every second. `Date` object methods, the modulo operator, and `Math.floor` are your main tools here — try implementing it yourself before looking anything up.

## Part 3 — Weather

Integrate [Open-Meteo](https://open-meteo.com/)'s free weather API, which needs no API key. Use `navigator.geolocation.getCurrentPosition()` to get the user's coordinates, then build the API request URL dynamically from them.

**Note:** geolocation requires HTTPS or `localhost` — it won't work from a plain `file://` URL.

## Troubleshooting

- Rate-limited API keys
- APOD occasionally returning a video instead of an image
- No geolocation prompt when opening the page via `file://`
- CORS errors from a typo in the request URL
- Script execution timing issues (make sure your script runs after the DOM is ready)

## Next steps

Add your own feature on top using another public API — cat facts, trivia, an AI chatbot via [ai.hackclub.com](https://ai.hackclub.com), or a Spotify integration. Include a `README.md` explaining your project before you submit it.
