---
title: "Good Journaling"
description: "How to write journal entries that get your hours approved instead of bounced back"
group: "Getting Started"
order: 2
---

# Good Journaling

*Adapted from [Macondo's docs](https://macondo.hackclub.com/docs/journals).*

A journal entry is a short write-up of a chunk of work, plus a photo or two and the hours you spent. You post one as you build — it logs your time, keeps your project streak alive, and is the evidence a reviewer reads when you ship. Good journals get your hours approved. Lazy or AI-written ones get you bounced back.

The whole job: write what you did and **why**, show a picture of it, and log honest hours. The rest of this page is just how to do that well.

## Why your journal matters

You're building something new — learning skills, making mistakes, making decisions. When you look back on the project in a few years, you probably won't remember most of that. Journaling is the keepsake of your journey, and it's a trove of knowledge others can learn from.

Without a journal, none of your steps are documented — how you pieced things together, why you chose X over Y. Reviewers use your journals too, checking that your decisions make sense, your work is original, and it meets the submission requirements.

There's a reward angle too: the hours you log count toward your approved hours when you ship, and keep your streak ticking.

## What goes in an entry

| Field | What it is | The rule |
| --- | --- | --- |
| Title | A short line describing the entry | Required, 75 characters or fewer |
| Content | Your write-up of the work | Required, at least 100 characters of actual writing (images don't count) |
| Image | A photo or screenshot of the work | Required — hardware needs more images for longer sessions, see below |
| Hours | How long you worked | Logged in 0.1-hour steps, up to 20 per entry |

If a session ran longer than 20 hours, split it into multiple entries — short and frequent beats one giant dump anyway.

## How to write a good entry

A good journal is a story — *your* story. You don't need perfect grammar. AI doesn't know your story, so it'll write a bad journal — don't use it.

### No AI in journals

Reviewers can tell when a journal is AI-generated, and it's grounds for rejection. Write it yourself, even if you think your writing is bad — honest beats polished. Write one entry per day's work, or per milestone; short and frequent beats long and sparse.

### Explain your decisions, not just your actions

The most important part of an entry is explaining *why*, not just *what*. Every entry should answer:

- What did you do?
- Why did you do it?
- What problems did you face?

### Screenshot and document everything

Screenshot your work at every meaningful step, not just when it's polished — show the messy intermediates, the before and after when you fix something. Same goes for photos on physical builds. For hardware, aim for roughly **one image per 5 hours of work**, with at least one on every entry — a 20-hour entry backed by a single screenshot isn't reviewable.

### Make mistakes. Describe them. Fix them.

You will make mistakes — footprints that are off, wiring that needs to be redone. Write about them, then fix them. A journal with no mistakes reads like a manual, not a journal.

## Video in a journal

Videos are great for showing something working, a timelapse, or a tricky build step. Images and video links must be hosted on `cdn.hackclub.com` — uploading through the journal editor's formatting buttons handles this automatically. A regular link to a YouTube video is fine to paste into your text; the CDN rule applies to direct video file links (`.mp4`, `.mov`, `.webm`, and similar).

## Logging time spent learning

Time spent on the project counts when it's real work on the project — including the figuring-out and the false starts. Log your hours honestly.

## Art and asset hours

Sprite art, UI mockups, music, 3D models, level design, and similar work can be logged through journals too, and counts toward your approved hours alongside coding or build time. As a general rule, art and asset hours shouldn't exceed roughly **40% of a project's total approved hours** — reviewers can make exceptions for exceptionally high-quality, clearly original work with intermediates documented in the journal, but quick sketches, generic stock assets, and AI-generated art won't earn one.

The most reliable way to back up art hours is a **timelapse of the work** — a tool like Lapse works well for this, or a manual screen recording. Link the timelapse directly in the journal entry so a reviewer doesn't have to dig for it.

## Do's and don'ts

| Do | Don't |
| --- | --- |
| Explain what you did, why you did it, and how | State only what you did, with no explanation why |
| Screenshot and document everything | Use generic statements like "I wired it up" or "I did CAD" |
| Describe your mistakes | Show only the end product |

## Examples

**A weak entry** looks like: *"I added a buck converter and wired it up. I did CAD and added a case. I soldered everything together and it worked!"* — paired with one generic photo. It never explains why the buck converter or case were needed, what design choices went into the case, or how it was tested.

**A strong entry**, adapted from [@alexren](https://github.com/qcoral/)'s [hwdocs example journal](https://hwdocs.hackclub.dev/shipping/example-journal/), reads more like: getting a Raspberry Pi's display working by adapting wiring from a different project that used a different display driver, digging through GitHub repos to find the right kernel driver parameters, and finally getting video output — with photos at each intermediate stage, not just the final result. The difference is that it shows the thought process, the research chain, and the mistakes along the way, not just a checklist.

## See also

- [Shipping Projects](/shipping) — what reviewers check when you ship
- [Hackatime](/Software/hackatime) — how your coding time gets tracked automatically
