## Task: Sprite Transformation Sequence (F24-F28)

You are working on the Pencil Test animation pipeline at:
/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline

**Start by reading these files in this order:**
1. `docs/production-checklist.md` — current production status
2. `CLAUDE.md` — project manual, pipeline architecture, skills map
3. `CHANGELOG.md` — decision history and prompt engineering lessons learned
4. `docs/pencil-test-storyboard.md` — lines 35-52 (Beat 2: The Draw)

**Context:** Act 1 keyframes are complete. F18 shows Sean mid-gesture with his
right arm swept forward holding a stylus, pencil trail lines arcing behind it.
F31 shows Sean looking at an RPG warrior sprite sitting on his shoulder. The
missing piece is the TRANSITION — frames F24-F28 where the pencil trail lines
from F18's gesture resolve and transform into the RPG warrior sprite character.

**The approved assets you'll work with:**
- `runs/run_2026-04-04_174805/approved/PT_A1_F18_key.png` — the gesture frame 
  with pencil trail (Sean holds this pose through F18-F30)
- `runs/run_2026-04-04_174805/candidates/sprite/turnaround_01.png` — RPG warrior
  sprite turnaround sheet (5 views)
- `runs/run_2026-04-04_174805/candidates/sprite/concept_B.png` — sprite standing
- `runs/run_2026-04-04_174805/candidates/sprite/seated_sprite_01.png` — sprite 
  seated (the pose it lands in on Sean's shoulder)
- `images/2D-Character-Sketch-Sean-v1.png` — A-2 anchor

**What to create:** A sequence of 4-5 overlay images showing pencil marks
clustering and transforming into the RPG warrior sprite. These are transparent
overlays composited on top of Sean's F18 hold pose. The storyboard describes:
- F24: Trailing pencil marks cluster and start to take shape
- F26: Shape resolves into recognizable sprite silhouette  
- F28: Sprite fully formed, does a small bounce (squash/stretch)

**Use these skills:**
- `gemini-pencil-animation-image-gen` — for generating each transformation frame
- `image-generator-prompt-science` — 7-Layer framework for the prompts
- `2d-animation-principles` — squash/stretch on the bounce, timing/spacing

**Key creative constraint:** The style shift from loose pencil marks to a 
recognizable blocky RPG sprite character is the hero moment of Act 1. The
pencil marks should feel like they're being "drawn into existence." The sprite
should emerge from the pencil energy, not just appear.

**Output:** Individual PNG frames for the transformation sequence, plus updated
production-checklist.md marking Phase 3 progress.

**Important lessons from CHANGELOG.md to apply:**
- Use the turnaround sheet as reference for sprite identity, but add "ONE 
  drawing on the page" constraint to prevent turnaround bleed
- Pencil test style: warm gray graphite on cream paper, NOT black ink
- All frames should be 1376x768 (16:9) to match the approved keyframes
