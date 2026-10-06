#!/usr/bin/env python3
"""Renders high-density technical visual frames for Anthropic Claude Sonnet 5.5 Short
in strict compliance with Anti-Black-Void Gate and Visual Style Bible v1.0.
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
ASSETS_DIR = Path("data/visuals/production_assets_sonnet55")
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Colors
BG_BASE = (7, 10, 15)
ANTHROPIC_TERRA = (204, 120, 92)
ANTHROPIC_LIGHT = (235, 160, 135)
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

def create_base_canvas(glow_color=(45, 25, 20), glow_center=(540, 960), glow_radius=750):
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
# SHOT 01: Claude Sonnet 5.5 Unveiled
# ==========================================
def render_shot_01():
    img, draw = create_base_canvas(glow_color=(45, 25, 20), glow_center=(540, 800))
    draw_title_card(draw, "ANTHROPIC FRONTIER RELEASE", ANTHROPIC_TERRA, "CLAUDE SONNET 5.5 UNVEILED", "High-Efficiency Frontier Developer Workhorse")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "CLAUDE 5.5 SERIES ARCHITECTURE", font=font_tag, fill=ACCENT_CYAN)
    
    # Model Profile Hero Card
    draw.rounded_rectangle([110, 540, W - 110, 860], radius=16, fill=(24, 18, 22), outline=ANTHROPIC_TERRA, width=2)
    draw.text((140, 570), "CLAUDE SONNET 5.5", font=font_title_lg, fill=ANTHROPIC_LIGHT)
    draw.text((140, 640), "Next-Gen Daily Driver for Autonomous Coding", font=font_title_md, fill=TEXT_WHITE)
    draw.text((140, 710), "• +30% Faster Token Generation Speed", font=font_sub, fill=ACCENT_GREEN)
    draw.text((140, 765), "• 1,000,000 Token Context Window", font=font_sub, fill=ACCENT_CYAN)
    draw.text((140, 815), "• 128,000 Max Output Tokens / Request", font=font_sub, fill=ACCENT_AMBER)

    # Core Competencies
    comp = [
        ("Agentic Software Engineering", "Full repository bug fixing, refactoring, tests", ACCENT_CYAN),
        ("Autonomous Computer Use", "80.1% on OSWorld 2.1 UI desktop benchmark", ANTHROPIC_LIGHT),
        ("Accessible Developer Economics", "$2.00 / 1M Input • $10.00 / 1M Output", ACCENT_GREEN),
    ]
    for i, (title, desc, col) in enumerate(comp):
        sy = 900 + i * 165
        draw.rounded_rectangle([110, sy, W - 110, sy + 135], radius=14, fill=(18, 24, 32), outline=col, width=2)
        draw.text((140, sy + 22), title, font=font_title_md, fill=col)
        draw.text((140, sy + 75), desc, font=font_sub, fill=TEXT_WHITE)

    draw_footer_card(draw, "Brings frontier intelligence to cost-effective daily engineering workflows")
    img.save(ASSETS_DIR / "shot_01.png")
    print("Rendered shot_01.png")

# ==========================================
# SHOT 02: 1M Context • +30% Speed
# ==========================================
def render_shot_02():
    img, draw = create_base_canvas(glow_color=(35, 30, 20), glow_center=(540, 850))
    draw_title_card(draw, "SPEED & CONTEXT SPECIFICATION", ACCENT_CYAN, "1M CONTEXT • +30% SPEED", "Massive Memory with Zero Latency Penalty")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "RUNTIME BENCHMARKS", font=font_tag, fill=ACCENT_CYAN)
    
    # 2 Big Stat Cards
    # Speed
    draw.rounded_rectangle([110, 540, W - 110, 880], radius=16, fill=(16, 26, 36), outline=ACCENT_CYAN, width=2)
    draw.text((140, 570), "+30% GENERATION SPEED", font=font_title_md, fill=ACCENT_CYAN)
    draw.text((140, 630), "Optimized speculative decoding architecture", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 690), "• Cuts interactive terminal coding wait times", font=font_body, fill=TEXT_MUTED)
    draw.text((140, 740), "• Rapid multi-step reasoning cycles", font=font_body, fill=TEXT_MUTED)
    draw.rounded_rectangle([140, 800, W - 160, 850], radius=8, fill=ACCENT_CYAN)
    draw.text((160, 812), "130% SPEED RELATIVE TO SONNET 5", font=font_mono_md, fill=BG_BASE)

    # Context
    draw.rounded_rectangle([110, 920, W - 110, 1370], radius=16, fill=(24, 18, 28), outline=ANTHROPIC_TERRA, width=2)
    draw.text((140, 950), "1,000,000 TOKEN CONTEXT WINDOW", font=font_title_md, fill=ANTHROPIC_LIGHT)
    draw.text((140, 1010), "Ingest 30+ microservices & entire documentation libraries", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 1070), "• 128,000 Output Tokens in single generation", font=font_body, fill=TEXT_WHITE)
    draw.text((140, 1120), "• Instant cache reads at $0.20 / 1M tokens", font=font_body, fill=ACCENT_GREEN)
    draw.text((140, 1170), "• Perfect needle-in-haystack recall across 1M tokens", font=font_body, fill=ACCENT_AMBER)
    draw.rounded_rectangle([140, 1250, W - 160, 1320], radius=10, fill=(45, 25, 20), outline=ANTHROPIC_TERRA, width=1)
    draw.text((160, 1270), "ENTERPRISE AIR-GAP DEPLOYMENT READY", font=font_tag, fill=ANTHROPIC_LIGHT)

    draw_footer_card(draw, "Maintains lightning response times across million-token codebases")
    img.save(ASSETS_DIR / "shot_02.png")
    print("Rendered shot_02.png")

# ==========================================
# SHOT 03: 70.6% Terminal-Bench Record
# ==========================================
def render_shot_03():
    img, draw = create_base_canvas(glow_color=(15, 45, 25), glow_center=(540, 900))
    draw_title_card(draw, "AGENTIC CODING BENCHMARK", ACCENT_GREEN, "70.6% TERMINAL-BENCH RECORD", "Highest Autonomous Engineering Score")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "TERMINAL-BENCH 4.0 BENCHMARK LEADERBOARD", font=font_tag, fill=ACCENT_CYAN)
    
    bars = [
        ("Claude Sonnet 5.5", 70.6, ACCENT_GREEN),
        ("Claude Opus 5.5", 66.4, ANTHROPIC_LIGHT),
        ("GPT-6 Astra", 65.2, ACCENT_CYAN),
        ("Claude Sonnet 5 (Legacy)", 10.3, ACCENT_RED),
    ]
    for i, (model_name, score, col) in enumerate(bars):
        by = 540 + i * 190
        draw.rounded_rectangle([110, by, W - 110, by + 155], radius=14, fill=(16, 22, 30), outline=CARD_BORDER, width=2)
        draw.text((140, by + 25), model_name, font=font_title_md, fill=TEXT_WHITE)
        draw.text((W - 240, by + 25), f"{score}%", font=font_title_md, fill=col)
        
        # Bar graphic
        bar_w = int((W - 280) * (score / 100.0))
        draw.rounded_rectangle([140, by + 90, 140 + bar_w, by + 130], radius=8, fill=col)

    draw_footer_card(draw, "Massive generational leap in autonomous debugging, refactoring, and git operations")
    img.save(ASSETS_DIR / "shot_03.png")
    print("Rendered shot_03.png")

# ==========================================
# SHOT 04: The Ultimate Agent Driver
# ==========================================
def render_shot_04():
    img, draw = create_base_canvas(glow_color=(35, 20, 40), glow_center=(540, 850))
    draw_title_card(draw, "DEPLOYMENT ECOSYSTEM", ANTHROPIC_LIGHT, "THE ULTIMATE AGENT DRIVER", "Available Globally on All Major Clouds")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "MULTI-CLOUD AVAILABILITY & INTEGRATIONS", font=font_tag, fill=ACCENT_CYAN)
    
    clouds = [
        ("Anthropic API & Console", "Direct access with prompt caching & batch API", ANTHROPIC_LIGHT),
        ("Amazon Bedrock", "Full AWS VPC enterprise compliance & serverless", ACCENT_AMBER),
        ("Google Cloud Vertex AI", "Deep integration with BigQuery and Google AI stacks", ACCENT_CYAN),
        ("Microsoft Azure AI", "Enterprise data sovereignty & security enclave", ACCENT_GREEN),
    ]
    for i, (cname, cdesc, col) in enumerate(clouds):
        cy_pos = 540 + i * 195
        draw.rounded_rectangle([110, cy_pos, W - 110, cy_pos + 160], radius=14, fill=(18, 22, 32), outline=col, width=2)
        draw.text((140, cy_pos + 25), cname, font=font_title_md, fill=col)
        draw.text((140, cy_pos + 85), cdesc, font=font_sub, fill=TEXT_WHITE)

    draw_footer_card(draw, "Empowers developer teams with state-of-the-art autonomous software pipelines")
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
    draw.text((150, 1270), "• Autonomous developer agent benchmarks", font=font_sub, fill=TEXT_WHITE)
    draw.text((150, 1320), "• 100% verified, zero hype", font=font_sub, fill=ACCENT_GREEN)

    draw_footer_card(draw, "Follow @lidoailab for daily autonomous AI intelligence")
    img.save(ASSETS_DIR / "shot_05.png")
    print("Rendered shot_05.png")

def main():
    print("Rendering Claude Sonnet 5.5 Visual Frames...")
    render_shot_01()
    render_shot_02()
    render_shot_03()
    render_shot_04()
    render_shot_05()
    print("All 5 visual frames rendered successfully!")

if __name__ == "__main__":
    main()
