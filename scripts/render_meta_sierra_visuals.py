#!/usr/bin/env python3
"""Renders high-density technical visual frames for Meta Sierra Personal Agent Protocol Short
in strict compliance with Anti-Black-Void Gate and Visual Style Bible v1.0.
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
ASSETS_DIR = Path("data/visuals/production_assets_meta_sierra")
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Colors
BG_BASE = (7, 10, 15)
META_BLUE = (0, 100, 224)
SIERRA_PURPLE = (147, 51, 234)
STRIPE_VIOLET = (99, 91, 255)
GRID_COLOR = (20, 30, 44)
GRID_TICK = (35, 55, 80)
TEXT_WHITE = (243, 247, 250)
TEXT_MUTED = (139, 152, 167)
ACCENT_CYAN = (77, 235, 255)
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
# SHOT 01: Personal Agent Protocol Launched
# ==========================================
def render_shot_01():
    img, draw = create_base_canvas(glow_color=(15, 30, 60), glow_center=(540, 800))
    draw_title_card(draw, "OPEN AGENT STANDARD", ACCENT_CYAN, "PERSONAL AGENT PROTOCOL", "Meta & Sierra Open Handshake Standard")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "PROTOCOL SPECIFICATION v0.1", font=font_tag, fill=ACCENT_CYAN)
    
    # Hero Architecture Card
    draw.rounded_rectangle([110, 540, W - 110, 840], radius=16, fill=(18, 24, 38), outline=META_BLUE, width=2)
    draw.text((140, 570), "PERSONAL AGENT PROTOCOL (PAP)", font=font_title_md, fill=ACCENT_CYAN)
    draw.text((140, 630), "Open OAuth-Based Agent-to-Business Handshake", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 690), "• Replaces fragile screen scraping with verified tokens", font=font_body, fill=ACCENT_GREEN)
    draw.text((140, 740), "• Establishes session-based identity & scope security", font=font_body, fill=TEXT_MUTED)
    draw.rounded_rectangle([140, 785, 380, 825], radius=6, fill=(20, 35, 50), outline=ACCENT_CYAN, width=1)
    draw.text((160, 795), "OAUTH 2.0 EXTENSION", font=font_tag, fill=ACCENT_CYAN)

    # Core Features
    feats = [
        ("Cryptographic Authentication", "Validates legitimate personal AI agents vs unauthorized bots", META_BLUE),
        ("Granular Scopes", "Read-only inventory vs authorized live write checkouts", SIERRA_PURPLE),
        ("Multi-Transport Support", "Operates over HTTP, WebSockets, OpenAPI, and MCP", ACCENT_GREEN),
    ]
    for i, (title, desc, col) in enumerate(feats):
        sy = 880 + i * 170
        draw.rounded_rectangle([110, sy, W - 110, sy + 140], radius=14, fill=(16, 22, 32), outline=col, width=2)
        draw.text((140, sy + 25), title, font=font_title_md, fill=col)
        draw.text((140, sy + 80), desc, font=font_sub, fill=TEXT_WHITE)

    draw_footer_card(draw, "Establishes the foundational protocol layer for the autonomous agent web")
    img.save(ASSETS_DIR / "shot_01.png")
    print("Rendered shot_01.png")

# ==========================================
# SHOT 02: OAuth Handshake • No Scraping
# ==========================================
def render_shot_02():
    img, draw = create_base_canvas(glow_color=(35, 20, 45), glow_center=(540, 850))
    draw_title_card(draw, "SECURITY ARCHITECTURE", SIERRA_PURPLE, "OAUTH HANDSHAKE • NO SCRAPING", "Structured Agent Authentication Loop")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "HANDSHAKE vs LEGACY SCRAPING", font=font_tag, fill=ACCENT_CYAN)
    
    # 2 Comparison Panels
    # Legacy
    draw.rounded_rectangle([110, 540, W - 110, 890], radius=16, fill=(28, 18, 22), outline=ACCENT_RED, width=2)
    draw.text((140, 570), "LEGACY AGENTS (BRUTE-FORCE SCRAPING)", font=font_title_md, fill=ACCENT_RED)
    draw.text((140, 630), "• Scrapes arbitrary DOM elements blindly", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 680), "• High failure rate on UI updates and Captchas", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 730), "• Triggers anti-bot rate limits and security blocks", font=font_body, fill=TEXT_MUTED)
    draw.rounded_rectangle([140, 810, 320, 855], radius=8, fill=ACCENT_RED)
    draw.text((160, 822), "UNRELIABLE & RISKY", font=font_tag, fill=BG_BASE)

    # PAP Handshake
    draw.rounded_rectangle([110, 930, W - 110, 1370], radius=16, fill=(18, 26, 38), outline=ACCENT_GREEN, width=2)
    draw.text((140, 960), "PERSONAL AGENT PROTOCOL (STRUCTURED)", font=font_title_md, fill=ACCENT_GREEN)
    draw.text((140, 1020), "• Declares identity via verified OAuth tokens", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 1070), "• Direct JSON-RPC / API inventory querying", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 1120), "• 100% Deterministic business integration", font=font_body, fill=ACCENT_CYAN)
    draw.text((140, 1170), "• Zero brittle HTML parsing or guesswork", font=font_body, fill=TEXT_MUTED)
    draw.rounded_rectangle([140, 1260, W - 160, 1320], radius=10, fill=(20, 45, 30), outline=ACCENT_GREEN, width=1)
    draw.text((160, 1280), "STANDARDIZED API INTERFACE", font=font_tag, fill=ACCENT_GREEN)

    draw_footer_card(draw, "Transforms fragile web scraping into cryptographically verified commerce")
    img.save(ASSETS_DIR / "shot_02.png")
    print("Rendered shot_02.png")

# ==========================================
# SHOT 03: Granular Access Controls
# ==========================================
def render_shot_03():
    img, draw = create_base_canvas(glow_color=(20, 40, 35), glow_center=(540, 900))
    draw_title_card(draw, "PERMISSION SCOPES", ACCENT_GREEN, "GRANULAR ACCESS CONTROLS", "Explicit User Authorization Boundaries")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "PERMISSION TIER HIERARCHY", font=font_tag, fill=ACCENT_CYAN)
    
    scopes = [
        ("Tier 1: Read-Only Browse", "scope: browse.inventory", "Check product stock, price, dimensions, policies", ACCENT_CYAN),
        ("Tier 2: User Preference Sync", "scope: cart.manage", "Save items, track wishlist, compare carts", ACCENT_AMBER),
        ("Tier 3: Write Commerce Action", "scope: checkout.execute", "Pre-authorized token checkout up to set dollar limit", ACCENT_GREEN),
        ("Tier 4: Enterprise Delegation", "scope: support.delegate", "Hand off complex tasks to merchant enterprise AI", SIERRA_PURPLE),
    ]
    for i, (stitle, sscope, sdesc, col) in enumerate(scopes):
        sy = 540 + i * 200
        draw.rounded_rectangle([110, sy, W - 110, sy + 165], radius=14, fill=(18, 24, 30), outline=col, width=2)
        draw.text((140, sy + 25), stitle, font=font_title_md, fill=col)
        draw.text((140, sy + 75), sscope, font=font_mono_sm, fill=TEXT_MUTED)
        draw.text((140, sy + 115), sdesc, font=font_body, fill=TEXT_WHITE)

    draw_footer_card(draw, "Consumers remain in full control over what their agents can buy or inspect")
    img.save(ASSETS_DIR / "shot_03.png")
    print("Rendered shot_03.png")

# ==========================================
# SHOT 04: Walmart • Shopify • Stripe
# ==========================================
def render_shot_04():
    img, draw = create_base_canvas(glow_color=(30, 25, 55), glow_center=(540, 850))
    draw_title_card(draw, "COMMERCE COALITION", STRIPE_VIOLET, "WALMART • SHOPIFY • STRIPE", "Global Retail & Payment Infrastructure")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "FOUNDING ADOPTION PARTNERS", font=font_tag, fill=ACCENT_CYAN)
    
    partners = [
        ("Walmart", "World's largest retailer enabling automated grocery & pantry restocking", ACCENT_AMBER),
        ("Shopify", "Millions of independent storefronts accepting agent checkouts", ACCENT_GREEN),
        ("Stripe", "Global payment rails powering secure agentic financial transactions", STRIPE_VIOLET),
        ("Meta & Sierra", "Powering consumer agent interfaces from glasses to enterprise bots", META_BLUE),
    ]
    for i, (pname, pdesc, col) in enumerate(partners):
        py_pos = 540 + i * 195
        draw.rounded_rectangle([110, py_pos, W - 110, py_pos + 160], radius=14, fill=(18, 22, 34), outline=col, width=2)
        draw.text((140, py_pos + 25), pname, font=font_title_md, fill=col)
        draw.text((140, py_pos + 85), pdesc, font=font_sub, fill=TEXT_WHITE)

    draw_footer_card(draw, "Unifies top retailers and payment rails into a cohesive autonomous economy")
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
    draw.text((275, 800), "youtube.com/@lidoailab", font=font_mono_md, fill=STRIPE_VIOLET)
    
    # CTA Card
    draw.rounded_rectangle([110, 1050, W - 110, 1380], radius=20, fill=(18, 25, 38), outline=CARD_BORDER, width=2)
    draw.text((150, 1090), "STAY AHEAD OF FRONTIER AI", font=font_tag, fill=ACCENT_AMBER)
    draw.text((150, 1145), "SUBSCRIBE FOR DAILY BREAKTHROUGHS", font=font_title_md, fill=TEXT_WHITE)
    draw.text((150, 1220), "• Autonomous agent architecture standards", font=font_sub, fill=TEXT_WHITE)
    draw.text((150, 1270), "• Multi-agent commerce protocols & APIs", font=font_sub, fill=TEXT_WHITE)
    draw.text((150, 1320), "• 100% verified, zero hype", font=font_sub, fill=ACCENT_GREEN)

    draw_footer_card(draw, "Follow @lidoailab for daily autonomous AI intelligence")
    img.save(ASSETS_DIR / "shot_05.png")
    print("Rendered shot_05.png")

def main():
    print("Rendering Meta Sierra Personal Agent Protocol Visual Frames...")
    render_shot_01()
    render_shot_02()
    render_shot_03()
    render_shot_04()
    render_shot_05()
    print("All 5 visual frames rendered successfully!")

if __name__ == "__main__":
    main()
