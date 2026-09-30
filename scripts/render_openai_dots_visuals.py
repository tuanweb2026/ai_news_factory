#!/usr/bin/env python3
"""Renders high-density technical visual frames for OpenAI DevDay Dots & GPT-6.1 Sol Short
in strict compliance with Anti-Black-Void Gate and Visual Style Bible v1.0.
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
ASSETS_DIR = Path("data/visuals/production_assets_dots")
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

font_title_lg = get_font(FONT_BOLD, 46)
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
# SHOT 01: Chatbots to Autonomous Agents
# ==========================================
def render_shot_01():
    img, draw = create_base_canvas(glow_color=(15, 25, 45), glow_center=(540, 940))
    draw_title_card(draw, "PARADIGM SHIFT", ACCENT_CYAN, "BEYOND CHATBOTS", "24/7 AUTONOMOUS AGENT ERA")
    
    # Diagram Area Y: 460 to 1420
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=(10, 15, 23), outline=CARD_BORDER, width=2)
    draw.text((100, 490), "AI ARCHITECTURE EVOLUTION (2022 -> 2026)", font=font_mono_md, fill=ACCENT_CYAN)

    # 1. 2022-2024 Reactive Chatbot
    draw.rounded_rectangle([100, 560, W - 100, 800], radius=14, fill=CARD_BG, outline=(40, 50, 70), width=2)
    draw.text((130, 585), "TRADITIONAL CHATBOTS (REACTIVE)", font=font_title_md, fill=TEXT_MUTED)
    draw.text((130, 635), "• Single turn input -> Single turn text output", font=font_body, fill=TEXT_WHITE)
    draw.text((130, 675), "• Idle when window closed; zero memory persistence", font=font_body, fill=TEXT_WHITE)
    draw.rounded_rectangle([W - 380, 585, W - 130, 635], radius=8, fill=(25, 30, 40), outline=ACCENT_AMBER, width=1)
    draw.text((W - 360, 598), "PROMPT & WAIT", font=font_mono_sm, fill=ACCENT_AMBER)

    # Down arrow
    draw.line([(540, 800), (540, 860)], fill=ACCENT_CYAN, width=4)
    draw.polygon([(525, 855), (555, 855), (540, 880)], fill=ACCENT_CYAN)

    # 2. 2026 Persistent Autonomous Agent
    draw.rounded_rectangle([100, 880, W - 100, 1160], radius=16, fill=(14, 25, 42), outline=ACCENT_CYAN, width=3)
    draw.text((130, 905), "AUTONOMOUS AGENTS (PROACTIVE)", font=font_title_md, fill=ACCENT_CYAN)
    draw.text((130, 960), "• Always-on 24/7 background execution loop", font=font_body, fill=TEXT_WHITE)
    draw.text((130, 1005), "• Multi-tool orchestration & isolated cloud sandboxes", font=font_body, fill=TEXT_WHITE)
    draw.text((130, 1050), "• Proactive state maintenance without user prompting", font=font_body, fill=TEXT_WHITE)
    draw.rounded_rectangle([W - 380, 905, W - 130, 955], radius=8, fill=(20, 38, 60), outline=ACCENT_CYAN, width=1)
    draw.text((W - 360, 918), "ALWAYS-ON 24/7", font=font_mono_sm, fill=ACCENT_CYAN)

    # Highlight Callout Banner
    draw.rounded_rectangle([110, 1200, W - 110, 1380], radius=14, fill=(18, 28, 42), outline=ACCENT_GREEN, width=2)
    draw.text((140, 1225), "OPENAI DEVDAY 2026 UNVEILING", font=font_sub, fill=ACCENT_GREEN)
    draw.text((140, 1270), "OpenAI shifts platform strategy from conversational assistants", font=font_body, fill=TEXT_WHITE)
    draw.text((140, 1310), "to persistent autonomous agents operating continuously.", font=font_body, fill=TEXT_WHITE)

    draw_footer_card(draw, "FROM PASSIVE CHAT INTERFACES TO PERSISTENT COMPUTE NODES")
    img.save(ASSETS_DIR / "shot-01.png")
    print("Saved shot-01.png")

# ==========================================
# SHOT 02: OpenAI Dots Announcement
# ==========================================
def render_shot_02():
    img, draw = create_base_canvas(glow_color=(12, 32, 50), glow_center=(540, 940))
    draw_title_card(draw, "KEYNOTE ANNOUNCEMENT", ACCENT_CYAN, "MEET OPENAI DOTS", "PERSONAL 24/7 AI AGENTS")
    
    # Diagram Area Y: 460 to 1420
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=(10, 15, 23), outline=CARD_BORDER, width=2)
    draw.text((100, 490), "OPENAI DOT CORE ARCHITECTURE", font=font_mono_md, fill=ACCENT_CYAN)

    # Central Dot Avatar Card
    draw.rounded_rectangle([100, 550, W - 100, 930], radius=16, fill=(16, 26, 42), outline=ACCENT_CYAN, width=3)
    
    # Glowing Dot graphic
    cx, cy = 540, 680
    for r in [90, 70, 50]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(20, 45, 75))
    draw.ellipse([cx - 35, cy - 35, cx + 35, cy + 35], fill=ACCENT_CYAN)
    # Orbiting dots
    draw.ellipse([cx - 95, cy - 10, cx - 75, cy + 10], fill=ACCENT_GREEN)
    draw.ellipse([cx + 75, cy - 10, cx + 95, cy + 10], fill=ACCENT_VIOLET)
    
    draw.text((cx - 160, 790), "DOT AGENT INSTANCE", font=font_title_md, fill=TEXT_WHITE)
    draw.text((cx - 190, 840), "STATUS: ACTIVE • DAEMON RUNNING", font=font_mono_sm, fill=ACCENT_GREEN)

    # Feature List Cards
    specs = [
        ("Background Persistence:", "Runs 24/7 without open browser sessions", ACCENT_CYAN),
        ("Personal Customization:", "Trained on individual workflow preferences", ACCENT_VIOLET),
        ("Secure Cloud Sandbox:", "Zero risk of local uncontained side effects", ACCENT_GREEN),
    ]
    for idx, (label, val, col) in enumerate(specs):
        sy = 970 + idx * 135
        draw.rounded_rectangle([100, sy, W - 100, sy + 115], radius=12, fill=CARD_BG, outline=col, width=2)
        draw.text((130, sy + 22), label, font=font_sub, fill=col)
        draw.text((130, sy + 65), val, font=font_body, fill=TEXT_WHITE)

    draw_footer_card(draw, "CUSTOMIZABLE PERSONAL AGENTS RUNNING PERPETUALLY IN THE CLOUD")
    img.save(ASSETS_DIR / "shot-02.png")
    print("Saved shot-02.png")

# ==========================================
# SHOT 03: Persistent Multi-Tool Workflows
# ==========================================
def render_shot_03():
    img, draw = create_base_canvas(glow_color=(20, 20, 48), glow_center=(540, 940))
    draw_title_card(draw, "TOOL EXECUTION", ACCENT_VIOLET, "PERSISTENT WORKFLOWS", "END-TO-END AUTONOMOUS TASKS")
    
    # Diagram Area Y: 460 to 1420
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=(10, 15, 23), outline=CARD_BORDER, width=2)
    draw.text((100, 490), "CROSS-PLATFORM ORCHESTRATION PIPELINE", font=font_mono_md, fill=ACCENT_VIOLET)

    workflows = [
        ("SLACK & COMMUNICATIONS", "Automates channel replies, drafts briefing digests, schedules team syncs.", ACCENT_CYAN, 560),
        ("GITHUB & CODE REPOSITORIES", "Reviews incoming PRs, runs test suites, fixes regression bugs autonomously.", ACCENT_GREEN, 820),
        ("CLOUD CLUSTER SANDBOXES", "Executes data transforms, manages API containers, logs system health.", ACCENT_AMBER, 1080),
    ]

    for title, desc, col, y in workflows:
        draw.rounded_rectangle([100, y, W - 100, y + 210], radius=14, fill=CARD_BG, outline=col, width=2)
        draw.rounded_rectangle([125, y + 20, 125 + len(title) * 13 + 30, y + 60], radius=6, fill=(20, 26, 38), outline=col, width=1)
        draw.text((140, y + 28), title, font=font_mono_sm, fill=col)
        draw.text((130, y + 80), desc, font=font_body, fill=TEXT_WHITE)
        draw.text((130, y + 140), "⚡ STATE: CONTINUOUS BACKGROUND DAEMON", font=font_mono_sm, fill=TEXT_MUTED)

    # Cross connect indicator
    draw.rounded_rectangle([100, 1320, W - 100, 1400], radius=10, fill=(18, 25, 38), outline=ACCENT_CYAN, width=1)
    draw.text((130, 1345), "SYNCHRONIZED EVENT LOOP: ZERO USER LATENCY", font=font_mono_md, fill=ACCENT_CYAN)

    draw_footer_card(draw, "INTEGRATED TOOL-CALLING ACROSS ENTERPRISE SOFTWARE SUITES")
    img.save(ASSETS_DIR / "shot-03.png")
    print("Saved shot-03.png")

# ==========================================
# SHOT 04: Powered by GPT-6.1 Sol
# ==========================================
def render_shot_04():
    img, draw = create_base_canvas(glow_color=(15, 35, 30), glow_center=(540, 940))
    draw_title_card(draw, "ENGINEERING CORE", ACCENT_GREEN, "GPT-6.1 SOL ENGINE", "ASTRA REASONING AT 80% LOWER COST")
    
    # Diagram Area Y: 460 to 1420
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=(10, 15, 23), outline=CARD_BORDER, width=2)
    draw.text((100, 490), "MODEL EFFICIENCY & BENCHMARK COMPARISON", font=font_mono_md, fill=ACCENT_GREEN)

    # Benchmark Cards
    cards = [
        ("REASONING CAPABILITY", "Matches GPT-6 Astra benchmark depth on STEM & coding", ACCENT_CYAN, 560),
        ("INFERENCE COST EFFICIENCY", "80% reduction in token pricing for sustainable 24/7 runs", ACCENT_GREEN, 760),
        ("CONTAINMENT GUARDRAILS", "Strict sandbox permissions eliminate deceptive drift risks", ACCENT_AMBER, 960),
    ]

    for title, desc, col, y in cards:
        draw.rounded_rectangle([100, y, W - 100, y + 170], radius=14, fill=CARD_BG, outline=col, width=2)
        draw.text((130, y + 25), title, font=font_sub, fill=col)
        draw.text((130, y + 75), desc, font=font_body, fill=TEXT_WHITE)
        # Meter
        draw.rounded_rectangle([130, y + 120, W - 130, y + 145], radius=6, fill=(20, 28, 40))
        draw.rounded_rectangle([130, y + 120, W - 200, y + 145], radius=6, fill=col)

    # Sol vs Astra Summary Box
    draw.rounded_rectangle([100, 1170, W - 100, 1380], radius=14, fill=(16, 28, 24), outline=ACCENT_GREEN, width=2)
    draw.text((130, 1200), "OPTIMIZED FOR CONTINUOUS AGENT OPERATION", font=font_title_md, fill=ACCENT_GREEN)
    draw.text((130, 1255), "By pruning speculative overhead and hard-locking scope APIs,", font=font_body, fill=TEXT_WHITE)
    draw.text((130, 1295), "GPT-6.1 Sol makes 24/7 background intelligence affordable.", font=font_body, fill=TEXT_WHITE)

    draw_footer_card(draw, "ENTERPRISE-GRADE REASONING BALANCED WITH COST EFFICIENCY")
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
    cx, cy = 540, 780
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
    
    draw.text((cx - 160, cy + 160), "VERIFIED FACTUAL", font=font_title_md, fill=TEXT_WHITE)
    draw.text((cx - 140, cy + 215), "14-GATE RED TEAM PASS", font=font_mono_md, fill=ACCENT_CYAN)

    specs = [
        "PRIMARY SOURCE: OPENAI DEVDAY 2026",
        "KEYNOTE DATE: SEPTEMBER 30, 2026",
        "PRODUCT: DOTS 24/7 AGENTS & GPT-6.1 SOL",
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
    print("All 5 OpenAI Dots frames rendered successfully.")
