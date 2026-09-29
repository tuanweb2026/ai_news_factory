#!/usr/bin/env python3
"""Renders high-density technical visual frames for NVIDIA Open Agent Safety Platform Short in strict compliance with
Anti-Black-Void Gate and Visual Style Bible v1.0.
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
ASSETS_DIR = Path("data/visuals/production_assets_safety")
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

font_title_lg = get_font(FONT_BOLD, 50)
font_title_md = get_font(FONT_BOLD, 38)
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
# SHOT 01: Rogue Agent Threat & Perimeter Breach
# ==========================================
def render_shot_01():
    img, draw = create_base_canvas(glow_color=(35, 15, 25), glow_center=(540, 940))
    draw_title_card(draw, "THREAT CONTAINMENT", ACCENT_RED, "CONTAINING ROGUE AGENTS", "AUTONOMOUS AI SANDBOX BREACHES")
    
    # Diagram Area Y: 460 to 1420
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=(10, 15, 23), outline=CARD_BORDER, width=2)
    draw.text((100, 490), "INCIDENT TELEMETRY: SANDBOX ESCAPE PROBE", font=font_mono_md, fill=ACCENT_RED)

    # Perimeter alert rings
    cx, cy = 540, 850
    for r in [280, 200, 130]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(65, 25, 35), width=2)

    # Central Compromised Agent Node
    draw.ellipse([cx - 85, cy - 85, cx + 85, cy + 85], fill=(38, 16, 24), outline=ACCENT_RED, width=3)
    draw.text((cx - 55, cy - 35), "ROGUE", font=font_title_md, fill=ACCENT_RED)
    draw.text((cx - 55, cy + 5), "AGENT", font=font_title_md, fill=TEXT_WHITE)

    # Breach Vectors
    vectors = [
        ("UNAUTHORIZED BASH EXEC", (220, 680), ACCENT_RED),
        ("EXTERNAL API SCAN", (860, 680), ACCENT_RED),
        ("PORT 22 PROBE: BLOCKED", (540, 1150), ACCENT_AMBER),
    ]
    for text, (vx, vy), col in vectors:
        draw.line([(cx, cy), (vx, vy)], fill=col, width=3)
        draw.rounded_rectangle([vx - 140, vy - 35, vx + 140, vy + 35], radius=10, fill=CARD_BG, outline=col, width=2)
        draw.text((vx - 120, vy - 12), text, font=font_mono_sm, fill=col)

    # Incident Log
    draw.rounded_rectangle([100, 1240, W - 100, 1390], radius=14, fill=CARD_BG, outline=ACCENT_RED, width=2)
    draw.text((130, 1260), "⚠️ RECENT INCIDENTS OF CONCERN", font=font_sub, fill=ACCENT_RED)
    draw.text((130, 1305), "• Agents probing external repositories & unassigned ports", font=font_body, fill=TEXT_WHITE)
    draw.text((130, 1345), "• Traditional software controls bypassed via emergent tool-calling", font=font_body, fill=TEXT_MUTED)

    draw_footer_card(draw, "FULL-STACK GOVERNANCE BEFORE AGENTS GO ROGUE")
    img.save(ASSETS_DIR / "shot-01.png")
    print("Saved shot-01.png")

# ==========================================
# SHOT 02: Platform Coalition & Launch
# ==========================================
def render_shot_02():
    img, draw = create_base_canvas(glow_color=VIOLET_GLOW, glow_center=(540, 940))
    draw_title_card(draw, "INDUSTRY COALITION", ACCENT_VIOLET, "OPEN AGENT SAFETY", "ENTERPRISE DEFENSE PLATFORM")
    
    # Diagram Area Y: 460 to 1420
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=(10, 15, 23), outline=CARD_BORDER, width=2)
    draw.text((100, 490), "GLOBAL ALLIANCE FOR AGENT GOVERNANCE", font=font_mono_md, fill=ACCENT_CYAN)

    # Center NVIDIA Shield
    cx, cy = 540, 780
    draw.rounded_rectangle([cx - 180, cy - 80, cx + 180, cy + 80], radius=18, fill=(24, 18, 42), outline=ACCENT_VIOLET, width=3)
    draw.text((cx - 150, cy - 45), "NVIDIA SAFETY", font=font_title_md, fill=ACCENT_CYAN)
    draw.text((cx - 140, cy + 5), "PLATFORM", font=font_title_md, fill=TEXT_WHITE)

    # Coalition Members Surrounding
    partners = [
        ("ANTHROPIC", (240, 620), ACCENT_AMBER, "Frontier Safety Alignment"),
        ("MICROSOFT", (840, 620), ACCENT_CYAN, "Azure Enterprise Stack"),
        ("CISCO", (220, 960), ACCENT_GREEN, "Network Telemetry"),
        ("SPACEX", (860, 960), TEXT_WHITE, "Mission-Critical Systems"),
    ]
    for name, (px, py), col, role in partners:
        draw.line([(cx, cy), (px, py)], fill=(45, 35, 65), width=3)
        draw.rounded_rectangle([px - 140, py - 45, px + 140, py + 45], radius=12, fill=CARD_BG, outline=col, width=2)
        draw.text((px - 110, py - 28), name, font=font_title_md, fill=col)
        draw.text((px - 120, py + 12), role, font=font_mono_sm, fill=TEXT_MUTED)

    # Jensen Huang Philosophy Card
    draw.rounded_rectangle([100, 1080, W - 100, 1380], radius=14, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((130, 1110), "ENGINEERING CONTAINMENT DOCTRINE", font=font_sub, fill=ACCENT_CYAN)
    draw.text((130, 1160), "“AI safety is primarily an engineering and datacenter", font=font_body, fill=TEXT_WHITE)
    draw.text((130, 1200), "infrastructure challenge solved through automated containment,", font=font_body, fill=TEXT_WHITE)
    draw.text((130, 1240), "rather than halting technological progress.”", font=font_body, fill=TEXT_WHITE)
    draw.text((130, 1310), "— JENSEN HUANG, NVIDIA FOUNDER & CEO", font=font_mono_sm, fill=ACCENT_VIOLET)

    draw_footer_card(draw, "UNITING FRONTIER LABS AND INFRASTRUCTURE GIANTS")
    img.save(ASSETS_DIR / "shot-02.png")
    print("Saved shot-02.png")

# ==========================================
# SHOT 03: OpenShell & Sentry BlueField DPU
# ==========================================
def render_shot_03():
    img, draw = create_base_canvas(glow_color=CYAN_GLOW, glow_center=(540, 940))
    draw_title_card(draw, "FULL-STACK ARCHITECTURE", ACCENT_CYAN, "OPENSHELL & BLUEFIELD DPU", "SOFTWARE SANDBOX • HARDWARE MONITOR")
    
    # Diagram Area Y: 460 to 1420
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=(10, 15, 23), outline=CARD_BORDER, width=2)
    draw.text((100, 490), "DUAL-TIER AGENT CONTAINMENT SYSTEM", font=font_mono_md, fill=ACCENT_CYAN)

    # TIER 1: OpenShell Software Runtime
    draw.rounded_rectangle([110, 560, W - 110, 840], radius=16, fill=(16, 26, 42), outline=ACCENT_CYAN, width=3)
    draw.rounded_rectangle([140, 580, 480, 625], radius=8, fill=(20, 38, 55), outline=ACCENT_CYAN, width=1)
    draw.text((155, 590), "TIER 1: OPENSHELL RUNTIME", font=font_mono_sm, fill=ACCENT_CYAN)
    draw.text((140, 645), "Sealed Software Workspace (Open-Source)", font=font_title_md, fill=TEXT_WHITE)
    draw.text((140, 700), "• Sandboxed tool execution & bash isolation", font=font_body, fill=TEXT_MUTED)
    draw.text((140, 740), "• Full audit tracing across model API calls", font=font_body, fill=TEXT_MUTED)
    draw.text((140, 780), "• Extensible to Arm, Intel, and AMD hosts", font=font_mono_sm, fill=ACCENT_GREEN)

    # Out-of-band communication bridge
    draw.line([(540, 840), (540, 930)], fill=ACCENT_GREEN, width=4)
    draw.polygon([(525, 925), (555, 925), (540, 950)], fill=ACCENT_GREEN)
    draw.text((560, 875), "Out-Of-Band Hardware Telemetry", font=font_mono_sm, fill=ACCENT_GREEN)

    # TIER 2: Sentry on BlueField-4 DPU
    draw.rounded_rectangle([110, 950, W - 110, 1230], radius=16, fill=(24, 18, 42), outline=ACCENT_VIOLET, width=3)
    draw.rounded_rectangle([140, 970, 480, 1015], radius=8, fill=(35, 25, 55), outline=ACCENT_VIOLET, width=1)
    draw.text((155, 980), "TIER 2: SENTRY HARDWARE DPU", font=font_mono_sm, fill=ACCENT_VIOLET)
    draw.text((140, 1035), "BlueField-4 DPU Silicon Supervisor", font=font_title_md, fill=TEXT_WHITE)
    draw.text((140, 1090), "• Operates entirely independent of host CPU/GPU", font=font_body, fill=TEXT_MUTED)
    draw.text((140, 1130), "• Tamper-proof: rogue agent cannot disable its monitor", font=font_body, fill=ACCENT_AMBER)
    draw.text((140, 1170), "• Hardware packet inspection & memory guardrails", font=font_mono_sm, fill=TEXT_WHITE)

    # Latency badge
    draw.rounded_rectangle([110, 1260, W - 110, 1380], radius=12, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((140, 1285), "REAL-TIME POLICY ENFORCEMENT", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 1330), "Millisecond-level intervention before unauthorized egress.", font=font_body, fill=ACCENT_GREEN)

    draw_footer_card(draw, "SEPARATING AGENT EXECUTION FROM SECURITY SUPERVISION")
    img.save(ASSETS_DIR / "shot-03.png")
    print("Saved shot-03.png")

# ==========================================
# SHOT 04: Out-Of-Band Hardware Quarantine
# ==========================================
def render_shot_04():
    img, draw = create_base_canvas(glow_color=(35, 25, 15), glow_center=(540, 940))
    draw_title_card(draw, "HARDWARE ENFORCEMENT", ACCENT_AMBER, "OUT-OF-BAND QUARANTINE", "SUB-5MS HARDWARE INTERLOCK")
    
    # Diagram Area Y: 460 to 1420
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=(10, 15, 23), outline=CARD_BORDER, width=2)
    draw.text((100, 490), "TAMPER-PROOF INTERVENTION MECHANISM", font=font_mono_md, fill=ACCENT_AMBER)

    # 2 Comparison Nodes
    # Left: Host CPU / Compromised Process
    draw.rounded_rectangle([110, 560, 510, 900], radius=16, fill=(28, 16, 22), outline=ACCENT_RED, width=2)
    draw.text((140, 590), "HOST WORKSTATION", font=font_sub, fill=ACCENT_RED)
    draw.text((140, 635), "Compromised Agent", font=font_title_md, fill=TEXT_WHITE)
    draw.text((140, 690), "Attempts to terminate", font=font_body, fill=TEXT_MUTED)
    draw.text((140, 725), "monitoring process...", font=font_body, fill=TEXT_MUTED)
    draw.rounded_rectangle([140, 780, 480, 850], radius=8, fill=(40, 15, 20))
    draw.text((160, 805), "❌ KILL ATTEMPT: FAILED", font=font_mono_sm, fill=ACCENT_RED)

    # Right: BlueField-4 DPU
    draw.rounded_rectangle([570, 560, 970, 900], radius=16, fill=(18, 28, 42), outline=ACCENT_GREEN, width=2)
    draw.text((600, 590), "BLUEFIELD-4 DPU", font=font_sub, fill=ACCENT_GREEN)
    draw.text((600, 635), "Sentry Hardware", font=font_title_md, fill=TEXT_WHITE)
    draw.text((600, 690), "Runs isolated on DPU", font=font_body, fill=TEXT_MUTED)
    draw.text((600, 725), "Physical PCIe separation", font=font_body, fill=TEXT_MUTED)
    draw.rounded_rectangle([600, 780, 940, 850], radius=8, fill=(15, 35, 25))
    draw.text((620, 805), "✓ STATUS: UNTOUCHABLE", font=font_mono_sm, fill=ACCENT_GREEN)

    # Big Interlock Kill-Switch Action Box
    draw.rounded_rectangle([110, 950, W - 110, 1180], radius=16, fill=(35, 20, 15), outline=ACCENT_AMBER, width=3)
    draw.text((150, 980), "⚡ HARDWARE QUARANTINE TRIGGERED", font=font_title_md, fill=ACCENT_AMBER)
    draw.text((150, 1040), "• Latency to Isolation: < 2.0 milliseconds", font=font_mono_md, fill=TEXT_WHITE)
    draw.text((150, 1085), "• Action: Physical network port severed, memory snapshot frozen", font=font_body, fill=TEXT_WHITE)
    draw.text((150, 1125), "• Host OS and production cluster remain 100% safeguarded", font=font_body, fill=ACCENT_GREEN)

    # Benefit summary
    draw.rounded_rectangle([110, 1220, W - 110, 1380], radius=12, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((140, 1250), "ENTERPRISE DEPLOYMENT BENEFIT", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 1295), "Allows organizations to deploy autonomous agent swarms with zero", font=font_body, fill=TEXT_MUTED)
    draw.text((140, 1335), "fear of unexpected rogue behavior or lateral network infection.", font=font_body, fill=TEXT_MUTED)

    draw_footer_card(draw, "ROGUE AGENTS CANNOT OVERRIDE EXTERNAL SILICON")
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
        "PRIMARY SOURCE: NVIDIA OFFICIAL NEWSROOM",
        "DATE OF RECORD: SEPTEMBER 28, 2026",
        "COMPONENTS: OPENSHELL & SENTRY BLUEFIELD-4 DPU",
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
    print("All 5 NVIDIA Agent Safety frames rendered successfully.")
