---
title: "USB Hub"
description: "Design your first custom USB hub PCB from scratch in EasyEDA, no electronics background needed"
order: 1000
---

# USB Hub

Made by [@Rudy](https://github.com/Outdatedcandy92)

*Adapted from [Macondo's docs](https://macondo.hackclub.com/docs/usb-hub).*

By the end of this guided project you'll have designed your own custom USB hub and ordered it as a real, assembled circuit board. No prior PCB experience is needed.

This first page is the gentle on-ramp: you'll set up your free EasyEDA account, create a project, and get comfortable with the two editors you'll live in (the Schematic editor and the PCB editor). The hands-on building starts on the next page, so treat this one as your map of the workspace.

## What you'll need

- A free **EasyEDA Pro** account. It's online, so there's nothing to install.
- A few minutes to click around. You don't need to memorize anything here, you're just getting your bearings.

## Getting started

Head over to [pro.easyeda.com](https://pro.easyeda.com/) and create an account, then log in. Once you're in, click the **Use Online** button (or go straight to [pro.easyeda.com/editor](https://pro.easyeda.com/editor)) to open the main dashboard.

To create a project, go to `File -> New -> Project`, or use the `Shift + N` shortcut. Give your project a name and, optionally, a short description. Once saved, the editor opens your new project — you'll see your project name in the left sidebar with a `Schematic1` and `PCB` file underneath it. These are the two files you'll be working on to design your USB hub.

## Schematic editor

Double-click `Schematic1` in the sidebar to open it. The schematic editor is where you design the *logic* of your circuit — how everything connects, using symbols instead of physical components. If someone understands your schematic, they understand how your circuit works, even without seeing the physical board.

> If the PCB editor is building the house, the schematic editor is the blueprint. It defines what goes where and how everything is connected, before you worry about the physical layout.

A few of the most important tools in the schematic editor's toolbar:

- **Components** — search the parts library (microcontrollers, connectors, regulators, and more) and place their symbols.
- **Resistor** — a shortcut for placing a resistor symbol; right-click it for other common passives like capacitors, inductors, and diodes.
- **Wire** — draws wires connecting components together.
- **Net Flag / Label** — a cleaner alternative to long wires. Two net flags that share a name are electrically connected, even with no visible wire between them, which keeps busy schematics readable.

The property sidebar on the right shows the properties of whatever's currently selected (or the page itself, if nothing is selected).

## PCB editor

Click `PCB1` in the sidebar to open the PCB editor. This is where your design becomes physically real: you set the board shape, arrange components on the layout, and draw copper traces connecting everything together.

> Unlike the schematic editor, which focuses on logic, the PCB editor is all about physical placement and routing — spacing, trace paths, and how everything fits on the board.

A quick, non-technical rundown of the first few PCB tools:

- **Pad** — the copper landing points where component leads or pins get soldered.
- **Via** — a small hole connecting copper traces between different layers of the board.
- **Board Outline** — defines the actual shape and size of your PCB; whatever you draw here is what gets manufactured.
- **Copper Area** — creates large copper regions (like ground or power planes) instead of routing many individual traces.
- **Fill Region** — similar to a copper area, but more general purpose; often used for shielding or custom copper shapes.

The right sidebar lists all the board's layers. For most beginner boards you only need to worry about five: the **Top Layer**, **Bottom Layer**, **Top Silkscreen**, **Bottom Silkscreen**, and the **Board Outline Layer** — more on those below.

## Anatomy of a PCB

A standard 2-layer PCB is made of two copper layers separated by a non-conductive substrate (usually FR4), which gives the board its strength while keeping the two copper layers electrically isolated.

Bare copper would oxidize and could short against other conductive surfaces, so manufacturers cover most of it with **solder mask** — a thin, non-conductive protective coating, like paint for your PCB, that also helps prevent accidental solder bridges.

On top of the solder mask sits the **silkscreen** layer — the text and graphics printed on the board (component names, reference designators like `R1` or `U2`, polarity markings, logos). It carries no electricity; it's purely for labeling, which helps a lot when assembling, debugging, or modifying your board later.

## Next steps

Now that you're comfortable navigating EasyEDA, it's time to put that knowledge into practice on the next page.

**Next:** [Schematics →](/Hardware/Starter Projects/USB Hub/schematics/)

<aside class="callout">

You must journal as you follow this guide! Reviewers approve hardware builds based on your journals — write an entry for every work session with photos, notes, and what went wrong. You can follow this guide, but you need to make your own changes to it; exact copies won't be approved. See [Good Journaling](/journals) for more.

</aside>
