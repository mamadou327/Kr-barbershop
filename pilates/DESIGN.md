# Olea Pilates: design notes

## Brief
Fictional reformer Pilates studio (Bermondsey, SE1). A showcase piece for content: the job is to make
someone stop scrolling on a phone and believe the room is real, then book a reformer.
Assumptions: studio, teachers, address and timetable are fictional and marked as such in the footer.

## Concepts considered
| | Idea | Anchor | Signature | O/F/Fe/P |
|---|---|---|---|---|
| A. Material | The site moves like a reformer carriage: drawn out under spring tension, returned with control | reformer springs and carriage | photoreal walk-in film; progress shown as a carriage on a rail with the four spring colours as stops; display type stretches on its width axis and springs back | 4 / 5 / 4 / 2 |
| B. Name | Olea = olive: slow growth, rings, the tree at the end of the room as destination | the name | rings growing as you scroll | 3 / 3 / 4 / 3 |
| C. Formal | Everything on a 4-count breath: in for 4, out for 4 | Pilates breathing | all motion on a 4 s / 8 s cycle | 3 / 4 / 5 / 4 |

Picked **A**. Stole from C for the idle state: the film breathes (scale in 4 s, out 4 s) when the visitor is still.

## Concept card
```
Idea:        The site moves like a reformer: out under tension, back with control.
Metaphor:    a reformer carriage on its rail, springs set by colour.
Signature:   the scroll-scrubbed photoreal walk to reformer 3, with the carriage-on-rail progress.
Emotion:     quiet, warm, expensive; "I want to be in that room at 7:30".
Motion verb: draw and return (long ease-out, controlled settle, never a bounce).
Screenshot:  the turn onto reformer 3 in the glowing mirrors, the rail showing the red stop lit.
```

## System
- Palette (single committed dark theme, the photographs bring the colour):
  ground #11100e (studio before the lights), ink #f1ede6, muted #a8a196, line rgba(241,237,230,.14),
  accent #d4472d (the red spring: used only for "yours" and the active stop), curtain #1b1916.
- Type: Archivo variable (wght 100–900, wdth 62–125). Display: 800, width 112–125, tracking -0.04em.
  Text: 400 at width 100. Meta: 500, width 88, uppercase only for the four spring labels.
  Avoided: cream + serif + terracotta (the previous version leaned that way).
- Grid: 12 columns, gutter clamp(16px, 2vw, 32px). Hang lines: col 1, col 5, col 9.
- Shape: radius 2px on controls only; images square-cornered.
- Motion: one ease, power3.out for entrances and expo.inOut for the carriage; 0.9 s large, 0.45 s small,
  stagger 40 ms. Hover: the label slides out along x and a copy returns from the other side (draw and return).
- Idle: film scale breathes 1.000 ↔ 1.012 on an 8 s cycle; off under reduced motion.

## Sections (each a different family)
1. Full-bleed media: the film, four-corner frame, captions bottom-left as plain display type over a scrim.
2. Statement: one paragraph at t-l across 9 columns.
3. Index list: the four classes as rows (name, length, level, spring dots); pointer preview photo on desktop, inline photo on phones.
4. Asymmetric pair: the olive-tree photograph on 7 columns, facts about the room on 4.
5. Booking: timetable + reformer plan that mirrors the room.
6. Footer finale: OLEA at mega width, address, hours, fictional-studio note.

## Decisions
- Single page (artifact host is one page): no inner page, transition or 404. Noted as a known gap.
- No loader screen: the first frame paints immediately and the rail fills as frames arrive.
