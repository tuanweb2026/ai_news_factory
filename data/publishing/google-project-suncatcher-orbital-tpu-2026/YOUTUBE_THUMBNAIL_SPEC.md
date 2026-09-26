# YOUTUBE THUMBNAIL & COVER SPECIFICATION
**Story ID:** `google-project-suncatcher-orbital-tpu-2026`  
**Video File:** `final_release_candidate.mp4` (Do NOT re-render; video file remains untouched)  
**Format Specs:** 9:16 Vertical Cover (1080x1920) + 16:9 Standard YouTube Preview Crop (1920x1080)  

---

## 1. Creative Strategy & Design Principles

YouTube Shorts thumbnails appear in:
1. **Shorts Grid / Feed:** Native 9:16 vertical portrait view.
2. **Channel Page & Search Results:** Centered square (1:1) or horizontal (16:9) crops.

To maximize mobile readability without clickbait deception:
- **Maximum Text Length:** 3–4 words in ultra-bold sans-serif (`Inter` or `Space Grotesk`).
- **High Contrast:** Titanium and dark CFRP satellite chassis with glowing cyan circuitry against the blackness of space and the luminous blue arc of Earth's atmosphere.
- **No Deceptive Imagery:** No massive fictional orbital death stars, flying servers, or fake Google login screens. The spacecraft depicted must faithfully match the Planet Labs MVP satellite bus architecture established in `SATELLITE_MASTER_DESIGN`.

---

## 2. Thumbnail Concept Specifications

| Specification Field | Production Value |
| :--- | :--- |
| **Recommended Headline Text** | **`AI TPUs IN ORBIT?`** *(Alternative: `TESTING TPUs IN SPACE`)* |
| **Word Count** | **4 words** (Strictly within the 4–5 word maximum) |
| **Badge / Subtext** | `RESEARCH PROTOTYPE` *(rendered in mint green #54E39A or cyan #4DEBFF pill badge)* |
| **Visual Composition** | **Foreground (Center-Right):** 3/4 isometric cutaway of the Planet Labs satellite bus, revealing the aluminum cold plate and 4 Trillium TPU dies glowing with subtle cyan circuit traces. Copper heat pipes run to exterior dark radiator fins.<br>**Background (Lower-Left):** Curved Earth limb illuminated by high-contrast dawn-dusk sunlight at the terminator line. Deep cosmic blackness with clean, cold star field above. |
| **Color Palette** | • Canvas / Space: Deep space black (`#070A0F`)<br>• Accents: Electric Cyan (`#4DEBFF`) & Deep Violet (`#9B7CFF`)<br>• Badge: Verified Mint Green (`#54E39A`)<br>• Hardware: Gold Kapton MLI blanket (`#D4AF37`) & Titanium chassis (`#1A2233`) |
| **Safe Zone Rules** | All typography and badges must remain within the central 1080x1080 square to guarantee zero cutoff when cropped to 1:1 or 16:9 in mobile search results. Keep top 15% and bottom 20% clear of critical information. |

---

## 3. Ready-to-Use Asset Frame Extraction (Recommended Default)

If a separate custom thumbnail is not generated, YouTube Studio allows selecting a frame directly from the rendered video.

- **Recommended Master Video Frame:** **`00:09.50` (Shot 03 Cutaway)** or **`00:13.20` (Shot 04 Orbital Mechanics)**.
- **FFmpeg Frame Extraction Command:**
  ```bash
  ffmpeg -ss 00:00:09.500 -i data/rendered/google-project-suncatcher-orbital-tpu-2026/release_candidate_6D/final_release_candidate.mp4 -vframes 1 -q:v 2 data/publishing/google-project-suncatcher-orbital-tpu-2026/thumbnail_cover_frame_shot03.jpg
  ```

---

## 4. Generative AI Prompt (For High-Res 3D Cover Rendering)

If rendering a custom standalone cover image via Midjourney, FLUX, or DALL-E 3:

```text
Vertical 9:16 high-precision aerospace engineering rendering. Detailed cutaway of a modern compact satellite bus (Planet Labs architecture) orbiting in low Earth orbit. The spacecraft chassis features titanium struts, dark carbon-fiber panels, and gold Kapton multi-layer insulation (MLI). An exposed cutaway reveals an aluminum cold plate mounting four Google Trillium TPU semiconductor dies with subtle glowing electric-cyan circuit interconnects. Thick copper heat pipes visibly route thermal energy from the chips to external planar dark radiator panels facing deep space. Below, the curved horizon of planet Earth shines with realistic blue atmospheric rim lighting along the dawn-dusk terminator line. Above is the pitch blackness of space. Highly detailed, photorealistic 3D octane render, 8k resolution, cinematic lighting, zero cartoon effects, zero fantasy spaceships, clean aerospace technical realism.
```

### Negative Prompt:
```text
cartoon, anime, blurry, low resolution, flying servers, giant computer monitor in space, fake google search bar, fantasy spaceship, laser battles, hyperdrive warp glow, distorted text, cheesy subscribe buttons.
```
