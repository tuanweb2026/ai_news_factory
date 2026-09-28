#!/usr/bin/env python3
"""Renders high-density technical visual frames for NVIDIA PAIR Short in strict compliance with
Anti-Black-Void Gate and Visual Style Bible v1.0.
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
ASSETS_DIR = Path("data/visuals/production_assets_pair")
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

font_title_lg = get_font(FONT_BOLD, 54)
font_title_md = get_font(FONT_BOLD, 42)
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
    # Safe zone container: Y 220 to 420
    draw.rounded_rectangle([70, 220, W - 70, 420], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=2)
    # Badge
    draw.rounded_rectangle([100, 245, 100 + len(badge_text) * 14 + 40, 285], radius=8, fill=(20, 30, 42), outline=badge_color, width=1)
    draw.text((120, 252), badge_text, font=font_tag, fill=badge_color)
    # Headline
    draw.text((100, 300), headline, font=font_title_lg, fill=TEXT_WHITE)
    # Subtitle
    draw.text((100, 365), subtitle, font=font_sub, fill=ACCENT_CYAN)

def draw_footer_card(draw, text):
    draw.rounded_rectangle([70, 1460, W - 70, 1560], radius=14, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((100, 1495), text, font=font_sub, fill=TEXT_MUTED)

# ==========================================
# SHOT 01: Central Dispatch Cluster
# ==========================================
def render_shot_01():
    img, draw = create_base_canvas(glow_color=CYAN_GLOW, glow_center=(540, 940))
    draw_title_card(draw, "APACHE 2.0 • OPEN SOURCE", ACCENT_GREEN, "NVIDIA PAIR", "DISTRIBUTED AI ROUTER")
    
    # Diagram Area Y: 460 to 1420
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=(10, 15, 23), outline=CARD_BORDER, width=2)
    draw.text((100, 490), "LOCAL TOPOLOGY ARCHITECTURE", font=font_mono_md, fill=ACCENT_CYAN)
    
    # Central Developer Hub Node
    hub_x, hub_y = 540, 900
    # Outer radar rings
    for r in [280, 200, 130]:
        draw.ellipse([hub_x - r, hub_y - r, hub_x + r, hub_y + r], outline=(25, 45, 65), width=2)
    
    # 3 Satellite Nodes
    nodes = [
        {"name": "RTX 4090 DESKTOP", "sub": "24GB VRAM", "pos": (240, 720), "color": ACCENT_CYAN},
        {"name": "DGX SPARK NODE", "sub": "CLUSTER ACCEL", "pos": (840, 720), "color": ACCENT_VIOLET},
        {"name": "M4 MAC STUDIO", "sub": "APPLE SILICON", "pos": (540, 1220), "color": ACCENT_GREEN},
    ]
    
    # Connecting Lines with Data Packets
    for n in nodes:
        nx, ny = n["pos"]
        draw.line([(hub_x, hub_y), (nx, ny)], fill=n["color"], width=3)
        # Midpoint packet
        mx, my = (hub_x + nx) // 2, (hub_y + ny) // 2
        draw.ellipse([mx - 12, my - 12, mx + 12, my + 12], fill=n["color"])
        
        # Satellite card
        w_box, h_box = 240, 100
        draw.rounded_rectangle([nx - w_box//2, ny - h_box//2, nx + w_box//2, ny + h_box//2], radius=12, fill=CARD_BG, outline=n["color"], width=2)
        draw.text((nx - 100, ny - 30), n["name"], font=font_tag, fill=TEXT_WHITE)
        draw.text((nx - 100, ny + 5), n["sub"], font=font_mono_sm, fill=n["color"])

    # Center Hub Icon
    draw.ellipse([hub_x - 70, hub_y - 70, hub_x + 70, hub_y + 70], fill=(16, 28, 44), outline=ACCENT_CYAN, width=3)
    draw.text((hub_x - 45, hub_y - 25), "PAIR", font=font_title_md, fill=ACCENT_CYAN)
    draw.text((hub_x - 40, hub_y + 15), "HUB", font=font_tag, fill=TEXT_WHITE)

    # Telemetry Bar
    draw.rounded_rectangle([100, 1340, W - 100, 1395], radius=10, fill=(15, 22, 32), outline=CARD_BORDER, width=1)
    draw.text((120, 1355), "DISCOVERY: mDNS • LATENCY: < 2ms • ZERO CLOUD EGRESS", font=font_mono_sm, fill=TEXT_MUTED)

    draw_footer_card(draw, "CONVERT HOME HARDWARE INTO DISTRIBUTED CLUSTER")
    img.save(ASSETS_DIR / "shot-01.png")
    print("Saved shot-01.png")

# ==========================================
# SHOT 02: Hardware Discovery
# ==========================================
def render_shot_02():
    img, draw = create_base_canvas(glow_color=VIOLET_GLOW, glow_center=(540, 940))
    draw_title_card(draw, "HARDWARE DISCOVERY", ACCENT_CYAN, "RTX & APPLE SILICON", "AUTOMATIC mDNS DETECTION")
    
    # Diagram Area Y: 460 to 1420
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=(10, 15, 23), outline=CARD_BORDER, width=2)
    draw.text((100, 490), "DETECTED COMPUTE NODES (LAN)", font=font_mono_md, fill=ACCENT_CYAN)

    hardware_cards = [
        {
            "y": 550,
            "title": "NVIDIA GEFORCE RTX 4090",
            "badge": "CUDA / TENSOR CORES",
            "specs": "24GB GDDR6X • OLLAMA ENGINE",
            "load": "83% CAPACITY",
            "bar_w": 420,
            "color": ACCENT_CYAN
        },
        {
            "y": 830,
            "title": "NVIDIA DGX SPARK NODE",
            "badge": "ENTERPRISE ACCELERATOR",
            "specs": "TURING & HOPPER ARCH • LOW NOISE",
            "load": "64% CAPACITY",
            "bar_w": 320,
            "color": ACCENT_VIOLET
        },
        {
            "y": 1110,
            "title": "APPLE M4 MAX MAC STUDIO",
            "badge": "APPLE SILICON / METAL",
            "specs": "128GB UNIFIED MEMORY • LM STUDIO",
            "load": "42% CAPACITY",
            "bar_w": 210,
            "color": ACCENT_GREEN
        }
    ]

    for c in hardware_cards:
        y = c["y"]
        draw.rounded_rectangle([100, y, W - 100, y + 240], radius=14, fill=CARD_BG, outline=c["color"], width=2)
        # Title & badge
        draw.text((130, y + 25), c["title"], font=font_title_md, fill=TEXT_WHITE)
        draw.rounded_rectangle([W - 380, y + 25, W - 130, y + 65], radius=6, fill=(18, 25, 38), outline=c["color"], width=1)
        draw.text((W - 365, y + 33), c["badge"], font=font_mono_sm, fill=c["color"])
        # Specs
        draw.text((130, y + 85), c["specs"], font=font_body, fill=TEXT_MUTED)
        # Load meter
        draw.text((130, y + 130), f"STATUS: ONLINE  •  LOAD: {c['load']}", font=font_mono_sm, fill=c["color"])
        # Background bar
        draw.rounded_rectangle([130, y + 165, W - 130, y + 195], radius=8, fill=(20, 28, 40))
        # Active bar
        draw.rounded_rectangle([130, y + 165, 130 + c["bar_w"], y + 195], radius=8, fill=c["color"])

    draw_footer_card(draw, "CROSS-PLATFORM: WINDOWS, LINUX & MACOS SUPPORTED")
    img.save(ASSETS_DIR / "shot-02.png")
    print("Saved shot-02.png")

# ==========================================
# SHOT 03: Load Balancer
# ==========================================
def render_shot_03():
    img, draw = create_base_canvas(glow_color=CYAN_GLOW, glow_center=(540, 940))
    draw_title_card(draw, "RUNTIME MECHANISM", ACCENT_AMBER, "SMART LOAD BALANCER", "DYNAMIC INFERENCE SCHEDULING")
    
    # Diagram Area Y: 460 to 1420
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=(10, 15, 23), outline=CARD_BORDER, width=2)
    draw.text((100, 490), "DISCRETE QUERY ROUTING PIPELINE", font=font_mono_md, fill=ACCENT_CYAN)

    # Top Incoming Swarm Box
    draw.rounded_rectangle([160, 560, W - 160, 680], radius=14, fill=CARD_BG, outline=ACCENT_AMBER, width=2)
    draw.text((200, 580), "MULTI-AGENT SWARM INCOMING QUERIES", font=font_sub, fill=ACCENT_AMBER)
    draw.text((200, 625), "Task #1: Code Synthesis • Task #2: Data Analysis • Task #3: Translation", font=font_mono_sm, fill=TEXT_WHITE)

    # Arrow down
    draw.line([(540, 680), (540, 750)], fill=ACCENT_AMBER, width=4)
    draw.polygon([(525, 745), (555, 745), (540, 770)], fill=ACCENT_AMBER)

    # Center Router Box
    draw.rounded_rectangle([120, 770, W - 120, 930], radius=16, fill=(16, 26, 42), outline=ACCENT_CYAN, width=3)
    draw.text((160, 795), "PAIR INFERENCE PROXY (PORT 11434 / 8080)", font=font_title_md, fill=ACCENT_CYAN)
    draw.text((160, 850), "• Model Availability Match: PASS", font=font_mono_sm, fill=TEXT_WHITE)
    draw.text((160, 880), "• Dynamic Load Balancing: LEAST BUSY NODE", font=font_mono_sm, fill=ACCENT_GREEN)

    # 3 Branch Lines
    workers = [
        {"x": 220, "name": "WORKER 1: RTX 4090", "engine": "Ollama (Qwen-2.5-Coder)", "speed": "84 tok/s", "col": ACCENT_CYAN},
        {"x": 540, "name": "WORKER 2: DGX SPARK", "engine": "LM Studio (Llama-3.3-70B)", "speed": "52 tok/s", "col": ACCENT_VIOLET},
        {"x": 860, "name": "WORKER 3: M4 STUDIO", "engine": "Ollama (DeepSeek-V2.5)", "speed": "68 tok/s", "col": ACCENT_GREEN},
    ]

    for w in workers:
        wx = w["x"]
        draw.line([(540, 930), (wx, 1030)], fill=w["col"], width=3)
        # Worker card
        draw.rounded_rectangle([wx - 140, 1030, wx + 140, 1310], radius=12, fill=CARD_BG, outline=w["col"], width=2)
        draw.text((wx - 120, 1055), w["name"][:16], font=font_tag, fill=TEXT_WHITE)
        draw.text((wx - 120, 1085), w["name"][17:], font=font_tag, fill=TEXT_WHITE)
        draw.line([(wx - 120, 1125), (wx + 120, 1125)], fill=(30, 45, 65), width=1)
        draw.text((wx - 120, 1145), "Engine:", font=font_mono_sm, fill=TEXT_MUTED)
        draw.text((wx - 120, 1175), w["engine"][:14], font=font_mono_sm, fill=w["col"])
        draw.text((wx - 120, 1205), w["engine"][14:], font=font_mono_sm, fill=w["col"])
        draw.text((wx - 120, 1250), w["speed"], font=font_sub, fill=ACCENT_GREEN)

    # Status ribbon
    draw.rounded_rectangle([100, 1340, W - 100, 1395], radius=10, fill=(15, 22, 32), outline=CARD_BORDER, width=1)
    draw.text((120, 1355), "ZERO QUEUE BOTTLENECKS  •  CONTINUOUS MULTI-AGENT INFERENCE", font=font_mono_sm, fill=TEXT_WHITE)

    draw_footer_card(draw, "OPENAI & OLLAMA COMPATIBLE • ZERO HARNESS CHANGES")
    img.save(ASSETS_DIR / "shot-03.png")
    print("Saved shot-03.png")

# ==========================================
# SHOT 04: Privacy & Negative Boundary
# ==========================================
def render_shot_04():
    img, draw = create_base_canvas(glow_color=CYAN_GLOW, glow_center=(540, 940))
    draw_title_card(draw, "CRITICAL BOUNDARY & SECURITY", ACCENT_GREEN, "100% LOCAL PRIVACY", "NO VRAM POOLING • ZERO CLOUD")
    
    # Diagram Area Y: 460 to 1420
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=(10, 15, 23), outline=CARD_BORDER, width=2)
    draw.text((100, 490), "LAN ISOLATION & MODEL INTEGRITY", font=font_mono_md, fill=ACCENT_GREEN)

    # Perimeter Green Box (Secure LAN)
    draw.rounded_rectangle([100, 550, W - 100, 1080], radius=16, fill=(12, 22, 28), outline=ACCENT_GREEN, width=3)
    draw.text((130, 575), "ENCRYPTED HOME LAN BOUNDARY (mDNS)", font=font_sub, fill=ACCENT_GREEN)

    # 2 Standalone Node Diagrams
    draw.rounded_rectangle([130, 630, 520, 860], radius=12, fill=CARD_BG, outline=ACCENT_CYAN, width=2)
    draw.text((150, 650), "NODE 1: FULL MODEL", font=font_sub, fill=TEXT_WHITE)
    draw.text((150, 695), "100% Weights Resident", font=font_mono_sm, fill=ACCENT_CYAN)
    draw.text((150, 735), "Discrete Query Processing", font=font_body, fill=TEXT_MUTED)
    draw.text((150, 785), "STATUS: INDEPENDENT", font=font_mono_sm, fill=ACCENT_GREEN)

    draw.rounded_rectangle([560, 630, 950, 860], radius=12, fill=CARD_BG, outline=ACCENT_VIOLET, width=2)
    draw.text((580, 650), "NODE 2: FULL MODEL", font=font_sub, fill=TEXT_WHITE)
    draw.text((580, 695), "100% Weights Resident", font=font_mono_sm, fill=ACCENT_VIOLET)
    draw.text((580, 735), "Discrete Query Processing", font=font_body, fill=TEXT_MUTED)
    draw.text((580, 785), "STATUS: INDEPENDENT", font=font_mono_sm, fill=ACCENT_GREEN)

    # CRITICAL BOUNDARY CALLOUT
    draw.rounded_rectangle([130, 890, 950, 1040], radius=12, fill=(25, 15, 20), outline=ACCENT_RED, width=2)
    draw.text((160, 915), "NEGATIVE BOUNDARY ENFORCEMENT:", font=font_sub, fill=ACCENT_RED)
    draw.text((160, 960), "❌ NO VRAM Pooling across machines", font=font_mono_md, fill=TEXT_WHITE)
    draw.text((160, 995), "❌ NO Tensor Model Sharding over LAN", font=font_mono_md, fill=TEXT_WHITE)

    # BLOCKED CLOUD EGRESS
    draw.rounded_rectangle([100, 1120, W - 100, 1310], radius=14, fill=(24, 16, 20), outline=ACCENT_RED, width=3)
    draw.text((140, 1145), "EXTERNAL INTERNET & PUBLIC CLOUD", font=font_title_md, fill=ACCENT_RED)
    draw.text((140, 1205), "⛔ OUTBOUND EGRESS: BLOCKED (0 BYTES)", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 1250), "All agent prompts, outputs & telemetry strictly on-device.", font=font_body, fill=TEXT_MUTED)

    # Shield Badge
    draw.rounded_rectangle([100, 1340, W - 100, 1395], radius=10, fill=(15, 25, 22), outline=ACCENT_GREEN, width=1)
    draw.text((120, 1355), "SHIELD VERIFIED: 100% AIR-GAPPED DATA SOVEREIGNTY", font=font_mono_sm, fill=ACCENT_GREEN)

    draw_footer_card(draw, "ZERO CLOUD RISK • ZERO SUBSCRIPTION COSTS")
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

    # 3 Summary Tags
    specs = [
        "PRIMARY SOURCE: NVIDIA GITHUB & OFFICIAL RELEASE",
        "LICENSE: APACHE 2.0 OPEN-SOURCE COMPLIANT",
        "DEVICE SUPPORT: RTX 20+ & APPLE SILICON M4+",
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
    print("All 5 frames rendered successfully.")
