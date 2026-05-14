# Research on prompt structure

## Main finding

The best-supported default for entity["product","Seedance 2.0","ByteDance multimodal video model"] in 2026 is **structured natural language**, not fully machine-like JSON. Across the official material I could retrieve from urlByteDance Seed official pageturn36view0, urlfal.ai Seedance docsturn11view3, and urlDreaminaturn17search2, the prompt is treated as a **text string** that should carry subject, action, camera, lighting, style, references, and sometimes scene cuts or timestamps. I found **no official ByteDance or fal.ai document that explicitly says raw JSON prompts outperform prose** for Seedance. The strongest direct side-by-side Seedance evidence I found says JSON can be more controlled than prose for complex multi-beat scenes, but that same source also says dense JSON can perform worse than bullets and recommends drafting in bullets first. citeturn11view2turn11view3turn18view2turn6view1turn6view3

For your use case—**start+end frame interpolation for hand-drawn pencil tests**—the evidence points even more strongly toward **labeled blocks or timecoded beats** rather than full JSON. Official Seedance image-to-video docs describe the prompt as a text description of the desired motion, and ByteDance ecosystem guidance for image-to-video warns that the scene is already present in the source image, so static content should be minimized or avoided. In practice, that means your prompt should mostly describe **motion arc, timing, camera behavior, and preservation constraints**, not restate the drawing. citeturn11view3turn12search4turn18view2

My recommendation is therefore: **keep your current labeled-block direction, tighten it, and only promote to minimal JSON when you need programmatic generation or many reusable fields.** Confidence: **medium**. The official evidence for structured prose is strong; the direct evidence that JSON itself is superior is real but much thinner and mostly third-party. citeturn11view3turn6view1turn6view3turn37view0

## Direct Seedance evidence

The official Seedance interfaces consistently present prompting as **natural-language direction with optional structure**, not as a privileged JSON schema. The official Seed page says the model gives “full control over performance, lighting, shadow, and camera movement.” fal’s official Seedance docs define `prompt` as a required **string**, describe reference prompting with `@Image1`, `@Video1`, and `@Audio1`, and say the prompt “supports scene cuts and timestamps for pacing control.” The same fal prompt guide recommends a simple anatomy: **“Subject + Action + Camera + Scene/Lighting + Style”**, with a target length of **50–150 words**. Dreamina’s official usage flow is similarly plain-language: “Describe the scene, action, and mood in the prompt box,” and it also markets the model as able to turn “a single sentence” into a complete video. That is strong evidence that Seedance’s native prompt interface expects **structured prose**, optionally segmented, rather than raw JSON as a special mode. citeturn36view0turn11view2turn11view3turn18view1turn18view2turn18view3

Just as important: the API wrapper being JSON does **not** mean the prompt dialect itself is JSON. fal’s REST example uses `Content-Type: application/json`, but the actual prompt remains a plain string such as “A spear-wielding warrior clashes…” Inside the schema, the model input is still `prompt: string`, not `prompt: object`. So there is a crucial distinction between **JSON as transport format** and **JSON as generation prompt style**. The official docs support the former; they do not explicitly endorse the latter. citeturn11view0turn11view2turn11view3

The strongest direct Seedance comparison I found is Micheal Lanham’s April 2026 side-by-side article comparing the **same scene** written as plain prose, timeline bullets, and JSON. His reporting is unusually concrete: the prose version was described as atmospheric but loose, the bullet version as tighter in timing, and the JSON version as the most controlled, with audio and lighting tracking the timeline more reliably. But the same article also gives the clearest warning against over-structuring: “Twenty is usually too many,” referring to JSON keys, and it explicitly recommends **draft in bullets, promote to JSON if the shot grows**. This is the best direct evidence I found that JSON can help on Seedance—but only in a narrow way: multi-beat, multi-parameter control, especially when you need reusable structure. citeturn5view0turn6view1turn6view2turn6view3

Other Seedance-specific 2026 guides converge on the same broader lesson without requiring JSON. urlMindStudiohttps://www.mindstudio.ai says the difference between mediocre and cinematic output “usually comes down to one thing: structure,” and argues that image-prompt-like dense paragraphs often yield something “narratively inert,” while timeline prompting with timestamps and camera directions gives Seedance the temporal structure it needs. urlHiggsfieldhttps://higgsfield.ai says “always specify your shot structure upfront” and recommends numbering shots individually for the highest-performing formats. Both are basically arguing for **labeled shot grammar**, not for JSON specifically. citeturn37view0turn37view1

The weaker social evidence is contradictory. A search-engine snippet from an urlXhttps://x.com post claimed “Seedance 2.0 works better with JSON prompts,” while a snippet from fal’s X highlights reportedly said “Use shot lists with timecodes, not prose.” Meanwhile, an indexed Reddit thread complained that some models ignore instructions “timestamps or not, JSON scripts or not.” Because these are snippets and casual community commentary rather than retrievable, controlled comparisons, I would treat them as **signal of debate**, not decision-grade proof. citeturn20search20turn20search33turn24search1

No direct evidence found from public, citation-grade archives of the fal.ai or BytePlus Discord communities specifically answering **JSON vs prose for Seedance**. I also did not find timestamp-verifiable YouTube transcript evidence strong enough to count in the final recommendation.

## ByteDance ecosystem evidence

The broader ByteDance ecosystem reinforces the same pattern: **componentized natural language beats unstructured prose, but official docs still stop short of recommending raw JSON.** In the Seedance 1.5 official prompt-guide snippet on urlVolcengine docshttps://www.volcengine.com, the prompt formula is given as **subject + motion + environment + camera/cut + aesthetic description + sound**. The English BytePlus/ModelArk Seedance 2.0 prompt-guide snippet says the prompt should clearly specify the reference object and can include advanced instructions like lighting details, visual style, and ambient sound effects. Dreamina’s own UI guidance is even simpler: scene, action, mood. All three are examples of **labeled ingredients inside natural language**, not a model-specific JSON schema. citeturn12search0turn15search21turn17search0turn18view2

For image-to-video specifically, the ByteDance ecosystem gives a strong clue that matters for your workflow. The official Seedance-1.0-lite prompt-guide snippet says image-to-video “already has the scene,” so users should reduce or even avoid describing static content. That maps closely to start+end frame interpolation: the frames already provide composition, style, staging, and much of the identity. The prompt’s job is to control **what changes between them**. This is a direct reason to avoid giant style paragraphs or duplicate JSON fields that merely restate what the frames already show. citeturn12search4turn11view3

The same ecosystem also warns about prompt density. The official Seedance 2.0 API reference snippet on Volcengine recommends keeping Chinese prompts under 500 characters and English prompts under 1000 words, warning that overly long prompts can scatter information and cause the model to ignore details. fal’s official Seedance guide is even tighter, recommending 50–150 words for standard prompting. Those guardrails point away from bloated schemas, repeated fields, or JSON-inside-prose unless the added structure is buying you real control. citeturn12search8turn11view3

Dreamina’s marketing language also matters here. It repeatedly frames Seedance as able to convert “a single sentence” into a complete video and tells users to “define your vision with prompts” by describing scene, action, and mood. That is not proof that short prose is always best; it is proof that inside ByteDance’s own product layer, **the intended user-facing contract is plain language with optional structure**, not rigid machine syntax. citeturn18view1turn18view2turn18view3

No direct evidence found in ByteDance’s public 2026 materials that **YAML** has any special advantage for Seedance.

## Adjacent Chinese model evidence

Across adjacent Chinese video models, the recurring winning pattern is **cinematic shot structure plus motion language**, not raw JSON. The most explicit example is the 2026 fal guide for entity["product","Kling 3.0","AI video model"]. It says Kling performs best when prompts are written “like directions to a scene,” urges users to “think in shots, not clips,” and says multi-shot prompts should label each shot’s framing, subject, and motion instead of compressing everything into one paragraph. It reports that well-structured shot prompts produce smoother transitions and more intentional cinematic flow. That is very close to the Seedance-specific evidence from MindStudio and Higgsfield, which makes the pattern fairly transferable. citeturn37view2turn37view0turn37view1

For entity["product","MiniMax-Hailuo-02","MiniMax video model"], the official MiniMax docs show a different flavor of structure: **inline command syntax**. The first-and-last-frame API supports `[commands]` for camera movement control inside the prompt, and the official Hailuo prompt guide says “simple language beats fancy writing every time” and advises ordering information by importance. That is not JSON, but it is still structured direction. In other words, Hailuo’s official guidance also prefers **lightweight syntax over dense narrative prose**. citeturn29search7turn29search0

Official entity["software","Vidu","AI video generation platform"] materials tell the same story from the image-to-video side. Vidu’s workflow articles say the prompt should function as a **movement instruction**, note that English is often more accurate for motion prompting, and give examples that focus on what moves and how. Vidu’s reference-to-video FAQ also emphasizes references for controlling identity, style, camera movement, and scene continuity, and its tools mention using frames to guide motion “from start to finish.” Again, the transferable lesson is to let the **images carry appearance** and let the prompt carry **motion and timing**. citeturn28view2turn27search20turn27search15

Taken together, the adjacent-Chinese-model evidence is supportive but not dispositive. It does **not** prove that JSON is neutral or harmful on Seedance. It does show that the broader Chinese video-model ecosystem in 2025–2026 repeatedly converged on **shot lists, command tags, timestamps, and motion-first prompting** rather than on deeply nested JSON as the default human authoring format. citeturn37view2turn29search7turn29search0turn28view2

## Western model baseline

The Western baseline points in the same direction. Official urlOpenAIhttps://openai.com guidance for entity["product","Sora 2","OpenAI video model"] says a good prompt should read “as if you were sketching it onto a storyboard.” It recommends stating camera framing, depth of field, action beats, lighting, and palette, and says that if you describe multiple shots in one prompt, each shot block should stay distinct. Crucially, OpenAI separates **prompt content** from **API parameters**: resolution and duration belong in the API call, while the prompt controls subject, motion, lighting, and style. That is a strong null-hypothesis baseline for Seedance: structured prose with clear shot blocks is normal across top video models. citeturn35view0turn35view1

Official urlGoogle DeepMindhttps://deepmind.google guidance for entity["product","Veo 3.1","Google video model"] is similarly explicit. Google’s Vertex AI docs define an “anatomy of a Veo prompt,” say that “breaking your idea down into key components is the most effective way” to guide generation, and offer a five-part formula: **cinematography + subject + action + context + style & ambiance**. The DeepMind prompt guide also tells users to define visual style and tone first, then fuse visuals with sound design. Again, this is highly structured, but still human-readable prose rather than JSON. citeturn32view1turn32view2turn32view0

Official urlRunwayhttps://runwayml.com docs for entity["product","Runway Gen-3 Alpha","Runway video model"] are even more direct about wording. The Gen-3 Alpha prompt guide says prompts should be direct and easily understood, “descriptive, not conversational or command-based,” and most effective when they separate scene, subject, and camera movement into a clear structure. Runway’s newer Academy guide for image-to-video says the prompt’s role is to describe **motion, camera work, and temporal progression**, and that users should not re-describe the content already present in the image. Gen-3 documentation is older and therefore somewhat stale relative to Runway’s current Gen-4.5 product line, but the motion-first principle carries through in the newer Academy material. citeturn34view0turn34view1turn34view2

So the Western baseline does **not** show a different world where JSON is the obvious best practice. If anything, it strengthens the case that the default best practice in 2025–2026 video generation was **structured prose with shot grammar**, while JSON mostly acted as an optional authoring or automation layer. citeturn35view0turn32view1turn34view0

## Patterns that help and fail

### What seems to help

For **one clear beat** in image-to-video, concise prose is still the best-supported default. That matches official Seedance examples that use a single prompt string to describe motion, and it matches Dreamina’s plain-language UI. For your pencil-test use case, a production-safe version would look like this:

```text
A rough pencil-test character in the start frame eases into the end pose. Subtle graphite boil, one controlled blink, torso leads the turn, hand settles last. Locked camera. Preserve rough line quality and timing-chart feel. No cleanup, no color fill, no extra fingers, no anatomy drift.
```

This is not copied from a source verbatim; it is an evidence-based synthesis of Seedance’s official motion-string design, Dreamina’s scene/action/mood guidance, and ByteDance’s advice not to re-describe static image content in image-to-video. citeturn11view3turn18view2turn12search4

For **two to four beats inside one generation**, labeled blocks or timestamps are the strongest fit. That aligns with the direct Seedance evidence from MindStudio and Higgsfield, and it also matches the best direct A/B comparison I found, where the bullet/timeline version was tighter than prose. A start+end interpolation version for your workflow would look like this:

```text
FORMAT: start+end frame interpolation, 6s, 16:9

MOTION ARC
0–2s: ease out of the start pose; shoulders initiate the turn; slight graphite boil
2–4s: right hand arrives first; head follows with a delayed blink
4–6s: settle into the end pose; tiny overshoot, then recover

CAMERA
locked-off frame, no lens change, no push-in

STYLE
preserve rough pencil texture, exposed construction lines, uneven graphite density

CONSTRAINTS
no cleanup into painted animation, no extra limbs, no face redesign, no line melting
```

The important point here is not the exact wording. It is that the structure maps one beat to one time range and lets the model focus on **temporal progression** instead of decoding a long paragraph full of mixed instructions. citeturn37view0turn37view1turn6view3

For **reusable multi-shot templates**, minimal JSON can make sense. The Lanham side-by-side comparison is the clearest direct Seedance evidence that JSON can deliver the most control when multiple dimensions—camera, lighting, audio, shot order, constraints—must stay aligned across several beats. But the JSON has to stay sparse. A practical pattern would be:

```json
{
  "subject": "same character as start and end frames",
  "timeline": [
    {"t": "0-2s", "action": "ease out of start pose"},
    {"t": "2-4s", "action": "head turn completes, hand settles"},
    {"t": "4-6s", "action": "stabilize into end pose"}
  ],
  "camera": "locked-off",
  "style": "rough pencil test, graphite boil preserved",
  "constraints": ["no cleanup", "no anatomy drift", "no extra limbs"]
}
```

On the direct Seedance evidence, this kind of JSON is most defensible when you need **reusable fields** or **programmatic prompt generation**, not when a human is just trying to author a normal shot fast. citeturn6view1turn6view2turn6view3

### What seems to fail

The clearest failure pattern is **dense paragraph prose for multi-beat shots**. In direct Seedance reporting, prose tended to blend multiple beats together; MindStudio says image-prompt-style dense descriptions often produce clips that are technically competent but narratively flat. If the clip needs discrete timing, plain prose is the wrong shape. citeturn6view3turn37view0

The second failure pattern is **over-structured JSON**. The best direct Seedance JSON advocate I found also warns against it: once decorative keys pile up, performance degrades. That warning is consistent with official ByteDance/fal guidance on prompt length and information overload. JSON is not magic; it is only helpful if each field carries unique, load-bearing control. citeturn6view1turn12search8turn11view3

The third failure pattern, and the one most relevant to you, is **double-encoding the frames**. ByteDance ecosystem guidance for image-to-video says the scene is already in the input image, so static description should be minimized; Runway’s image-to-video docs say almost the same thing. For start+end interpolation, that means a long block restating pose, costume, composition, line quality, background layout, and mood is often wasted prompt budget unless one of those elements actually needs to change. citeturn12search4turn34view1

For **JSON-inside-prose** and **YAML vs JSON on Seedance specifically**, no direct evidence found. My own inference is that both are risky whenever they increase prompt length without adding new motion or continuity information, but that inference comes from the overload and double-encoding evidence above. It is **not** backed by a direct Seedance A/B test.

## Recommendation

Use **labeled blocks or timecoded structured prose** as your production default for entity["product","Seedance 2.0","ByteDance multimodal video model"], especially for start+end frame interpolation and hand-drawn pencil tests. That recommendation is the most directly supported by the official Seedance interfaces, the ByteDance ecosystem’s image-to-video guidance, and the strongest 2026 Seedance-specific secondary guides. It fits the model’s documented support for timestamps, scene cuts, and `@reference` syntax, while avoiding the specific image-to-video mistake of re-describing what the frames already provide. citeturn11view3turn18view2turn12search4turn37view0turn37view1

Use **full JSON only as a second-tier format** when one of three things is true: you are generating prompts programmatically, you need many reusable fields across related shots, or you have a complex multi-beat scene where camera, sound, lighting, and transitions must all stay independently editable. If you go this route, keep the JSON **minimal**. The direct Seedance evidence supports JSON as a control scaffold, not as a license to write giant schemas. citeturn6view1turn6view2turn6view3

So the practical answer to your actual decision is:

**Choose labeled blocks over full JSON as the default Seedance template.**  
**Add timestamps when the shot has multiple beats.**  
**Reserve minimal JSON for reusable, programmatic, or unusually complex prompts.**

Confidence is **medium** because the official evidence for structured prose is strong, but the official evidence for **JSON superiority** is basically absent, and the direct Seedance A/B evidence for JSON comes mostly from one well-documented but still third-party source. On the evidence currently available, your current v3 direction looks **closer to the likely optimum** than a jump to all-JSON. citeturn11view3turn18view2turn12search4turn6view1turn6view3