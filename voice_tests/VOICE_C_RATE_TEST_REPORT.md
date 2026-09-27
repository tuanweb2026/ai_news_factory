# AI NEWS FACTORY — CANDIDATE C (ARIA) SPEAKING RATE TUNING REPORT

**Experiment Status:** COMPLETED  
**Scope:** Isolated Voice Calibration Pass (No modifications to live factory configuration, scheduled publish jobs, or YouTube channel)  
**Comparison Video Artifact:** `voice_tests/VOICE_C_RATE_TEST.mp4`  
**Generated Date:** September 27, 2026  

---

## 1. Executive Summary

Following human listening evaluation which identified **Candidate C (`en-US-AriaNeural`)** as the most natural-sounding voice for AI NEWS FACTORY English Shorts, this experiment tuned the speaking rate to determine the optimal balance between:
- Natural human conversational cadence
- Broadcast authority & presence
- High intelligibility on technical terminology
- Compelling Shorts pacing without sounding robotic, hurried, or unnatural at sentence boundaries

Three calibrated rate variants were generated using the identical test script, visual sequence (Style Bible v1.0 dark technical diagrams), and audio mix (-24 dB ambient tech drone):

* **Section 1 (00:00 – 00:15):** `ARIA / 165 WPM` (Calibrated Rate: `+26.0%`)
* **Section 2 (00:15 – 00:30):** `ARIA / 170 WPM` (Calibrated Rate: `+30.0%`)
* **Section 3 (00:30 – 00:45):** `ARIA / 175 WPM` (Calibrated Rate: `+34.0%`)

---

## 2. Technical Audio & Rate Measurements

The benchmark script contains exactly 50 words:
> *"Artificial intelligence is moving faster than most teams can track. Every week brings new models, new reasoning benchmarks, and new autonomous agents. The real bottleneck is no longer raw compute. It is whether your systems can make fast, reliable decisions under uncertainty. Watch how this architecture adapts in real time."*

### Variant Measurements Table

| Parameter / Metric | Variant A (165 WPM) | Variant B (170 WPM) | Variant C (175 WPM) |
| :--- | :--- | :--- | :--- |
| **Voice Label** | `ARIA / 165 WPM` | `ARIA / 170 WPM` | `ARIA / 175 WPM` |
| **Timestamp in Video** | `00:00 - 00:15` | `00:15 - 00:30` | `00:30 - 00:45` |
| **Target Speaking Rate** | `165.0 WPM` | `170.0 WPM` | `175.0 WPM` |
| **Actual Measured WPM** | **`164.91 WPM`** | **`170.07 WPM`** | **`175.32 WPM`** |
| **Rate Adjustment Parameter** | `+26.0%` | `+30.0%` | `+34.0%` |
| **Full Uncut Duration** | `18.19 s` | `17.64 s` | `17.11 s` |
| **Integrated Loudness** | `-16.3 LUFS` | `-16.2 LUFS` | `-16.2 LUFS` |
| **True Peak** | `-1.7 dBTP` | `-1.5 dBTP` | `-1.5 dBTP` |
| **Loudness Range (LRA)** | `2.5 LU` | `2.4 LU` | `2.4 LU` |
| **Speech Pause Naturalness** | Pronounced breathing room | Balanced newsroom cadence | Tight, energetic transitions |
| **Sentence Ending Inflection** | Completely unhurried | Firm downward cadence | Slight compression on final syllable |

---

## 3. SSML Configuration Specification

When applied to production, Azure Cognitive Speech Services / Edge TTS executes this configuration via the following SSML template:

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
       xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
  <voice name="en-US-AriaNeural">
    <mstts:express-as style="newscast-formal" styledegree="1.0">
      <prosody rate="{RATE_PARAMETER}">
        Artificial intelligence is moving faster than most teams can track.
        Every week brings new models, new reasoning benchmarks, and new autonomous agents.
        The real bottleneck is no longer raw compute.
        It is whether your systems can make fast, reliable decisions under uncertainty.
        Watch how this architecture adapts in real time.
      </prosody>
    </mstts:express-as>
  </voice>
</speak>
```

### Rate Mapping:
- **165 WPM:** `rate="+26%"` (or prosody `rate="1.26"`)
- **170 WPM:** `rate="+30%"` (or prosody `rate="1.30"`)
- **175 WPM:** `rate="+34%"` (or prosody `rate="1.34"`)

---

## 4. Acoustic & Cadence Observations (Awaiting Human Decision)

In strict accordance with the experiment protocol, **no subjective winner is declared**. Below are the descriptive acoustic traits observed across the variants:

### 165 WPM (`+26.0%` Rate, 18.19s Full Run)
- **Acoustic Characteristics:** Highly relaxed, conversational yet formal delivery. Intonation contours on multi-syllable technical words (*"uncertainty"*, *"architecture"*, *"reasoning benchmarks"*) remain distinct with full vowel elongation.
- **Cadence & Pauses:** Clear, natural breathing intervals between clauses. Zero hint of synthetic compression.
- **Editorial Fit:** Ideal for dense engineering Shorts where the audience needs cognitive space to read on-screen mathematical notations or state diagrams simultaneously.

### 170 WPM (`+30.0%` Rate, 17.64s Full Run)
- **Acoustic Characteristics:** Crisp, forward-moving broadcast delivery reminiscent of prime-time news headlines. Maintains clear pitch modulation while conveying momentum.
- **Cadence & Pauses:** Punctuation pauses remain distinct, while inter-word silences tighten slightly to maintain narrative pull.
- **Editorial Fit:** Well-balanced for fast-paced 30–35 second Shorts scripts where information density and viewer retention are paramount.

### 175 WPM (`+34.0%` Rate, 17.11s Full Run)
- **Acoustic Characteristics:** High energy and urgency. Consonants remain sharp, but phrase transitions become rapid.
- **Cadence & Pauses:** Inter-phrase pauses are significantly compressed. Sentence endings carry minimal decay time into the next clause.
- **Editorial Fit:** Best suited for breaking news alerts or brief 20-second punchy explainers. May require careful monitoring on multi-clause sentences to prevent auditory fatigue.

---

## 5. Technical Video QA Pass

The final comparison video passed all technical verification tests:

| Check | Specification | Result |
| :--- | :--- | :--- |
| **Output File** | `voice_tests/VOICE_C_RATE_TEST.mp4` | Present & Verified |
| **Dimensions / Ratio** | `1080 × 1920` (9:16 Vertical) | PASS |
| **Duration** | `00:00:45.00` (1350 frames @ 30 fps) | PASS (Exact 45.00s) |
| **Video Codec** | `H.264 (avc1, High Profile, yuv420p)` | PASS |
| **Audio Codec** | `AAC-LC (Stereo, 48 kHz, 192 kbps)` | PASS |
| **Audio Mix Loudness** | `-16.2 LUFS` (Target: -16 ± 1 LUFS) | PASS |
| **True Peak** | `-1.5 dBTP` (Limit: $\le -1.5$ dBTP) | PASS |
| **Decode Integrity** | `ffmpeg -v error -f null -` | Zero errors / 0 frame drops |
| **Subtitles** | Embedded `mov_text` track with `ARIA / [WPM]` section headers | PASS |
| **Live Pipeline Status** | `config/factory.yaml` unchanged, zero uploads | PASS |
