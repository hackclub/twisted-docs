---
title: Shipping Software
description: How to ship a software project for Twisted
order: 1
---

This page is specifically about shipping software, you can find more about shipping [here](/shipping).

# The four things every ship needs

## 1. A public repo
You need a github repo, which is set to public, with real commit history. Don't put six weeks of work into one `initial commit`, as we have no evidence you built it.
Use Github desktop or Git to regularly commit whenever you feel that you made something or did progress.

## 2. A README that has enough info
Reviewers will read it first, and it's what people see when they find your repo later.

You can use this as a starting point for your README:
~~~markdown
# Project name

A short description on what it does 

![screenshot](path/to/screenshot.png)

## Try it
https://example.com

## Features
- The thing it does
- The other thing it does

## Running locally
```bash
git clone https://github.com/your_username/blahblahblah
cd project
npm install
npm run dev
```

## Built with
(insert whatever you built this with)
~~~
Feel free to modify this, or not use this at all (even better!). Make your README as customised as possible with images, links, more about you, etc.

### 3. A live demo
The format depends on what you built so you should see [Shipping by project type](#shipping-by-project-type) below.


## Shipping by project type
### Web apps and sites
This is the easiest to setup and demo.

| Host | Good for | Notes |
| --- | --- | --- |
| [GitHub Pages](https://pages.github.com/) | Static sites | Free, simple, but no backend |
| [Hack Club Nest](https://hackclub.app/) | Anything, including backends adn databases | Free for Hack clubbers, real Linux server |
| [Vercel](https://vercel.com/) / [Netlify](https://netlify.com/) | Next.js, React, static and serverless | Free tier, deploys when you push to github |

Don't use Render, Railway, Streamlit or anything that is a free trial or has loading time.

### Games
- **Web playable is nicer for us** Godot, Unity, and Construct all export to HTML5, which ship that to GitHub Pages or [itch.io](https://itch.io/) so people play it simply.
- If you must ship a binary, build for **Windows, macOS, and Linux**, and attach them to a Github Release
- Include controls in the README, so reviewers don't get confused.

### CLI tools and libraries
- Publish it: [npm](https://npmjs.com/), [PyPI](https://pypi.org/), [crates.io](https://crates.io/) or something like that
- Or attach prebuilt executables to a GitHub Release.

### Mobile apps
- **Android:** Preferabily on Google Play Store, but an APK on Github Releases also works.
- **iOS:** This isn't required, as Apple doesnt provide an easy way to sideload iOS apps, but an app on the App Store would be nice

## Track your time

Most YSWS programs verify hours with [Hackatime](https://hackatime.hackclub.com/setup), which is Hack Club's time tracker. Install the plugin for your editor **before** you start building.

Check that it's actually logging after your first session as you don't want to be losing time.

