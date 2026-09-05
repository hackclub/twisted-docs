---
title: "USB Hub: Schematics"
description: "Design a USB hub schematic in EasyEDA — the SL2.1S hub IC, USB connectors, and supporting components"
order: 1001
---

# USB Hub: Schematics

Made by [@Rudy](https://github.com/Outdatedcandy92)

*Adapted from [Macondo's docs](https://macondo.hackclub.com/docs/usb-hub/schematics).*

Now that you're comfortable in EasyEDA, it's time to design the schematic for your USB hub — placing the hub IC and connectors, then wiring up power, data, and the supporting passives around them.

## The hub IC

The **SL2.1S** chip (JLCPCB part `C2684433`) is the brain of your USB hub — it splits one upstream USB connection into four usable downstream ports. Place it on your schematic as the centerpiece of the design.

## Connectors

You'll need at least one upstream connector and several downstream ports:

- **Upstream:** a USB Type-C connector (`C2765186`) works well.
- **Downstream:** a mix of Type-C and Type-A connectors (`C668591`) is common, though you can customize your own port configuration.

## Supporting components

Around the hub IC and connectors, you'll need:

- **5.1 kΩ pull-down resistors** on the upstream USB-C CC pins.
- **56 kΩ pull-up resistors** on each downstream USB-C CC pin.
- **1 µF and 100 nF decoupling capacitors** for power stability, placed close to the IC's power pins following standard schematic conventions.

## Keeping it clean

Aim for a clean schematic that's much easier to debug, share, and come back to later:

- Place components in a logical left-to-right layout: upstream connector → hub IC → downstream connectors.
- Use net labels for data lines and power rails instead of long crisscrossing wires, so connections stay easy to trace.
- Group each connector with its own supporting resistors/capacitors so the schematic reads as a set of clear building blocks rather than a tangle.

## Next steps

With your schematic wired up, it's time to lay it out as a physical board.

**Next:** [PCB →](/Hardware/Starter Projects/USB Hub/pcb/)

<aside class="callout">

Keep journaling as you build! See [Good Journaling](/journals) for what reviewers look for.

</aside>
