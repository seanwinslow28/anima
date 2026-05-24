# Executive Summary

- **Top pick:** A hybrid pipeline combining a small **LoRA** on our 30 keyframes with a lightweight **adapter** (PuLID or PhotoMaker) plus ControlNet poses, all on Z-Image Turbo or FLUX. This yields high fidelity + style consistency at moderate cost.  
- **Fast & flexible:** Adapter-only methods (e.g. PhotoMaker or InstantID + ControlNet on FLUX/Z-Image) require no training; very quick to iterate but give only medium likeness (ID score ≈3–4/5) and often prefer photoreal style over pencil.  
- **High-fidelity:** Training a character **LoRA** (FLUX or Z-Image Turbo) from the 30 keyframes locks identity firmly (ID score ≈4–5/5), but costs hours on a 4090. Z-Image Turbo LoRAs need very few images (~10–15)【5†L1-L5】【68†L60-L68】 and run in ~11–16 GB, rivaling FLUX/SDXL quality.  
- **Style preservation:** Pure adapters (IP-Adapter, InstantID, PuLID) often “photorealize” the face and can look pasted-on if lighting or style differs【43†L37-L45】【54†L110-L119】. Composing a **style LoRA** (trained on pencil sketches) plus the character LoRA in the stack is key for hand-drawn look.  
- **In-between frames:** Specialized tools like **ComfyUI’s ToonCrafter** or the Frame-Interpolation plugin (RIFE, FILM, etc.) can smoothly interpolate between keyframes while keeping style【74†L319-L327】【79†】. New unified models (Lance/Janus2) can do image editing, but aren’t purpose-built for style-locked interpolation yet.

