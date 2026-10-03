#!/usr/bin/env python3
"""Renders high-density technical visual frames for OpenAI GPT-6 Sol & Luna Short
in strict compliance with Anti-Black-Void Gate and Visual Style Bible v1.0.
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
ASSETS_DIR = Path("data/visuals/production_assets_gpt6_sol_luna")
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

font_title_lg = get_font(FONT_BOLD, 44)
font_title_md = get_font(FONT_BOLD, 36)
font_sub = get_font(FONT_BOLD, 28)
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
# SHOT 01: GPT-6 Sol & Luna Unveiled
# ==========================================
def render_shot_01():
    img, draw = create_base_canvas(glow_color=(35, 25, 15), glow_center=(540, 800))
    draw_title_card(draw, "OPENAI FRONTIER EXPANSION", ACCENT_AMBER, "GPT-6 SOL & LUNA UNVEILED", "Specialized Autonomous Agent Lineup")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "GPT-6 MODEL FAMILY EXPANSION", font=font_tag, fill=ACCENT_CYAN)
    
    # Dual Model Cards
    # Sol Card
    draw.rounded_rectangle([110, 540, W - 110, 930], radius=16, fill=(20, 26, 38), outline=ACCENT_AMBER, width=2)
    draw.text((140, 570), "GPT-6 SOL • CLOUD ACCELERATOR", font=font_title_md, fill=ACCENT_AMBER)
    draw.text((140, 630), "• 4x Faster Token Generation Throughput", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 685), "• 65% Lower Enterprise Operating Cost", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 740), "• High-throughput API for Autonomous Agents", font=font_sub, fill=ACCENT_CYAN)
    draw.text((140, 795), "• Optimized for complex cloud browser tasks", font=font_sub, fill=TEXT_MUTED)
    draw.text((140, 855), "TARGET: Enterprise Agent Swarms", font=font_tag, fill=ACCENT_AMBER)

    # Luna Card
    draw.rounded_rectangle([110, 970, W - 110, 1370], radius=16, fill=(24, 18, 38), outline=ACCENT_VIOLET, width=2)
    draw.text((140, 1000), "GPT-6 LUNA • ON-DEVICE NPU", font=font_title_md, fill=ACCENT_VIOLET)
    draw.text((140, 1060), "• Local Quantized Neural Network", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 1115), "• Sub-10ms UI Frame Perception", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 1170), "• 100% On-Device Screen Privacy (Zero Cloud Leak)", font=font_sub, fill=ACCENT_GREEN)
    draw.text((140, 1225), "• Air-gapped enterprise compliance", font=font_sub, fill=TEXT_MUTED)
    draw.text((140, 1285), "TARGET: Real-Time Desktop OS Control", font=font_tag, fill=ACCENT_VIOLET)

    draw_footer_card(draw, "Dual-engine architecture dividing cloud reasoning and local perception")
    img.save(ASSETS_DIR / "shot_01.png")
    print("Rendered shot_01.png")

# ==========================================
# SHOT 02: Purpose-Built for Agents
# ==========================================
def render_shot_02():
    img, draw = create_base_canvas(glow_color=(15, 35, 45), glow_center=(540, 850))
    draw_title_card(draw, "AUTONOMOUS OS CONTROL", ACCENT_CYAN, "PURPOSE-BUILT FOR AGENTS", "Browser Automation & System Control Loop")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "AGENTIC CLOSED-LOOP WORKFLOW", font=font_tag, fill=ACCENT_CYAN)
    
    # Workflow Loop Diagram
    steps = [
        ("1. Screen Ingestion", "Luna processes 60 FPS desktop pixels via local NPU", ACCENT_VIOLET),
        ("2. DOM & UI Parsing", "Identifies buttons, forms, terminal prompts", ACCENT_CYAN),
        ("3. Action Planning", "Sol evaluates multi-step task execution graph", ACCENT_AMBER),
        ("4. System Execution", "Dispatches clicks, keystrokes, API calls safely", ACCENT_GREEN),
    ]
    for i, (stitle, sdesc, col) in enumerate(steps):
        sy = 540 + i * 190
        draw.rounded_rectangle([110, sy, W - 110, sy + 155], radius=14, fill=(18, 24, 34), outline=col, width=2)
        draw.text((140, sy + 25), stitle, font=font_title_md, fill=col)
        draw.text((140, sy + 80), sdesc, font=font_sub, fill=TEXT_WHITE)
        draw.text((W - 220, sy + 30), f"PHASE {i+1}", font=font_mono_sm, fill=col)

    draw_footer_card(draw, "Zero latency UI feedback loop engineered for autonomous software agents")
    img.save(ASSETS_DIR / "shot_02.png")
    print("Rendered shot_02.png")

# ==========================================
# SHOT 03: 4x Faster • 65% Cheaper Benchmark
# ==========================================
def render_shot_03():
    img, draw = create_base_canvas(glow_color=(15, 45, 25), glow_center=(540, 900))
    draw_title_card(draw, "PERFORMANCE & COST BENCHMARKS", ACCENT_GREEN, "4X FASTER • 65% CHEAPER", "Efficiency Gains vs GPT-6 Astra")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "ENTERPRISE WORKFLOW TELEMETRY", font=font_tag, fill=ACCENT_CYAN)
    
    # Throughput Card
    draw.rounded_rectangle([110, 540, W - 110, 920], radius=16, fill=(16, 25, 22), outline=ACCENT_GREEN, width=2)
    draw.text((140, 570), "TOKEN GENERATION THROUGHPUT", font=font_title_md, fill=ACCENT_GREEN)
    
    # Bar Chart: Astra vs Sol
    draw.text((140, 630), "GPT-6 Astra (Baseline): 65 tokens/sec", font=font_sub, fill=TEXT_MUTED)
    draw.rounded_rectangle([140, 670, 380, 710], radius=8, fill=(35, 45, 55))
    
    draw.text((140, 740), "GPT-6 Sol: 260 tokens/sec (4.0x Speedup)", font=font_sub, fill=ACCENT_GREEN)
    draw.rounded_rectangle([140, 780, W - 160, 830], radius=8, fill=ACCENT_GREEN)
    draw.text((W - 240, 792), "400%", font=font_mono_md, fill=BG_BASE)
    
    draw.text((140, 860), "Optimized speculative decoding + distillation", font=font_mono_sm, fill=TEXT_WHITE)

    # Cost Card
    draw.rounded_rectangle([110, 960, W - 110, 1370], radius=16, fill=(28, 20, 20), outline=ACCENT_RED, width=2)
    draw.text((140, 990), "API INFERENCE COST REDUCTION", font=font_title_md, fill=ACCENT_AMBER)
    
    draw.text((140, 1050), "GPT-6 Astra: $15.00 / 1M tokens", font=font_sub, fill=TEXT_MUTED)
    draw.rounded_rectangle([140, 1090, W - 160, 1130], radius=8, fill=(55, 35, 35))
    
    draw.text((140, 1160), "GPT-6 Sol: $5.25 / 1M tokens (-65% Cost)", font=font_sub, fill=ACCENT_AMBER)
    draw.rounded_rectangle([140, 1200, 420, 1250], radius=8, fill=ACCENT_AMBER)
    draw.text((320, 1212), "35%", font=font_mono_md, fill=BG_BASE)
    
    draw.text((140, 1290), "Unlocks continuous 24/7 background agent execution", font=font_mono_sm, fill=TEXT_WHITE)

    draw_footer_card(draw, "Dramatically lowers economic barriers for enterprise automation swarms")
    img.save(ASSETS_DIR / "shot_03.png")
    print("Rendered shot_03.png")

# ==========================================
# SHOT 04: On-Device NPU • Zero Data Leak
# ==========================================
def render_shot_04():
    img, draw = create_base_canvas(glow_color=(30, 15, 45), glow_center=(540, 850))
    draw_title_card(draw, "HARDWARE PRIVACY SHIELD", ACCENT_VIOLET, "ON-DEVICE NPU • ZERO LEAK", "Local Real-Time Screen Vision Analysis")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "LOCAL HARDWARE ISOLATION ARCHITECTURE", font=font_tag, fill=ACCENT_CYAN)
    
    # Chip Box
    draw.rounded_rectangle([110, 540, W - 110, 960], radius=16, fill=(18, 16, 28), outline=ACCENT_VIOLET, width=2)
    draw.text((140, 570), "SILICON NPU DIE • QUANTIZED LUNA", font=font_title_md, fill=ACCENT_VIOLET)
    
    # Visual Air-Gap Shield
    cx, cy = 540, 770
    draw.ellipse([cx - 130, cy - 130, cx + 130, cy + 130], fill=(26, 22, 42), outline=ACCENT_VIOLET, width=3)
    draw.text((cx - 85, cy - 25), "NPU CORE", font=font_title_md, fill=ACCENT_GREEN)
    draw.text((cx - 75, cy + 25), "LUNA ENGINE", font=font_mono_sm, fill=TEXT_WHITE)
    
    draw.rounded_rectangle([140, 890, 420, 930], radius=8, fill=(15, 40, 20), outline=ACCENT_GREEN, width=1)
    draw.text((160, 900), "LOCAL MEMORY ONLY", font=font_tag, fill=ACCENT_GREEN)
    
    draw.rounded_rectangle([W - 440, 890, W - 140, 930], radius=8, fill=(45, 15, 20), outline=ACCENT_RED, width=1)
    draw.text((W - 410, 900), "NO CLOUD UPLOAD", font=font_tag, fill=ACCENT_RED)

    # 3 Security Points
    sec_points = [
        ("Zero Pixel Transmission", "Screenshots never leave local device memory", ACCENT_GREEN),
        ("Sub-10ms Inference", "Direct silicon acceleration eliminates API roundtrip", ACCENT_CYAN),
        ("HIPAA & SOC-2 Compliance", "Enterprise air-gapped data protection standard", ACCENT_VIOLET),
    ]
    for i, (title, desc, col) in enumerate(sec_points):
        sy = 1000 + i * 125
        draw.rounded_rectangle([110, sy, W - 110, sy + 105], radius=12, fill=(16, 20, 30), outline=CARD_BORDER, width=2)
        draw.text((140, sy + 20), title, font=font_sub, fill=col)
        draw.text((140, sy + 60), desc, font=font_body, fill=TEXT_WHITE)

    draw_footer_card(draw, "Complete privacy sovereignty for healthcare, finance, and legal agents")
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
    draw.text((150, 1220), "• Model architecture deep dives", font=font_sub, fill=TEXT_WHITE)
    draw.text((150, 1270), "• Autonomous agent system blueprints", font=font_sub, fill=TEXT_WHITE)
    draw.text((150, 1320), "• 100% verified, zero hype", font=font_sub, fill=ACCENT_GREEN)

    draw_footer_card(draw, "Follow @lidoailab for daily autonomous AI intelligence")
    img.save(ASSETS_DIR / "shot_05.png")
    print("Rendered shot_05.png")

def main():
    print("Rendering GPT-6 Sol & Luna Visual Frames...")
    render_shot_01()
    render_shot_02()
    render_shot_03()
    render_shot_04()
    render_shot_05()
    print("All 5 GPT-6 Sol & Luna visual frames rendered successfully!")

if __name__ == "__main__":
    main()
