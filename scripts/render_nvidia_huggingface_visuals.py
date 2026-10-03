#!/usr/bin/env python3
"""Renders high-density technical visual frames for NVIDIA Hugging Face Acquisition Short
in strict compliance with Anti-Black-Void Gate and Visual Style Bible v1.0.
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
ASSETS_DIR = Path("data/visuals/production_assets_nvidia_huggingface")
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Colors
BG_BASE = (7, 10, 15)
NVIDIA_GREEN = (118, 185, 0)
HUGGING_YELLOW = (255, 210, 30)
GRID_COLOR = (20, 30, 44)
GRID_TICK = (35, 55, 80)
TEXT_WHITE = (243, 247, 250)
TEXT_MUTED = (139, 152, 167)
ACCENT_CYAN = (77, 235, 255)
ACCENT_VIOLET = (155, 124, 255)
ACCENT_AMBER = (255, 184, 77)
ACCENT_RED = (255, 92, 112)
CARD_BG = (13, 18, 26)
CARD_BORDER = (30, 45, 65)

# Fonts
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_MONO = "/System/Library/Fonts/SFNSMono.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

font_title_lg = get_font(FONT_BOLD, 44)
font_title_md = get_font(FONT_BOLD, 36)
font_sub = get_font(FONT_BOLD, 28)
font_body = get_font(FONT_REG, 24)
font_tag = get_font(FONT_BOLD, 22)
font_mono_sm = get_font(FONT_MONO, 20)
font_mono_md = get_font(FONT_MONO, 24)

def create_base_canvas(glow_color=(15, 35, 20), glow_center=(540, 960), glow_radius=750):
    img = Image.new("RGB", (W, H), BG_BASE)
    draw = ImageDraw.Draw(img)
    
    # 1. Radial depth glow
    cx, cy = glow_center
    for r in range(glow_radius, 60, -35):
        alpha = math.sin((r / glow_radius) * (math.pi / 2))
        inv_alpha = 1.0 - alpha
        cur_color = (
            int(BG_BASE[0] * alpha + glow_color[0] * inv_alpha * 2.8),
            int(BG_BASE[1] * alpha + glow_color[1] * inv_alpha * 2.8),
            int(BG_BASE[2] * alpha + glow_color[2] * inv_alpha * 2.8),
        )
        cur_color = tuple(min(255, max(0, c)) for c in cur_color)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=cur_color)
        
    # 2. Technical coordinate grid
    for x in range(0, W, 80):
        draw.line([(x, 0), (x, H)], fill=GRID_COLOR, width=1)
    for y in range(0, H, 80):
        draw.line([(0, y), (W, y)], fill=GRID_COLOR, width=1)
        
    # Grid intersection ticks
    for x in range(80, W, 160):
        for y in range(80, H, 160):
            draw.line([(x - 6, y), (x + 6, y)], fill=GRID_TICK, width=1)
            draw.line([(x, y - 6), (x, y + 6)], fill=GRID_TICK, width=1)

    # 3. Top Banner
    draw.rounded_rectangle([70, 90, W - 70, 180], radius=14, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.rounded_rectangle([90, 108, 380, 162], radius=10, fill=(18, 35, 55), outline=ACCENT_CYAN, width=1)
    draw.ellipse([110, 130, 122, 142], fill=ACCENT_CYAN)
    draw.text((135, 122), "AI NEWS FACTORY", font=font_tag, fill=TEXT_WHITE)
    draw.text((W - 390, 124), "VERIFIED INTELLIGENCE", font=font_mono_sm, fill=ACCENT_CYAN)
    
    return img, draw

def draw_title_card(draw, badge_text, badge_color, headline, subtitle):
    draw.rounded_rectangle([70, 220, W - 70, 420], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.rounded_rectangle([100, 245, 100 + len(badge_text) * 14 + 40, 285], radius=8, fill=(20, 30, 42), outline=badge_color, width=1)
    draw.text((120, 252), badge_text, font=font_tag, fill=badge_color)
    draw.text((100, 300), headline, font=font_title_lg, fill=TEXT_WHITE)
    draw.text((100, 365), subtitle, font=font_sub, fill=ACCENT_CYAN)

def draw_footer_card(draw, text):
    draw.rounded_rectangle([70, 1460, W - 70, 1560], radius=14, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((100, 1495), text, font=font_sub, fill=TEXT_MUTED)

# ==========================================
# SHOT 01: NVIDIA Buys Hugging Face: $12.9B
# ==========================================
def render_shot_01():
    img, draw = create_base_canvas(glow_color=(20, 45, 15), glow_center=(540, 800))
    draw_title_card(draw, "LANDMARK ACQUISITION", NVIDIA_GREEN, "NVIDIA BUYS HUGGING FACE", "$12.9 Billion Open-Source Deal")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "STRATEGIC MERGER SPECIFICATION", font=font_tag, fill=ACCENT_CYAN)
    
    # Valuation Metric Hero
    draw.rounded_rectangle([110, 540, W - 110, 780], radius=16, fill=(16, 28, 20), outline=NVIDIA_GREEN, width=2)
    draw.text((140, 570), "$12,900,000,000 USD", font=font_title_lg, fill=NVIDIA_GREEN)
    draw.text((140, 640), "Definitive Cash & Stock Acquisition Agreement", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 695), "Largest open-source AI platform transaction in history", font=font_mono_sm, fill=ACCENT_CYAN)

    # Entity Cards Side-by-Side
    # NVIDIA
    draw.rounded_rectangle([110, 820, 510, 1370], radius=14, fill=(14, 22, 16), outline=NVIDIA_GREEN, width=2)
    draw.text((140, 850), "NVIDIA", font=font_title_md, fill=NVIDIA_GREEN)
    draw.text((140, 910), "AI Silicon Leader", font=font_tag, fill=TEXT_MUTED)
    draw.text((140, 980), "• CUDA Architecture", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 1040), "• TensorRT Engine", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 1100), "• Blackwell Ultra GPUs", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 1160), "• Global Cloud Compute", font=font_sub, fill=TEXT_WHITE)

    # Hugging Face
    draw.rounded_rectangle([570, 820, W - 110, 1370], radius=14, fill=(24, 22, 14), outline=HUGGING_YELLOW, width=2)
    draw.text((600, 850), "HUGGING FACE", font=font_title_md, fill=HUGGING_YELLOW)
    draw.text((600, 910), "Open-Source Hub", font=font_tag, fill=TEXT_MUTED)
    draw.text((600, 980), "• 1.5M Open Models", font=font_sub, fill=TEXT_WHITE)
    draw.text((600, 1040), "• 300K Datasets", font=font_sub, fill=TEXT_WHITE)
    draw.text((600, 1100), "• Transformers Lib", font=font_sub, fill=TEXT_WHITE)
    draw.text((600, 1160), "• Global Dev Community", font=font_sub, fill=TEXT_WHITE)

    draw_footer_card(draw, "Unifies leading AI silicon hardware with global open model registry")
    img.save(ASSETS_DIR / "shot_01.png")
    print("Rendered shot_01.png")

# ==========================================
# SHOT 02: 1.5M Models • 300K Datasets
# ==========================================
def render_shot_02():
    img, draw = create_base_canvas(glow_color=(30, 35, 15), glow_center=(540, 850))
    draw_title_card(draw, "GLOBAL ECOSYSTEM SCALE", HUGGING_YELLOW, "1.5M MODELS • 300K DATASETS", "The Epicenter of Open-Source AI")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "HUGGING FACE REPOSITORY STATS", font=font_tag, fill=ACCENT_CYAN)
    
    metrics = [
        ("1,540,000+", "Open AI Models", HUGGING_YELLOW),
        ("310,000+", "Public Datasets", ACCENT_CYAN),
        ("45,000,000+", "Monthly Active Devs", NVIDIA_GREEN),
    ]
    for i, (val, lbl, col) in enumerate(metrics):
        sy = 540 + i * 260
        draw.rounded_rectangle([110, sy, W - 110, sy + 220], radius=16, fill=(18, 24, 30), outline=col, width=2)
        draw.text((140, sy + 30), val, font=font_title_lg, fill=col)
        draw.text((140, sy + 105), lbl, font=font_title_md, fill=TEXT_WHITE)
        draw.text((140, sy + 160), "Decentralized open weights across vision, language, & robotics", font=font_body, fill=TEXT_MUTED)

    draw_footer_card(draw, "Powers over 80% of open-source research and commercial deployment")
    img.save(ASSETS_DIR / "shot_02.png")
    print("Rendered shot_02.png")

# ==========================================
# SHOT 03: Compute Neutrality Pledged
# ==========================================
def render_shot_03():
    img, draw = create_base_canvas(glow_color=(15, 35, 45), glow_center=(540, 900))
    draw_title_card(draw, "OPEN SOURCE PROTECTION", ACCENT_CYAN, "COMPUTE NEUTRALITY PLEDGED", "Full Multi-Hardware Ecosystem Support")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "BINDING COMMITMENT MATRIX", font=font_tag, fill=ACCENT_CYAN)
    
    hardware_list = [
        ("AMD Instinct & ROCm", "First-class compilation & benchmark support", NVIDIA_GREEN),
        ("Intel Gaudi & Xe", "Complete open model serving integration", NVIDIA_GREEN),
        ("Apple Silicon (Metal/MPS)", "On-device Mac & iPad inference acceleration", NVIDIA_GREEN),
        ("Google TPU & Cloud TPUs", "Continuous JAX & PyTorch-XLA compatibility", NVIDIA_GREEN),
    ]
    for i, (hw, desc, col) in enumerate(hardware_list):
        sy = 540 + i * 190
        draw.rounded_rectangle([110, sy, W - 110, sy + 155], radius=14, fill=(18, 25, 35), outline=CARD_BORDER, width=2)
        draw.text((140, sy + 25), hw, font=font_title_md, fill=TEXT_WHITE)
        draw.text((140, sy + 80), desc, font=font_sub, fill=ACCENT_CYAN)
        draw.rounded_rectangle([W - 320, sy + 30, W - 140, sy + 75], radius=8, fill=(18, 45, 25), outline=NVIDIA_GREEN, width=1)
        draw.text((W - 295, sy + 40), "SUPPORTED", font=font_tag, fill=NVIDIA_GREEN)

    draw_footer_card(draw, "CEO Jensen Huang & Clement Delangue guarantee open hardware choice")
    img.save(ASSETS_DIR / "shot_03.png")
    print("Rendered shot_03.png")

# ==========================================
# SHOT 04: Silicon Meets Open Weights
# ==========================================
def render_shot_04():
    img, draw = create_base_canvas(glow_color=(25, 35, 15), glow_center=(540, 850))
    draw_title_card(draw, "VERTICAL INTEGRATION", NVIDIA_GREEN, "SILICON MEETS OPEN WEIGHTS", "The Unified AI Computing Stack")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "END-TO-END ACCELERATION STACK", font=font_tag, fill=ACCENT_CYAN)
    
    stack_layers = [
        ("Level 4: Autonomous Agents", "Enterprise workflows, multi-agent swarms", ACCENT_AMBER),
        ("Level 3: Open Weights Hub", "Hugging Face Models, Datasets, & Spaces", HUGGING_YELLOW),
        ("Level 2: Software & Runtimes", "CUDA, TensorRT-LLM, vLLM, PyTorch", ACCENT_CYAN),
        ("Level 1: Hardware Accelerators", "Blackwell, Grace Hopper, Quantum-X Networks", NVIDIA_GREEN),
    ]
    for i, (title, desc, col) in enumerate(stack_layers):
        sy = 540 + i * 200
        draw.rounded_rectangle([110, sy, W - 110, sy + 165], radius=16, fill=(16, 24, 28), outline=col, width=2)
        draw.text((140, sy + 30), title, font=font_title_md, fill=col)
        draw.text((140, sy + 90), desc, font=font_sub, fill=TEXT_WHITE)

    draw_footer_card(draw, "Seamlessly optimizes open AI models for next-generation silicon architectures")
    img.save(ASSETS_DIR / "shot_04.png")
    print("Rendered shot_04.png")

# ==========================================
# SHOT 05: Official AI News Factory Lockup
# ==========================================
def render_shot_05():
    img, draw = create_base_canvas(glow_color=(25, 20, 50), glow_center=(540, 960), glow_radius=850)
    
    # Central Logo Box
    cx, cy = 540, 750
    for r in range(320, 80, -25):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(30 + r//8, 45 + r//7, 95 + r//5), width=2)
        
    draw.rounded_rectangle([200, 620, W - 200, 880], radius=24, fill=CARD_BG, outline=ACCENT_CYAN, width=3)
    draw.text((240, 660), "AI NEWS FACTORY", font=font_title_lg, fill=TEXT_WHITE)
    draw.text((310, 740), "DAILY VERIFIED INTELLIGENCE", font=font_tag, fill=ACCENT_CYAN)
    draw.text((275, 800), "youtube.com/@lidoailab", font=font_mono_md, fill=ACCENT_VIOLET)
    
    # CTA Card
    draw.rounded_rectangle([110, 1050, W - 110, 1380], radius=20, fill=(18, 25, 38), outline=CARD_BORDER, width=2)
    draw.text((150, 1090), "STAY AHEAD OF FRONTIER AI", font=font_tag, fill=ACCENT_AMBER)
    draw.text((150, 1145), "SUBSCRIBE FOR DAILY BREAKTHROUGHS", font=font_title_md, fill=TEXT_WHITE)
    draw.text((150, 1220), "• Silicon & model infrastructure news", font=font_sub, fill=TEXT_WHITE)
    draw.text((150, 1270), "• Independent technical verification", font=font_sub, fill=TEXT_WHITE)
    draw.text((150, 1320), "• Zero hype, 100% provenance", font=font_sub, fill=NVIDIA_GREEN)

    draw_footer_card(draw, "Follow @lidoailab for daily autonomous AI intelligence")
    img.save(ASSETS_DIR / "shot_05.png")
    print("Rendered shot_05.png")

def main():
    print("Rendering NVIDIA Hugging Face Visual Frames...")
    render_shot_01()
    render_shot_02()
    render_shot_03()
    render_shot_04()
    render_shot_05()
    print("All 5 visual frames rendered successfully!")

if __name__ == "__main__":
    main()
