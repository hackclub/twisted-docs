---
title: "USB Hub: Ordering"
description: "Run a design rule check and order your USB hub as an assembled board from JLCPCB"
order: 1003
---

# USB Hub: Ordering

Made by [@Rudy](https://github.com/Outdatedcandy92)

*Adapted from [Macondo's docs](https://macondo.hackclub.com/docs/usb-hub/ordering).*

Before you order, run EasyEDA's **Design Rule Checker (DRC)** — it scans your design for issues that could cause problems during manufacturing. A common one at this stage is a differential pair error; if you hit it, adjust the length tolerance setting to `10` in the Design Rules configuration and re-run the check.

## Ordering from JLCPCB

Once the DRC passes, click **Order PCB**. A few settings matter most:

- **PCB Color** — green is the default; black and white are also available if you want a different look.
- **Surface Finish** — HASL (silver, default), HASL Lead Free, or ENIG (gold) for a nicer finish.
- **PCBA** — set the assembly type to Economic, with a quantity of 2 (one spare in case something goes wrong during assembly or soldering).

## Checking your BOM

Before checking out, double-check the Bill of Materials page — make sure every part on your board actually has a part selected and sourced, not left blank. A missing part here means a missing component on your finished board.

<aside class="callout">

Once your order is placed, keep journaling while you wait and while you assemble/test the board when it arrives — see [Good Journaling](/journals) and [Shipping Hardware](/Hardware/shipping) for what to do next.

</aside>
