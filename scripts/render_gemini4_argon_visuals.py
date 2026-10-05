#!/usr/bin/env python3
"""Renders high-density technical visual frames for Google Gemini 4 Argon Short
in strict compliance with Anti-Black-Void Gate and Visual Style Bible v1.0.
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
ASSETS_DIR = Path("data/visuals/production_assets_gemini4_argon")
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Colors
BG_BASE = (7, 10, 15)
GEMINI_BLUE = (66, 133, 244)
GEMINI_CYAN = (77, 235, 255)
GRID_COLOR = (20, 30, 44)
GRID_TICK = (35, 55, 80)
TEXT_WHITE = (243, 247, 250)
TEXT_MUTED = (139, 152, 167)
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

def create_base_canvas(glow_color=(15, 30, 50), glow_center=(540, 960), glow_radius=750):
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
    draw.rounded_rectangle([90, 108, 380, 162], radius=10, fill=(18, 35, 55), outline=GEMINI_CYAN, width=1)
    draw.ellipse([110, 130, 122, 142], fill=GEMINI_CYAN)
    draw.text((135, 122), "AI NEWS FACTORY", font=font_tag, fill=TEXT_WHITE)
    draw.text((W - 390, 124), "VERIFIED INTELLIGENCE", font=font_mono_sm, fill=GEMINI_CYAN)
    
    return img, draw

def draw_title_card(draw, badge_text, badge_color, headline, subtitle):
    draw.rounded_rectangle([70, 220, W - 70, 420], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.rounded_rectangle([100, 245, 100 + len(badge_text) * 14 + 40, 285], radius=8, fill=(20, 30, 42), outline=badge_color, width=1)
    draw.text((120, 252), badge_text, font=font_tag, fill=badge_color)
    draw.text((100, 300), headline, font=font_title_lg, fill=TEXT_WHITE)
    draw.text((100, 365), subtitle, font=font_sub, fill=GEMINI_CYAN)

def draw_footer_card(draw, text):
    draw.rounded_rectangle([70, 1460, W - 70, 1560], radius=14, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((100, 1495), text, font=font_sub, fill=TEXT_MUTED)

# ==========================================
# SHOT 01: 1,000,000 Token Output Unlocked
# ==========================================
def render_shot_01():
    img, draw = create_base_canvas(glow_color=(15, 35, 60), glow_center=(540, 800))
    draw_title_card(draw, "GOOGLE FRONTIER AI", GEMINI_CYAN, "1M TOKEN OUTPUT UNLOCKED", "Historic Generative Limit Broken")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "OUTPUT GENERATION CAPACITY SPECIFICATION", font=font_tag, fill=GEMINI_CYAN)
    
    # Hero Metric Card
    draw.rounded_rectangle([110, 540, W - 110, 830], radius=16, fill=(16, 26, 42), outline=GEMINI_CYAN, width=2)
    draw.text((140, 570), "1,000,000 TOKENS", font=font_title_lg, fill=GEMINI_CYAN)
    draw.text((140, 640), "Single Continuous Generative Response", font=font_title_md, fill=TEXT_WHITE)
    draw.text((140, 710), "• 15.6x Increase over industry 64,000 token limit", font=font_sub, fill=ACCENT_GREEN)
    draw.text((140, 765), "• Equivalent to ~750,000 words or entire software repos", font=font_mono_sm, fill=TEXT_MUTED)

    # Architectural highlights
    highlights = [
        ("Long-Horizon Reasoning", "Eliminates prompt fragmentation across massive tasks", GEMINI_BLUE),
        ("Autonomous Software Migration", "Refactors enterprise codebases in a single execution", ACCENT_VIOLET),
        ("Continuous Verification", "Generates and self-audits complete system implementations", ACCENT_GREEN),
    ]
    for i, (title, desc, col) in enumerate(highlights):
        sy = 870 + i * 175
        draw.rounded_rectangle([110, sy, W - 110, sy + 145], radius=14, fill=(18, 24, 34), outline=col, width=2)
        draw.text((140, sy + 25), title, font=font_title_md, fill=col)
        draw.text((140, sy + 80), desc, font=font_sub, fill=TEXT_WHITE)

    draw_footer_card(draw, "Breaks the fundamental barrier on autonomous AI reasoning horizons")
    img.save(ASSETS_DIR / "shot_01.png")
    print("Rendered shot_01.png")

# ==========================================
# SHOT 02: Gemini 4 Argon Launched
# ==========================================
def render_shot_02():
    img, draw = create_base_canvas(glow_color=(15, 25, 55), glow_center=(540, 850))
    draw_title_card(draw, "NEW FRONTIER MODEL", GEMINI_BLUE, "GEMINI 4 ARGON LAUNCHED", "Built for Complex Engineering & Security")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "MODEL CAPABILITIES & SPECS", font=font_tag, fill=GEMINI_CYAN)
    
    specs = [
        ("SWE-Bench Verified", "77.9% State-of-the-Art Software Engineering", ACCENT_GREEN),
        ("Target Output Horizon", "1,000,000 Output Tokens / Request", GEMINI_CYAN),
        ("Introductory Pricing", "$2.00 / 1M Input • $10.00 / 1M Output", ACCENT_AMBER),
        ("Deployment Channel", "Fairwind Program & Trusted Enterprise Partners", ACCENT_VIOLET),
    ]
    for i, (lbl, val, col) in enumerate(specs):
        sy = 540 + i * 200
        draw.rounded_rectangle([110, sy, W - 110, sy + 165], radius=14, fill=(16, 24, 36), outline=col, width=2)
        draw.text((140, sy + 25), lbl, font=font_tag, fill=col)
        draw.text((140, sy + 75), val, font=font_title_md, fill=TEXT_WHITE)

    draw_footer_card(draw, "Official release from Google DeepMind research infrastructure")
    img.save(ASSETS_DIR / "shot_02.png")
    print("Rendered shot_02.png")

# ==========================================
# SHOT 03: 64K vs 1,000,000 Tokens
# ==========================================
def render_shot_03():
    img, draw = create_base_canvas(glow_color=(20, 40, 50), glow_center=(540, 900))
    draw_title_card(draw, "OUTPUT HORIZON COMPARISON", GEMINI_CYAN, "64K vs 1,000,000 TOKENS", "A Generational Shift in AI Generation")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "SINGLE-RESPONSE GENERATIVE CAPACITY", font=font_tag, fill=GEMINI_CYAN)
    
    # 64K Box
    draw.rounded_rectangle([110, 550, W - 110, 880], radius=16, fill=(24, 20, 24), outline=ACCENT_RED, width=2)
    draw.text((140, 580), "LEGACY MODELS (64,000 TOKENS)", font=font_title_md, fill=ACCENT_RED)
    draw.text((140, 640), "• Limited to ~45,000 words per output", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 695), "• Cuts off mid-refactoring on large codebases", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 750), "• Requires complicated chunking and multiple prompts", font=font_sub, fill=TEXT_MUTED)
    draw.rounded_rectangle([140, 810, 260, 850], radius=8, fill=ACCENT_RED)
    draw.text((160, 820), "64K LIMIT", font=font_tag, fill=BG_BASE)

    # 1M Box
    draw.rounded_rectangle([110, 930, W - 110, 1370], radius=16, fill=(16, 28, 42), outline=GEMINI_CYAN, width=2)
    draw.text((140, 960), "GEMINI 4 ARGON (1,000,000 TOKENS)", font=font_title_lg, fill=GEMINI_CYAN)
    draw.text((140, 1030), "• Complete 750,000-word software repositories", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 1085), "• End-to-end kernel development & testing suites", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 1140), "• Unbroken execution chain without human intervention", font=font_sub, fill=ACCENT_GREEN)
    draw.rounded_rectangle([140, 1220, W - 160, 1280], radius=10, fill=GEMINI_CYAN)
    draw.text((160, 1235), "1,000,000 TOKENS (15.6X CAPACITY)", font=font_title_md, fill=BG_BASE)

    draw_footer_card(draw, "Eliminates output token starvation across enterprise workflows")
    img.save(ASSETS_DIR / "shot_03.png")
    print("Rendered shot_03.png")

# ==========================================
# SHOT 04: Fairwind Cyber Defense
# ==========================================
def render_shot_04():
    img, draw = create_base_canvas(glow_color=(35, 20, 20), glow_center=(540, 850))
    draw_title_card(draw, "AUTONOMOUS CYBER DEFENSE", ACCENT_RED, "FAIRWIND CYBER DEFENSE", "Autonomous Zero-Day Vulnerability Patching")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "MISSION: CRITICAL INFRASTRUCTURE DEFENSE", font=font_tag, fill=GEMINI_CYAN)
    
    radar_cards = [
        ("Zero-Day Ingestion", "Ingests entire kernel source codebases into 1M context", GEMINI_CYAN),
        ("Autonomous Vulnerability Discovery", "Unsupervised symbolic verification of exploit vectors", ACCENT_AMBER),
        ("Instant Patch Generation", "Generates full verified regression-tested patches", ACCENT_GREEN),
        ("Government & Critical Infra", "Controlled deployment via Google Fairwind Program", ACCENT_RED),
    ]
    for i, (title, desc, col) in enumerate(radar_cards):
        sy = 540 + i * 195
        draw.rounded_rectangle([110, sy, W - 110, sy + 160], radius=14, fill=(22, 18, 26), outline=col, width=2)
        draw.text((140, sy + 25), title, font=font_title_md, fill=col)
        draw.text((140, sy + 85), desc, font=font_sub, fill=TEXT_WHITE)

    draw_footer_card(draw, "Transforms defensive cybersecurity from manual triage to autonomous patch loops")
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
        
    draw.rounded_rectangle([200, 620, W - 200, 880], radius=24, fill=CARD_BG, outline=GEMINI_CYAN, width=3)
    draw.text((240, 660), "AI NEWS FACTORY", font=font_title_lg, fill=TEXT_WHITE)
    draw.text((310, 740), "DAILY VERIFIED INTELLIGENCE", font=font_tag, fill=GEMINI_CYAN)
    draw.text((275, 800), "youtube.com/@lidoailab", font=font_mono_md, fill=ACCENT_VIOLET)
    
    # CTA Card
    draw.rounded_rectangle([110, 1050, W - 110, 1380], radius=20, fill=(18, 25, 38), outline=CARD_BORDER, width=2)
    draw.text((150, 1090), "STAY AHEAD OF FRONTIER AI", font=font_tag, fill=ACCENT_AMBER)
    draw.text((150, 1145), "SUBSCRIBE FOR DAILY BREAKTHROUGHS", font=font_title_md, fill=TEXT_WHITE)
    draw.text((150, 1220), "• Google DeepMind model releases", font=font_sub, fill=TEXT_WHITE)
    draw.text((150, 1270), "• Deep technical benchmarks & specs", font=font_sub, fill=TEXT_WHITE)
    draw.text((150, 1320), "• 100% verified, zero hype", font=font_sub, fill=ACCENT_GREEN)

    draw_footer_card(draw, "Follow @lidoailab for daily autonomous AI intelligence")
    img.save(ASSETS_DIR / "shot_05.png")
    print("Rendered shot_05.png")

def main():
    print("Rendering Google Gemini 4 Argon Visual Frames...")
    render_shot_01()
    render_shot_02()
    render_shot_03()
    render_shot_04()
    render_shot_05()
    print("All 5 visual frames rendered successfully!")

if __name__ == "__main__":
    main()
