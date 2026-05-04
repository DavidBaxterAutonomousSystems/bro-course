# Study Circle (Spring 2026)

This page is specifically about the **study circle** run with Folkuniversitetet Örebro.

It is related to BRO, but it is **not** the full BRO course format.  
The study circle is a small BRO-inspired format that is group-driven and will hopefully also test, improve, and document a future stronger course version.

## Why This Study Circle Exists

- **Learn together** through a practical, hands-on build and integration process.
- Have fun building a real autonomous system that can do something the group imagines and works toward together.
- Document the process in parallel so it can be reused as part of BRO course development.

## Study Circle Format

- Approximately 6+ participants.
- Approximately 1 meeting per week.
- Approximately 3 study hours per meeting.
- Approximately 6 weeks total.
- Small-group, practical format at ORU.

## Technical Goal

Minimum goal: Start from a box of parts and reach a working drone system that can be configured, monitored, and commanded from a nearby computer to perform a simple autonomous waypoint mission.

Stretch goal: Define and demonstrate a customized autonomous mission selected by group interest.

The focus is broader than flight alone and should provide understanding of hardware setup, autopilot, software stack, communication, and practical system integration.

## Stretch Demo Brainstorming

To help the group choose an exciting stretch demo, here are a few realistic examples:

- Search-and-rescue style sweep: fly an autonomous area sweep to find preplaced objects and report their locations.
- Autonomous orienteering challenge: navigate a sequence of checkpoints with scoring for accuracy and completion time.
- GPS-denied navigation demo: test local-navigation methods without GPS, with an optional extension to controlled indoor autonomous flight.
- Cybersecurity mission-hardening demo: map likely attack paths (GCS, telemetry radios, companion link) and implement at least one mitigation per path.
- Companion-computer autonomy demo: run onboard Raspberry Pi computer-vision and control logic to follow a moving object of a selected class.
- Field reliability challenge: repeat the same autonomous mission across multiple runs and evaluate consistency, timing, and recovery behavior.

These are starting points for discussion; the group decides what to build toward.

## What We Plan To Cover

- Core architecture of a modern autonomous platform.
- Major hardware and software components.
- Practical build and setup workflow.
- Autopilot and ground-control basics.
- Communication and integration concepts.
- A repeatable demo-oriented setup.

## Participant-Directed Goals

The group can set shared priorities during the study circle, for example:

- Deeper sensor integration and calibration.
- Telemetry, networking, and link reliability tuning.
- Onboard companion-computer setup and software deployment.
- Software-in-the-Loop (SITL)-first mission development and sim-to-real deployment workflow.
- Autopilot reconfiguration for another vehicle class (for example, rover) to understand what transfers and what changes.
- Custom 3D-printed parts and mounting for cleaner integration and maintainability.
- Lower-level control-loop tuning and optimization.
- Faster debugging and troubleshooting habits.
- Clear documentation and reproducible setup steps.

Add or revise these as the group aligns on interests.
The group should also aim to execute an autonomous task or mission that participants are excited about and can plan and work toward together.

## Using This Site Together

This site can also serve as a shared place to organize what the study circle learns, not only as a finished course handout.

Participants can help in whatever way is comfortable:

- Point out when an instruction or a general step in the build, run, or operate process is unclear.
- Add notes from build sessions, including what worked, what failed, and what should be tried next.
- Share photos, observations, troubleshooting steps, or useful links.
- Suggest new sections or pages that would help organize topics the group wants to understand.
- Use GitHub issues or pull requests if that workflow is comfortable; otherwise share feedback through the group and it can be folded into the site.

Small observations are useful. A quick note about where someone got stuck can help make the course clearer and easier to repeat.

## Expectations

- No prior drone-building or programming experience is required.
- Regular participation across the study circle period.
- Willingness to engage in hands-on technical work and troubleshooting.
- Participants should feel empowered to help shape priorities so the study circle stays interesting and aligned with group goals.
