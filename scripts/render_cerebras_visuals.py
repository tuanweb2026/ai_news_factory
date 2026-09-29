#!/usr/bin/env python3
"""Renders high-density technical visual frames for Cerebras Systems & Gimlet Labs Short in strict compliance with
Anti-Black-Void Gate and Visual Style Bible v1.0.
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
ASSETS_DIR = Path("data/visuals/production_assets_cerebras")
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Colors
BG_BASE = (7, 10, 15)
CYAN_GLOW = (14, 27, 44)
VIOLET_GLOW = (22, 19, 42)
GRID_COLOR = (20, 30, 44)
GRID_TICK = (35, 55, 80)
TEXT_WHITE = (243, 247, 250)
TEXT_MUTED = (139, 152, 167)
ACCENT_CYAN = (77, 235, 255)
ACCENT_VIOLET = (155, 124, 255)
ACCENT_GREEN = (84, 227, 154)
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

font_title_lg = get_font(FONT_BOLD, 52)
font_title_md = get_font(FONT_BOLD, 40)
font_sub = get_font(FONT_BOLD, 30)
font_body = get_font(FONT_REG, 24)
font_tag = get_font(FONT_BOLD, 22)
font_mono_sm = get_font(FONT_MONO, 20)
font_mono_md = get_font(FONT_MONO, 24)

def create_base_canvas(glow_color=(14, 27, 44), glow_center=(540, 960), glow_radius=750):
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
    # Header tag pill
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
# SHOT 01: 3,000 Tokens/Sec Speed Shock
# ==========================================
def render_shot_01():
    img, draw = create_base_canvas(glow_color=CYAN_GLOW, glow_center=(540, 940))
    draw_title_card(draw, "SPEED BREAKTHROUGH", ACCENT_CYAN, "3,000 TOKENS / SEC", "ULTRAFAST INFERENCE ENGINE")
    
    # Diagram Area Y: 460 to 1420
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=(10, 15, 23), outline=CARD_BORDER, width=2)
    draw.text((100, 490), "INFERENCE THROUGHPUT COMPARISON", font=font_mono_md, fill=ACCENT_CYAN)

    bars = [
        {"label": "Standard GPU Inference", "speed": "100 tok/s", "val": 120, "col": TEXT_MUTED, "y": 570, "sub": "Traditional memory bandwidth bottleneck"},
        {"label": "Optimized GPU Speculative", "speed": "350 tok/s", "val": 280, "col": ACCENT_AMBER, "y": 780, "sub": "HBM3e memory access limits"},
        {"label": "Cerebras CS-4 on Gimlet Cloud", "speed": "3,000 tok/s", "val": 740, "col": ACCENT_CYAN, "y": 990, "sub": "Wafer-Scale SRAM: 30x throughput surge"},
    ]

    for b in bars:
        y = b["y"]
        draw.rounded_rectangle([100, y, W - 100, y + 175], radius=14, fill=CARD_BG, outline=b["col"], width=2)
        draw.text((130, y + 20), b["label"], font=font_title_md, fill=TEXT_WHITE)
        draw.text((W - 280, y + 20), b["speed"], font=font_title_md, fill=b["col"])
        draw.text((130, y + 70), b["sub"], font=font_body, fill=TEXT_MUTED)
        # Background bar
        draw.rounded_rectangle([130, y + 115, W - 130, y + 145], radius=8, fill=(20, 28, 40))
        # Active bar
        draw.rounded_rectangle([130, y + 115, 130 + b["val"], y + 145], radius=8, fill=b["col"])

    # Multiplier callout badge
    draw.rounded_rectangle([160, 1220, W - 160, 1380], radius=16, fill=(18, 32, 48), outline=ACCENT_GREEN, width=3)
    draw.text((200, 1245), "⚡ 30x SPEED ADVANTAGE", font=font_title_md, fill=ACCENT_GREEN)
    draw.text((200, 1305), "Enables fluid voice, video synthesis & multi-agent swarms.", font=font_body, fill=TEXT_WHITE)

    draw_footer_card(draw, "INSTANTANEOUS MULTI-AGENT INFERENCE AT SCALE")
    img.save(ASSETS_DIR / "shot-01.png")
    print("Saved shot-01.png")

# ==========================================
# SHOT 02: 100MW Deal & Infrastructure
# ==========================================
def render_shot_02():
    img, draw = create_base_canvas(glow_color=VIOLET_GLOW, glow_center=(540, 940))
    draw_title_card(draw, "INFRASTRUCTURE CONTRACT", ACCENT_VIOLET, "CEREBRAS & GIMLET LABS", "100 MEGAWATT POWER DEAL")
    
    # Diagram Area Y: 460 to 1420
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=(10, 15, 23), outline=CARD_BORDER, width=2)
    draw.text((100, 490), "STRATEGIC INFRASTRUCTURE DEPLOYMENT", font=font_mono_md, fill=ACCENT_CYAN)

    # 100MW Center Badge
    draw.rounded_rectangle([180, 560, W - 180, 710], radius=16, fill=(24, 18, 42), outline=ACCENT_VIOLET, width=3)
    draw.text((220, 585), "100 MEGAWATTS COMMITTED", font=font_title_md, fill=ACCENT_VIOLET)
    draw.text((220, 645), "Dedicated high-speed wafer compute over next 1–2 years.", font=font_body, fill=TEXT_WHITE)

    # Two Hub Boxes
    draw.rounded_rectangle([110, 750, 510, 970], radius=14, fill=CARD_BG, outline=ACCENT_CYAN, width=2)
    draw.text((140, 780), "CEREBRAS CS-4", font=font_title_md, fill=ACCENT_CYAN)
    draw.text((140, 835), "• Wafer Scale Engine", font=font_body, fill=TEXT_WHITE)
    draw.text((140, 875), "• 44GB On-Chip SRAM", font=font_body, fill=TEXT_WHITE)
    draw.text((140, 915), "• 21 PB/s Memory Bandwidth", font=font_mono_sm, fill=TEXT_MUTED)

    draw.rounded_rectangle([570, 750, 970, 970], radius=14, fill=CARD_BG, outline=ACCENT_VIOLET, width=2)
    draw.text((600, 780), "GIMLET CLOUD", font=font_title_md, fill=ACCENT_VIOLET)
    draw.text((600, 835), "• Disaggregated Stack", font=font_body, fill=TEXT_WHITE)
    draw.text((600, 875), "• Low-Latency Routing", font=font_body, fill=TEXT_WHITE)
    draw.text((600, 915), "• Enterprise API Tier", font=font_mono_sm, fill=TEXT_MUTED)

    # Connecting bus line
    draw.line([(510, 860), (570, 860)], fill=ACCENT_AMBER, width=6)

    # Rollout timeline
    draw.rounded_rectangle([110, 1020, W - 110, 1380], radius=14, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((140, 1050), "DEPLOYMENT ROADMAP", font=font_sub, fill=TEXT_WHITE)
    
    phases = [
        ("PHASE 1 (Late 2026)", "First Cerebras-powered Gimlet Cloud datacenter online", ACCENT_GREEN),
        ("PHASE 2 (2027)", "Broad global platform availability for enterprise workloads", ACCENT_CYAN),
        ("WORKLOADS", "Real-time Voice AI, Video Generation, Agent Swarms & Finance", ACCENT_AMBER),
    ]
    for idx, (p_title, p_desc, p_col) in enumerate(phases):
        py = 1110 + idx * 80
        draw.ellipse([140, py + 12, 156, py + 28], fill=p_col)
        draw.text((170, py + 8), p_title, font=font_mono_sm, fill=p_col)
        draw.text((400, py + 8), p_desc, font=font_body, fill=TEXT_WHITE)

    draw_footer_card(draw, "MASSIVE COMPUTE INFRASTRUCTURE FOR THE AGENTIC ERA")
    img.save(ASSETS_DIR / "shot-02.png")
    print("Saved shot-02.png")

# ==========================================
# SHOT 03: CS-4 Wafer Scale Engine Blueprint
# ==========================================
def render_shot_03():
    img, draw = create_base_canvas(glow_color=CYAN_GLOW, glow_center=(540, 940))
    draw_title_card(draw, "HARDWARE BLUEPRINT", ACCENT_CYAN, "CEREBRAS CS-4 WAFER", "WAFER SCALE ENGINE ARCHITECTURE")
    
    # Diagram Area Y: 460 to 1420
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=(10, 15, 23), outline=CARD_BORDER, width=2)
    draw.text((100, 490), "SILICON DIE SIZE COMPARISON (TRUE SCALE)", font=font_mono_md, fill=ACCENT_CYAN)

    # Giant Wafer Square / Circle
    wx, wy = 360, 930
    w_size = 460
    # Outer wafer circle
    draw.ellipse([wx - w_size//2, wy - w_size//2, wx + w_size//2, wy + w_size//2], outline=(30, 55, 80), width=3)
    # Wafer die grid
    draw.rounded_rectangle([wx - 190, wy - 190, wx + 190, wy + 190], radius=16, fill=(15, 28, 42), outline=ACCENT_CYAN, width=3)
    for i in range(-150, 160, 40):
        draw.line([(wx + i, wy - 190), (wx + i, wy + 190)], fill=(25, 45, 65), width=1)
        draw.line([(wx - 190, wy + i), (wx + 190, wy + i)], fill=(25, 45, 65), width=1)
        
    draw.text((wx - 140, wy - 30), "CEREBRAS WSE", font=font_title_md, fill=TEXT_WHITE)
    draw.text((wx - 120, wy + 20), "46,225 mm² DIE", font=font_sub, fill=ACCENT_CYAN)

    # Tiny GPU Die Comparison
    gx, gy = 820, 930
    draw.rounded_rectangle([gx - 45, gy - 45, gx + 45, gy + 45], radius=6, fill=(24, 18, 30), outline=ACCENT_AMBER, width=2)
    draw.text((gx - 35, gy - 12), "GPU", font=font_sub, fill=ACCENT_AMBER)
    draw.text((gx - 80, gy + 65), "814 mm² DIE", font=font_mono_sm, fill=TEXT_MUTED)
    draw.text((gx - 110, gy + 95), "(Conventional GPU)", font=font_body, fill=TEXT_MUTED)

    # Specs Card
    draw.rounded_rectangle([100, 1190, W - 100, 1390], radius=14, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((130, 1215), "TECHNICAL SPECIFICATIONS", font=font_sub, fill=TEXT_WHITE)
    specs = [
        "• On-Chip SRAM: 44 Gigabytes (Zero off-chip HBM bottlenecks)",
        "• Memory Bandwidth: 21 Petabytes / second",
        "• Eliminates inter-chip interconnect latency completely",
    ]
    for idx, s in enumerate(specs):
        draw.text((130, 1260 + idx * 38), s, font=font_body, fill=ACCENT_CYAN if idx == 0 else TEXT_MUTED)

    draw_footer_card(draw, "DINNER-PLATE-SIZED CHIP ELIMINATES MEMORY BOTTLENECKS")
    img.save(ASSETS_DIR / "shot-03.png")
    print("Saved shot-03.png")

# ==========================================
# SHOT 04: Disaggregated Inference Pipeline
# ==========================================
def render_shot_04():
    img, draw = create_base_canvas(glow_color=CYAN_GLOW, glow_center=(540, 940))
    draw_title_card(draw, "SYSTEM ARCHITECTURE", ACCENT_AMBER, "DISAGGREGATED COMPUTE", "GPU PREFILL • WAFER DECODE")
    
    # Diagram Area Y: 460 to 1420
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=(10, 15, 23), outline=CARD_BORDER, width=2)
    draw.text((100, 490), "TWO-STAGE HYBRID INFERENCE PIPELINE", font=font_mono_md, fill=ACCENT_CYAN)

    # Stage 1: Prefill on GPUs
    draw.rounded_rectangle([110, 560, W - 110, 770], radius=16, fill=CARD_BG, outline=ACCENT_AMBER, width=2)
    draw.rounded_rectangle([140, 580, 460, 625], radius=8, fill=(35, 25, 15), outline=ACCENT_AMBER, width=1)
    draw.text((155, 590), "STAGE 1: PREFILL PHASE", font=font_mono_sm, fill=ACCENT_AMBER)
    draw.text((140, 645), "Handled by NVIDIA GPU Clusters", font=font_title_md, fill=TEXT_WHITE)
    draw.text((140, 700), "Optimized for dense matrix computations & prompt ingestion.", font=font_body, fill=TEXT_MUTED)

    # Transfer Arrow
    draw.line([(540, 770), (540, 860)], fill=ACCENT_GREEN, width=4)
    draw.polygon([(525, 855), (555, 855), (540, 880)], fill=ACCENT_GREEN)
    draw.text((560, 810), "Ultra-Low Latency KV-Cache Transfer", font=font_mono_sm, fill=ACCENT_GREEN)

    # Stage 2: Decode on Cerebras WSE
    draw.rounded_rectangle([110, 880, W - 110, 1090], radius=16, fill=(16, 28, 44), outline=ACCENT_CYAN, width=3)
    draw.rounded_rectangle([140, 900, 460, 945], radius=8, fill=(18, 38, 55), outline=ACCENT_CYAN, width=1)
    draw.text((155, 910), "STAGE 2: DECODE STREAM", font=font_mono_sm, fill=ACCENT_CYAN)
    draw.text((140, 965), "Powered by Cerebras CS-4 WSE", font=font_title_md, fill=TEXT_WHITE)
    draw.text((140, 1020), "3,000 tokens/sec continuous generation without queue stalls.", font=font_body, fill=ACCENT_GREEN)

    # Efficiency Benefit Box
    draw.rounded_rectangle([110, 1130, W - 110, 1380], radius=14, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((140, 1160), "ARCHITECTURAL ADVANTAGES", font=font_sub, fill=TEXT_WHITE)
    advantages = [
        "✓ Maximum hardware efficiency: GPUs do prefill, WSE does decode",
        "✓ Lowest cost-per-token for high-concurrency agent swarms",
        "✓ Sub-second full response time for complex reasoning chains",
    ]
    for idx, adv in enumerate(advantages):
        draw.text((140, 1210 + idx * 48), adv, font=font_body, fill=TEXT_WHITE if idx == 0 else TEXT_MUTED)

    draw_footer_card(draw, "OPTIMAL HARDWARE SPECIALIZATION FOR AI INFERENCE")
    img.save(ASSETS_DIR / "shot-04.png")
    print("Saved shot-04.png")

# ==========================================
# SHOT 05: Brand CTA Lockup
# ==========================================
def render_shot_05():
    img, draw = create_base_canvas(glow_color=CYAN_GLOW, glow_center=(540, 940))
    draw_title_card(draw, "AI NEWS FACTORY", ACCENT_CYAN, "VERIFIED AI SHORTS", "DAILY PRODUCTION PIPELINE")
    
    # Diagram Area Y: 460 to 1420
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=(10, 15, 23), outline=CARD_BORDER, width=2)
    
    # Glowing Shield Center
    cx, cy = 540, 800
    for r in [260, 200, 140]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(30, 50, 75), width=2)
        
    draw.polygon([
        (cx, cy - 120),
        (cx + 110, cy - 60),
        (cx + 110, cy + 50),
        (cx, cy + 130),
        (cx - 110, cy + 50),
        (cx - 110, cy - 60),
    ], fill=(16, 28, 44), outline=ACCENT_CYAN)
    
    # Checkmark inside shield
    draw.line([(cx - 40, cy), (cx - 10, cy + 35)], fill=ACCENT_GREEN, width=8)
    draw.line([(cx - 10, cy + 35), (cx + 45, cy - 35)], fill=ACCENT_GREEN, width=8)
    
    draw.text((cx - 160, cy + 170), "VERIFIED FACTUAL", font=font_title_md, fill=TEXT_WHITE)
    draw.text((cx - 140, cy + 225), "14-GATE RED TEAM PASS", font=font_mono_md, fill=ACCENT_CYAN)

    specs = [
        "PRIMARY SOURCE: CEREBRAS OFFICIAL & GLOBENEWSWIRE",
        "DATE OF RECORD: SEPTEMBER 28, 2026",
        "SPEED VERIFIED: UP TO 3,000 TOKENS / SECOND",
    ]
    for idx, s in enumerate(specs):
        sy = 1110 + idx * 80
        draw.rounded_rectangle([120, sy, W - 120, sy + 60], radius=10, fill=CARD_BG, outline=(30, 45, 65), width=1)
        draw.ellipse([145, sy + 22, 160, sy + 37], fill=ACCENT_CYAN)
        draw.text((180, sy + 18), s, font=font_mono_sm, fill=TEXT_WHITE)

    draw_footer_card(draw, "SUBSCRIBE @LIDO_AI_LAB FOR DAILY FACTUAL AI UPDATES")
    img.save(ASSETS_DIR / "shot-05.png")
    print("Saved shot-05.png")

if __name__ == "__main__":
    render_shot_01()
    render_shot_02()
    render_shot_03()
    render_shot_04()
    render_shot_05()
    print("All 5 Cerebras frames rendered successfully.")
