#!/usr/bin/env python3
"""Renders high-density technical visual frames for OpenAI 722 Math Proofs Short
in strict compliance with Anti-Black-Void Gate and Visual Style Bible v1.0.
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
ASSETS_DIR = Path("data/visuals/production_assets_openai_722math")
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Colors
BG_BASE = (7, 10, 15)
OPENAI_GREEN = (16, 163, 127)
MATH_CYAN = (77, 235, 255)
MATH_PURPLE = (168, 85, 247)
GRID_COLOR = (20, 30, 44)
GRID_TICK = (35, 55, 80)
TEXT_WHITE = (243, 247, 250)
TEXT_MUTED = (139, 152, 167)
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

def create_base_canvas(glow_color=(15, 35, 45), glow_center=(540, 960), glow_radius=750):
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
    draw.rounded_rectangle([90, 108, 380, 162], radius=10, fill=(18, 35, 55), outline=MATH_CYAN, width=1)
    draw.ellipse([110, 130, 122, 142], fill=MATH_CYAN)
    draw.text((135, 122), "AI NEWS FACTORY", font=font_tag, fill=TEXT_WHITE)
    draw.text((W - 390, 124), "VERIFIED INTELLIGENCE", font=font_mono_sm, fill=MATH_CYAN)
    
    return img, draw

def draw_title_card(draw, badge_text, badge_color, headline, subtitle):
    draw.rounded_rectangle([70, 220, W - 70, 420], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.rounded_rectangle([100, 245, 100 + len(badge_text) * 14 + 40, 285], radius=8, fill=(20, 30, 42), outline=badge_color, width=1)
    draw.text((120, 252), badge_text, font=font_tag, fill=badge_color)
    draw.text((100, 300), headline, font=font_title_lg, fill=TEXT_WHITE)
    draw.text((100, 365), subtitle, font=font_sub, fill=MATH_CYAN)

def draw_footer_card(draw, text):
    draw.rounded_rectangle([70, 1460, W - 70, 1560], radius=14, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((100, 1495), text, font=font_sub, fill=TEXT_MUTED)

# ==========================================
# SHOT 01: 722 AI Math Discoveries Dropped
# ==========================================
def render_shot_01():
    img, draw = create_base_canvas(glow_color=(20, 45, 35), glow_center=(540, 800))
    draw_title_card(draw, "OPENAI SCIENTIFIC RELEASE", OPENAI_GREEN, "722 AI MATH DISCOVERIES", "Published to Public GitHub Repository")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "OPEN REPOSITORY SPECIFICATION", font=font_tag, fill=MATH_CYAN)
    
    # Hero Metric Card
    draw.rounded_rectangle([110, 540, W - 110, 840], radius=16, fill=(16, 28, 24), outline=OPENAI_GREEN, width=2)
    draw.text((140, 570), "722 MANUSCRIPTS", font=font_title_lg, fill=OPENAI_GREEN)
    draw.text((140, 640), "github.com/openai/math", font=font_title_md, fill=MATH_CYAN)
    draw.text((140, 710), "• 372 Families of new mathematical results", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 765), "• Unreleased frontier reasoning model solves 4,000 open problems", font=font_mono_sm, fill=TEXT_MUTED)

    # Core Discoveries
    disc = [
        ("Number Theory & Primes", "Novel analytic bounds on prime distribution", MATH_CYAN),
        ("Kakeya & Geometric Measure", "Maximal function estimates in high dimensions", MATH_PURPLE),
        ("Lean 4 Formal Proofs", "Machine-checked formalizations for verification", ACCENT_GREEN),
    ]
    for i, (title, desc, col) in enumerate(disc):
        sy = 880 + i * 170
        draw.rounded_rectangle([110, sy, W - 110, sy + 140], radius=14, fill=(18, 24, 30), outline=col, width=2)
        draw.text((140, sy + 25), title, font=font_title_md, fill=col)
        draw.text((140, sy + 80), desc, font=font_sub, fill=TEXT_WHITE)

    draw_footer_card(draw, "Massive open-source drop accelerating pure mathematics")
    img.save(ASSETS_DIR / "shot_01.png")
    print("Rendered shot_01.png")

# ==========================================
# SHOT 02: 372 Mathematical Families
# ==========================================
def render_shot_02():
    img, draw = create_base_canvas(glow_color=(35, 20, 45), glow_center=(540, 850))
    draw_title_card(draw, "MATHEMATICAL TAXONOMY", MATH_PURPLE, "372 MATHEMATICAL FAMILIES", "Spanning Modern Theoretical Disciplines")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "DISCIPLINE BREAKDOWN", font=font_tag, fill=MATH_CYAN)
    
    categories = [
        ("Algebraic Geometry & Topology", "148 Manuscripts", "Cohomology & manifold singularity analysis", MATH_CYAN),
        ("Number Theory & Diophantine", "112 Manuscripts", "Modular forms & algebraic number fields", MATH_PURPLE),
        ("Mathematical Physics & PDE", "64 Manuscripts", "Hamiltonian systems & quantum field bounds", ACCENT_AMBER),
        ("Theoretical Computer Science", "48 Manuscripts", "Complexity classes, circuit lower bounds", ACCENT_GREEN),
    ]
    for i, (cat_name, count_str, cat_desc, col) in enumerate(categories):
        cy_pos = 540 + i * 200
        draw.rounded_rectangle([110, cy_pos, W - 110, cy_pos + 165], radius=16, fill=(18, 22, 32), outline=col, width=2)
        draw.text((140, cy_pos + 25), cat_name, font=font_title_md, fill=TEXT_WHITE)
        draw.text((W - 320, cy_pos + 25), count_str, font=font_title_md, fill=col)
        draw.text((140, cy_pos + 85), cat_desc, font=font_sub, fill=TEXT_MUTED)

    draw_footer_card(draw, "Consulted with Institute for Advanced Study mathematics advisory group")
    img.save(ASSETS_DIR / "shot_02.png")
    print("Rendered shot_02.png")

# ==========================================
# SHOT 03: 3 Hrs Reasoning • Lean Verified
# ==========================================
def render_shot_03():
    img, draw = create_base_canvas(glow_color=(15, 45, 30), glow_center=(540, 900))
    draw_title_card(draw, "TEST-TIME COMPUTE & RIGOR", ACCENT_GREEN, "3 HRS REASONING • LEAN CHECKED", "AI Intuition Meets Automated Verification")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "VERIFICATION ARCHITECTURE", font=font_tag, fill=MATH_CYAN)
    
    # Reasoning Compute Card
    draw.rounded_rectangle([110, 540, W - 110, 900], radius=16, fill=(16, 26, 22), outline=ACCENT_GREEN, width=2)
    draw.text((140, 570), "~3.0 HOURS REASONING PER PROOF", font=font_title_md, fill=ACCENT_GREEN)
    draw.text((140, 630), "Equivalent to 3 hours of continuous thinking in ChatGPT Pro", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 690), "• Thousands of hypotheses evaluated per lemma", font=font_body, fill=TEXT_MUTED)
    draw.text((140, 740), "• Test-time compute scaling overcomes reasoning barriers", font=font_body, fill=TEXT_MUTED)
    draw.rounded_rectangle([140, 810, W - 160, 860], radius=8, fill=ACCENT_GREEN)
    draw.text((160, 822), "SCALED TEST-TIME SEARCH ENGINE", font=font_mono_md, fill=BG_BASE)

    # Lean Formalization Card
    draw.rounded_rectangle([110, 940, W - 110, 1370], radius=16, fill=(20, 24, 38), outline=MATH_CYAN, width=2)
    draw.text((140, 970), "LEAN 4 INTERACTIVE THEOREM PROVER", font=font_title_md, fill=MATH_CYAN)
    draw.text((140, 1030), "Machine-checked proofs eliminate algebraic oversight", font=font_sub, fill=TEXT_WHITE)
    draw.text((140, 1090), "• Formalized in Lean 4 syntax for reproducible audit", font=font_body, fill=TEXT_WHITE)
    draw.text((140, 1140), "• Eliminates reliance on purely conversational outputs", font=font_body, fill=TEXT_MUTED)
    draw.text((140, 1190), "• International mathematicians validating results", font=font_body, fill=ACCENT_AMBER)
    draw.rounded_rectangle([140, 1260, W - 160, 1320], radius=10, fill=(20, 35, 45), outline=MATH_CYAN, width=1)
    draw.text((160, 1280), "FORMAL MATHEMATICAL RIGOR", font=font_tag, fill=MATH_CYAN)

    draw_footer_card(draw, "Combines intuitive hypothesis exploration with strict symbolic proofs")
    img.save(ASSETS_DIR / "shot_03.png")
    print("Rendered shot_03.png")

# ==========================================
# SHOT 04: New Era of Discovery
# ==========================================
def render_shot_04():
    img, draw = create_base_canvas(glow_color=(35, 25, 50), glow_center=(540, 850))
    draw_title_card(draw, "THE SCIENTIFIC REVOLUTION", MATH_PURPLE, "NEW ERA OF DISCOVERY", "Sam Altman: 'AI Accelerates Discovery'")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "SCIENTIFIC ACCELERATION IMPACT", font=font_tag, fill=MATH_CYAN)
    
    impacts = [
        ("From Tools to Collaborators", "AI moves beyond autocomplete into autonomous research", OPENAI_GREEN),
        ("Solving Unresolved Conjectures", "Formulates proofs once thought decades away", MATH_CYAN),
        ("Open-Source Science Model", "Immediate public dissemination invites global audit", MATH_PURPLE),
        ("Next: Physics & Biology", "Reasoning swarms expanding into drug design & material science", ACCENT_AMBER),
    ]
    for i, (title, desc, col) in enumerate(impacts):
        sy = 540 + i * 195
        draw.rounded_rectangle([110, sy, W - 110, sy + 160], radius=14, fill=(18, 24, 34), outline=col, width=2)
        draw.text((140, sy + 25), title, font=font_title_md, fill=col)
        draw.text((140, sy + 85), desc, font=font_sub, fill=TEXT_WHITE)

    draw_footer_card(draw, "Marks a turning point in human and machine collaborative science")
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
        
    draw.rounded_rectangle([200, 620, W - 200, 880], radius=24, fill=CARD_BG, outline=MATH_CYAN, width=3)
    draw.text((240, 660), "AI NEWS FACTORY", font=font_title_lg, fill=TEXT_WHITE)
    draw.text((310, 740), "DAILY VERIFIED INTELLIGENCE", font=font_tag, fill=MATH_CYAN)
    draw.text((275, 800), "youtube.com/@lidoailab", font=font_mono_md, fill=MATH_PURPLE)
    
    # CTA Card
    draw.rounded_rectangle([110, 1050, W - 110, 1380], radius=20, fill=(18, 25, 38), outline=CARD_BORDER, width=2)
    draw.text((150, 1090), "STAY AHEAD OF FRONTIER AI", font=font_tag, fill=ACCENT_AMBER)
    draw.text((150, 1145), "SUBSCRIBE FOR DAILY BREAKTHROUGHS", font=font_title_md, fill=TEXT_WHITE)
    draw.text((150, 1220), "• Scientific AI discoveries & proofs", font=font_sub, fill=TEXT_WHITE)
    draw.text((150, 1270), "• Frontier reasoning model analysis", font=font_sub, fill=TEXT_WHITE)
    draw.text((150, 1320), "• 100% verified, zero hype", font=font_sub, fill=ACCENT_GREEN)

    draw_footer_card(draw, "Follow @lidoailab for daily autonomous AI intelligence")
    img.save(ASSETS_DIR / "shot_05.png")
    print("Rendered shot_05.png")

def main():
    print("Rendering OpenAI 722 Math Proofs Visual Frames...")
    render_shot_01()
    render_shot_02()
    render_shot_03()
    render_shot_04()
    render_shot_05()
    print("All 5 visual frames rendered successfully!")

if __name__ == "__main__":
    main()
