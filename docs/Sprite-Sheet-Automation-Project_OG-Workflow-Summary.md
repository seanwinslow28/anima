## **Sprite-Sheet-Automation-Project\_2026 — Original Workflow Summary**

### **What It Is**

A **Manifest-Driven CLI Pipeline** that automates generating, auditing, retrying, packing, and validating AI-generated pixel art sprite sheets for 16BitFit Battle Mode — a 2D fighting game with 12 fighters in Street Fighter II style.

### **The Core Loop (7 Steps)**

The entire system follows one repeatable flow:

1. **CLI Command** → You run `pipeline:run` and point it at a `manifest.yaml` file. The manifest is the single source of truth — it defines the character, animation, frame count, quality thresholds, prompt templates, and export settings.  
2. **Orchestrator** → The central state machine initializes a `RunState`, locks the configuration into `manifest.lock.json`, and begins coordinating everything. It never talks to external tools directly — it delegates to Adapters.  
3. **Generator Adapter** → Calls Nano Banana Pro (Gemini) to produce frame candidates. Frame 0 uses the character's **anchor sprite** as a reference. Frames 1+ chain from the previously approved frame to maintain temporal consistency.  
4. **Auditor** → Each candidate frame is immediately evaluated against two tiers of quality checks:  
   * **Hard Fails (HF01–HF05):** Blocking. Wrong dimensions, missing alpha, baseline drift \>1px, naming errors, or gross anatomy failures \= instant reject.  
   * **Soft Fails (SF01–SF05):** Non-blocking but trigger retries. Identity drift (DINO/SSIM), palette drift, line weight inconsistency, temporal coherence issues, alpha halos.  
5. **RetryManager** → If a frame fails, it climbs a **Retry Ladder** with bounded attempts:  
   * Attempt 1: Edit from anchor (re-ground identity)  
   * Attempt 2: Re-anchor from original reference  
   * Attempt 3: Tighten prompt constraints  
   * Attempt 4: **Stop** with a diagnostic report explaining what failed and why  
6. **Packer Adapter** → All approved frames are sent to **TexturePacker CLI**, which compiles them into an atlas (`atlas.png` \+ `atlas.json`) with locked settings (trim, extrude, padding, no rotation).  
7. **Validator Adapter** → The atlas is loaded into a **headless Phaser 3** instance (via Puppeteer) that runs micro-tests: pivot/origin behavior, trim jitter/baseline stability, and naming key conventions. **Engine truth is the final arbiter** — if Phaser says it jitters, it fails regardless of what metrics said.

### **Technology Stack (and Why)**

| Tech | Role | Why This Choice |
| ----- | ----- | ----- |
| **Node.js (v20+)** | Runtime | Best ecosystem support for CLI tools and image processing libraries |
| **TypeScript 5.x** | Language | Strict type safety prevents bugs in complex state management (the pipeline has a lot of moving parts) |
| **Oclif 4.x** | CLI Framework | Purpose-built for Node CLIs — handles argument parsing, plugin architecture, and command organization out of the box |
| **Zod** | Validation | Validates manifest YAML and external data at runtime (catches config errors before they cause silent failures) |
| **Pino** | Logging | Outputs structured JSON logs — machine-readable for debugging, not just human-readable text |
| **Execa** | Subprocess calls | Safely executes external CLI tools (TexturePacker, Gemini CLI) with proper escaping across Windows/Mac/Linux |
| **Sharp** | Image processing | Fast Node.js library for normalizing, resizing, and analyzing images during auditing |
| **Puppeteer Core** | Headless browser | Launches real Chrome to run Phaser in a true WebGL context, so validation matches actual game behavior |

### **Architecture Pattern: Hexagonal (Ports & Adapters)**

The key design decision is that **core logic never touches external tools directly**. Every external dependency (Gemini, TexturePacker, Phaser) is wrapped in an **Adapter** that implements a typed interface. This means:

* You can swap Gemini for ComfyUI or OpenAI later without rewriting the pipeline  
* You can swap TexturePacker for Aseprite  
* You can swap Phaser for another engine  
* The audit/retry/orchestration logic stays stable regardless

### **MVP Scope**

The MVP was intentionally minimal — **1 Champion × 2 animations (Idle \+ Walk)**:

* **Idle (4 frames):** Validates identity consistency, palette, alpha handling with minimal motion  
* **Walk (6–8 frames):** Stress-tests temporal coherence and baseline stability in a looping cycle

The goal wasn't to generate the full roster — it was to **prove the system is trustworthy** before scaling. If the loop works reliably for Idle \+ Walk, it scales to everything else.

### **Key Artifacts Per Run**

Every run produces a deterministic folder structure:

* `manifest.lock.json` — Frozen config snapshot  
* `state.json` — Atomically persisted pipeline state (resumable)  
* `audit/audit_log.jsonl` — Every frame evaluation  
* `audit/run_summary.json` — Aggregate stats (retry rate, reject rate, top failure codes)  
* `artifacts/frame_###/candidates/` — All generated candidates  
* `export/atlas.png` \+ `atlas.json` — Final packed sprite sheet  
* `validation/results.json` — Phaser test results

### **The "Engine Truth" Principle**

This is the project's north star: **if it plays cleanly in Phaser, it ships. If metrics say "pass" but the animation jitters in-engine, it fails.** The pipeline treats AI output as raw material to be validated — not final product. Phaser is the regulator.

