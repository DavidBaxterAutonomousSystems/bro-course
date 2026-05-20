# Build Notes

This page is a shared place to collect follow-up prompts, side quests, lessons learned, known unknowns, and practical build notes as the study circle develops.

## Suggested Follow-Up

After the first meeting:

- Look at the subsystem groups in the [BOM](bom.md) and pick one that you are most interested in.
- Maybe it is the one you know most about, or just one you think is cool.
- Tell us why next meeting.

Also think about this:

- If somehow you already knew how to do it, what is something cool you would like to do with a drone?
- Race it autonomously through a drone course?
- Do orienteering without hitting any trees?

## Side Quests

These are optional directions for anyone who wants to explore beyond the main build.

- Source another BOM, or source one subsystem for another build.
    - Try to find compatible parts that are better by some measure of your choice.
    - You could compare cost, availability, documentation, weight, power, repairability, or quality.
    - Possibly keep the same general size as our drone, or intentionally go bigger or smaller.
    - How many similar parts can you find that are manufactured in the EU?

## Documentation TODOs

Things we may want to add as the site develops:

- Add pictures for each part.
- Explain each part.

## Identifiable Skills and Capabilities

These are skills or capabilities that should become more concrete as we build.

- Charge and use a LiPo battery.
- Solder.

## Lessons Learned

### Meeting 1

- Plugging the battery into the charger is itself a practical step to learn: connector type, polarity, balance lead, cell count, and charging mode all matter.
- A battery's **capacity** tells us roughly how much electric charge it can store. A **3300 mAh** battery can also be written as **3.3 Ah**, because **1000 mAh = 1 Ah**. The unit **Ah** means **amp-hours**. A capacity of **3.3 Ah** means that, in theory, the battery could provide **3.3 amps for 1 hour**, or **1 amp for 3.3 hours**, or **6.6 amps for 0.5 hours**.
- The **C rating** is a multiplier on that capacity. So for a **3.3 Ah** battery, **1C = 3.3 A**. In theory, discharging at **1C** would empty the battery in **1 hour**. A **40C** rating means **40 x 3.3 A = 132 A** maximum rated discharge current. In theory, discharging at **40C** would empty the battery in **1/40 of an hour**, or about **90 seconds**.
- In practice, treat **C ratings** as optimistic and leave margin for **voltage sag, heat, battery age, connectors, and wiring**.
- An **XS LiPo** means **X cells in series**. For example, a **4S LiPo** has four cells in series. Pack voltage is the per-cell voltage multiplied by the number of cells.
- If the battery manufacturer does not specify a charge rate, a rough safe rule of thumb is to charge at **1C** or less. For a **3300 mAh** pack, **1C charging = 3.3 A**.
- For LiPo voltage, think per cell first. **Maximum/full** is about **4.20 V per cell**, **storage** is about **3.80 V per cell**, and **minimum** should be treated cautiously. Avoid going below about **3.3 V per cell under load**, and never intentionally discharge near or below **3.0 V per cell**.
- For an **XS LiPo**, multiply those values by **X**. A **4S** pack is about **16.8 V full**, **15.2 V at storage**, and should generally be kept above roughly **13.2 V under load**.

## Known Unknowns

### Soldering Tip Preparation

What should we do, if anything, to prepare a new soldering iron tip before using it?

Some things to check before soldering the power system:

- Should the new tip be cleaned, tinned, or otherwise prepared before the first joint?
- What temperature range should we use for the wire, pads, and solder we have?
- How do we keep the tip from oxidizing while working?
- When should we use the brass sponge, wet sponge, flux, or extra solder?

### Camera Data and Video

How do we get camera data both to the Raspberry Pi for computer vision tasks that tell the flight controller what to do, and also get that video transmitted externally with low latency so we can see what the drone sees?

We may need another part. I am not sure if we can use the Kahuna to plug into the Raspberry Pi instead of the flight controller and stream data back over WiFi. I have not really looked into how the Kahuna interfaces and what it exactly does.

### Camera Mounting

How should we mount either camera?

It would probably be best to 3D print a housing for each camera that attaches nicely to the frame. We still need to decide roughly where on the frame each camera should go, then measure, design, and print the mounting part.

### Pixhawk Wiring

Where does everything plug into the Pixhawk flight controller?

I believe everything should have a place to go with the right connectors to fit, but I have not verified it yet or looked closely through the flight controller documentation and informal guides.
