---
title: "USB Hub: PCB"
description: "Convert your USB hub schematic into a routed PCB layout in EasyEDA"
order: 1002
---

# USB Hub: PCB

Made by [@Rudy](https://github.com/Outdatedcandy92)

*Adapted from [Macondo's docs](https://macondo.hackclub.com/docs/usb-hub/pcb).*

With your schematic finished, it's time to turn it into a physical board.

## Converting to a PCB

Use the **Convert Schematic to PCB** button to open the PCB editor with your components already loaded, connected by **ratlines** — the blue lines showing which pads still need to be routed with copper traces.

## Placing components

Place components in logical clusters based on function rather than scattering them randomly. For example, the USB upstream connector and its capacitor and two pull-down resistors should sit together as one cluster near the upstream connector, not spread across the board.

## Routing

- Route the USB data pins as **differential pairs** — matched-length traces that keep the signal pair intact for reliable high-speed data. EasyEDA's differential pair routing tool is available via `Alt+D`.
- Add **copper pours** for power and ground so you're not routing every power connection as an individual trace.

## Custom board shapes

You aren't limited to a rectangle — EasyEDA supports importing a DXF file to define a custom board outline. A common workflow is converting an image into a DXF using an image-to-DXF tool, then importing that as your board shape.

## Polish

A few finishing touches that make a board feel like a finished product rather than a prototype:

- A keychain slot or mounting holes, if you want the hub to be portable or mountable.
- Silkscreen graphics or a logo.
- Filleted (rounded) edges instead of sharp corners.

## Next steps

Once your board is routed and polished, it's ready to send off for manufacturing.

**Next:** [Ordering →](/Hardware/Starter Projects/USB Hub/ordering/)

<aside class="callout">

Reviewers approve hardware builds based on your journals — keep logging your work. See [Good Journaling](/journals).

</aside>
