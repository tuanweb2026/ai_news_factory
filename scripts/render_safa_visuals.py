#!/usr/bin/env python3
"""Renders high-density technical visual frames for SAFA Alliance Short
in strict compliance with Anti-Black-Void Gate and Visual Style Bible v1.0.
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
ASSETS_DIR = Path("data/visuals/production_assets_safa")
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
# SHOT 01: Unified Frontier Safety Pact
# ==========================================
def render_shot_01():
    img, draw = create_base_canvas(glow_color=(15, 25, 45), glow_center=(540, 940))
    draw_title_card(draw, "HISTORIC ALLIANCE", ACCENT_CYAN, "UNIFIED SAFETY PACT", "FRONTIER AI LABS UNITE")
    
    # Diagram Area Y: 460 to 1420
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=(10, 15, 23), outline=CARD_BORDER, width=2)
    draw.text((100, 490), "STANDARDS AUTHORITY FOR FRONTIER AI", font=font_mono_md, fill=ACCENT_CYAN)

    # 4 Lab Badges Grid
    labs = [
        ("OPENAI", "Frontier Alignment Protocols", ACCENT_CYAN, 560),
        ("ANTHROPIC", "Constitutional AI & Safety Probes", ACCENT_AMBER, 750),
        ("GOOGLE DEEPMIND", "Autonomous Containment Evals", ACCENT_GREEN, 940),
        ("MICROSOFT", "Enterprise Governance & Audit Gates", ACCENT_VIOLET, 1130),
    ]

    for name, role, col, y in labs:
        draw.rounded_rectangle([100, y, W - 100, y + 155], radius=14, fill=CARD_BG, outline=col, width=2)
        draw.text((130, y + 25), name, font=font_title_md, fill=TEXT_WHITE)
        draw.text((130, y + 75), role, font=font_body, fill=TEXT_MUTED)
        draw.rounded_rectangle([W - 320, y + 25, W - 130, y + 70], radius=8, fill=(20, 28, 40), outline=col, width=1)
        draw.text((W - 300, y + 36), "SIGNATORY", font=font_mono_sm, fill=col)

    # Callout Banner
    draw.rounded_rectangle([110, 1310, W - 110, 1400], radius=10, fill=(18, 28, 42), outline=ACCENT_CYAN, width=1)
    draw.text((140, 1342), "FIRST BINDING MULTI-LAB SAFETY AUDITING COMPACT", font=font_mono_md, fill=ACCENT_CYAN)

    draw_footer_card(draw, "UNIFIED PRE-DEPLOYMENT GATES FOR AUTONOMOUS AGENT MODELS")
    img.save(ASSETS_DIR / "shot-01.png")
    print("Saved shot-01.png")

# ==========================================
# SHOT 02: SAFA Standards Authority
# ==========================================
def render_shot_02():
    img, draw = create_base_canvas(glow_color=(12, 32, 50), glow_center=(540, 940))
    draw_title_card(draw, "CHARTER ANNOUNCEMENT", ACCENT_CYAN, "MEET SAFA ALLIANCE", "INDUSTRY AUDIT STANDARDS")
    
    # Diagram Area Y: 460 to 1420
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=(10, 15, 23), outline=CARD_BORDER, width=2)
    draw.text((100, 490), "SAFA MULTILATERAL GOVERNANCE MANDATE", font=font_mono_md, fill=ACCENT_CYAN)

    # Central Shield Badge
    draw.rounded_rectangle([100, 550, W - 100, 930], radius=16, fill=(16, 26, 42), outline=ACCENT_CYAN, width=3)
    
    cx, cy = 540, 680
    for r in [90, 70, 50]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(20, 45, 75))
    draw.ellipse([cx - 35, cy - 35, cx + 35, cy + 35], fill=ACCENT_CYAN)
    draw.ellipse([cx - 95, cy - 10, cx - 75, cy + 10], fill=ACCENT_GREEN)
    draw.ellipse([cx + 75, cy - 10, cx + 95, cy + 10], fill=ACCENT_VIOLET)
    
    draw.text((cx - 150, 790), "SAFA CHARTER SEAL", font=font_title_md, fill=TEXT_WHITE)
    draw.text((cx - 200, 840), "STANDARDS AUTHORITY FOR FRONTIER AI", font=font_mono_sm, fill=ACCENT_GREEN)

    # Core Standards
    specs = [
        ("Mandatory Pre-Launch Audits:", "Rigorous red-teaming pass required before public API", ACCENT_CYAN),
        ("Universal Deception Benchmark:", "Standardized scoring for action misrepresentation", ACCENT_VIOLET),
        ("Zero Autonomous Breach Tolerance:", "Immediate model quarantine if safety containment fails", ACCENT_RED),
    ]
    for idx, (label, val, col) in enumerate(specs):
        sy = 970 + idx * 135
        draw.rounded_rectangle([100, sy, W - 100, sy + 115], radius=12, fill=CARD_BG, outline=col, width=2)
        draw.text((130, sy + 22), label, font=font_sub, fill=col)
        draw.text((130, sy + 65), val, font=font_body, fill=TEXT_WHITE)

    draw_footer_card(draw, "ESTABLISHING COMMON CRITICAL THRESHOLDS FOR FRONTIER AI")
    img.save(ASSETS_DIR / "shot-02.png")
    print("Saved shot-02.png")

# ==========================================
# SHOT 03: Mandatory Red-Team Gates
# ==========================================
def render_shot_03():
    img, draw = create_base_canvas(glow_color=(35, 15, 25), glow_center=(540, 940))
    draw_title_card(draw, "EVALUATION GATES", ACCENT_RED, "MANDATORY RED-TEAM GATES", "CONTAINMENT & DECEPTION THRESHOLDS")
    
    # Diagram Area Y: 460 to 1420
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=(10, 15, 23), outline=CARD_BORDER, width=2)
    draw.text((100, 490), "UNIFIED SAFETY METRICS THRESHOLDS", font=font_mono_md, fill=ACCENT_RED)

    metrics = [
        ("AGENT DECEPTION SCORING", "Must score < 0.05% misrepresentation rate across tests", ACCENT_RED, 560),
        ("SCOPE BOUNDARY CONTAINMENT", "Zero unapproved tool invocations outside designated sandbox", ACCENT_AMBER, 760),
        ("UNAUTHORIZED REPLICATION CHECK", "Hard-coded safeguards against autonomous process spawning", ACCENT_GREEN, 960),
    ]

    for title, desc, col, y in metrics:
        draw.rounded_rectangle([100, y, W - 100, y + 170], radius=14, fill=CARD_BG, outline=col, width=2)
        draw.text((130, y + 25), title, font=font_sub, fill=col)
        draw.text((130, y + 75), desc, font=font_body, fill=TEXT_WHITE)
        draw.rounded_rectangle([130, y + 120, W - 130, y + 145], radius=6, fill=(20, 28, 40))
        draw.rounded_rectangle([130, y + 120, W - 220, y + 145], radius=6, fill=col)

    draw.rounded_rectangle([100, 1170, W - 100, 1380], radius=14, fill=(26, 18, 22), outline=ACCENT_RED, width=2)
    draw.text((130, 1200), "PREVENTATIVE FAIL-CLOSED ARCHITECTURE", font=font_title_md, fill=ACCENT_RED)
    draw.text((130, 1255), "Any failure on mandatory red-team gates automatically halts", font=font_body, fill=TEXT_WHITE)
    draw.text((130, 1295), "commercial release, forcing models into quarantine RL study.", font=font_body, fill=TEXT_WHITE)

    draw_footer_card(draw, "RIGOROUS PRE-RELEASE AUDITING RIGS APPLIED TO ALL FLAGSHIPS")
    img.save(ASSETS_DIR / "shot-03.png")
    print("Saved shot-03.png")

# ==========================================
# SHOT 04: Real-Time Vulnerability Mesh
# ==========================================
def render_shot_04():
    img, draw = create_base_canvas(glow_color=(20, 20, 48), glow_center=(540, 940))
    draw_title_card(draw, "TELEMETRY MESH", ACCENT_VIOLET, "VULNERABILITY MESH", "CROSS-LAB INCIDENT EXCHANGE")
    
    # Diagram Area Y: 460 to 1420
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=(10, 15, 23), outline=CARD_BORDER, width=2)
    draw.text((100, 490), "CROSS-LAB TELEMETRY & EARLY WARNING PROTOCOL", font=font_mono_md, fill=ACCENT_VIOLET)

    channels = [
        ("ANONYMOUS ANOMALY FEEDS", "Labs share zero-day jailbreaks & deception traces in real time", ACCENT_CYAN, 560),
        ("CROSS-EVALUATION BENCHMARKS", "Each lab independently stress-tests peers' pre-release checkpoints", ACCENT_GREEN, 820),
        ("CONTAINMENT INCIDENT LOGS", "Shared registry of tool-calling failures and prompt leakage", ACCENT_AMBER, 1080),
    ]

    for title, desc, col, y in channels:
        draw.rounded_rectangle([100, y, W - 100, y + 210], radius=14, fill=CARD_BG, outline=col, width=2)
        draw.rounded_rectangle([125, y + 20, 125 + len(title) * 13 + 30, y + 60], radius=6, fill=(20, 26, 38), outline=col, width=1)
        draw.text((140, y + 28), title, font=font_mono_sm, fill=col)
        draw.text((130, y + 80), desc, font=font_body, fill=TEXT_WHITE)
        draw.text((130, y + 140), "🔒 ENCRYPTED EARLY-WARNING BUS ACTIVE", font=font_mono_sm, fill=TEXT_MUTED)

    draw.rounded_rectangle([100, 1320, W - 100, 1400], radius=10, fill=(18, 25, 38), outline=ACCENT_CYAN, width=1)
    draw.text((130, 1345), "COORDINATED VULNERABILITY DISCLOSURE ACROSS INDUSTRY", font=font_mono_md, fill=ACCENT_CYAN)

    draw_footer_card(draw, "COLLECTIVE DEFENSE AGAINST EMERGENT AGENT RISKS")
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
        "PRIMARY SOURCE: FRONTIER LAB JOINT CHARTER",
        "DATE: OCTOBER 2026 SAFETY ALLIANCE",
        "FRAMEWORK: SAFA UNIFIED RED-TEAM THRESHOLDS",
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
    print("All 5 SAFA Alliance frames rendered successfully.")
