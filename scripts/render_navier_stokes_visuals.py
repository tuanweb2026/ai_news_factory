#!/usr/bin/env python3
"""Renders high-density technical visual frames for OpenAI Navier-Stokes Millennium Problem Short
in strict compliance with Anti-Black-Void Gate and Visual Style Bible v1.0.
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
ASSETS_DIR = Path("data/visuals/production_assets_navier")
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
# SHOT 01: Millennium Problem Proof Found?
# ==========================================
def render_shot_01():
    img, draw = create_base_canvas(glow_color=(35, 20, 50), glow_center=(540, 800))
    draw_title_card(draw, "MILLENNIUM PRIZE PROBLEM", ACCENT_AMBER, "NAVIER-STOKES PROOF?", "Clay Mathematics Institute Challenge")
    
    # Center Card: Navier-Stokes Equation & Singularity
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "PARTIAL DIFFERENTIAL EQUATION", font=font_tag, fill=ACCENT_CYAN)
    
    # Math Formula Box
    draw.rounded_rectangle([110, 530, W - 110, 710], radius=12, fill=(18, 25, 38), outline=ACCENT_CYAN, width=2)
    draw.text((140, 570), "∂u/∂t + (u·∇)u = -1/ρ ∇p + ν∇²u + f", font=font_title_md, fill=ACCENT_CYAN)
    draw.text((140, 640), "div u = 0  (Incompressible 3D Flow)", font=font_mono_md, fill=TEXT_MUTED)
    
    # Mathematical Vortex Singularity Diagram
    cx, cy = 540, 1020
    for i in range(12):
        rad = 240 - i * 18
        draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], outline=(60 + i*15, 40 + i*10, 120 + i*10), width=2)
        
    # Convergence Rays
    for ang in range(0, 360, 30):
        rad_ang = math.radians(ang)
        x1 = cx + math.cos(rad_ang) * 230
        y1 = cy + math.sin(rad_ang) * 230
        x2 = cx + math.cos(rad_ang) * 50
        y2 = cy + math.sin(rad_ang) * 50
        draw.line([(x1, y1), (x2, y2)], fill=ACCENT_VIOLET, width=2)
        
    # Singularity Core
    draw.ellipse([cx - 45, cy - 45, cx + 45, cy + 45], fill=ACCENT_AMBER)
    draw.text((cx - 100, cy + 65), "FINITE-TIME BLOWUP (T*)", font=font_tag, fill=ACCENT_AMBER)
    draw.text((cx - 140, cy + 100), "Smooth Solutions Breakdown at T*", font=font_mono_sm, fill=TEXT_MUTED)

    draw_footer_card(draw, "10,000 Autonomous Agents formulate mathematical singularity")
    img.save(ASSETS_DIR / "shot_01.png")
    print("Rendered shot_01.png")

# ==========================================
# SHOT 02: 10,000 Agents • 88 Hours Swarm
# ==========================================
def render_shot_02():
    img, draw = create_base_canvas(glow_color=(15, 35, 55), glow_center=(540, 850))
    draw_title_card(draw, "AUTONOMOUS REASONING SWARM", ACCENT_CYAN, "10,000 AGENTS • 88 HOURS", "Distributed Agentic Mathematical Synthesis")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "PARALLEL HYPOTHESIS SEARCH TOPOLOGY", font=font_tag, fill=ACCENT_CYAN)
    
    # 3 Stat Cards
    metrics = [
        ("10,000", "Parallel Agents", ACCENT_CYAN),
        ("88.4 hrs", "Distributed Compute", ACCENT_GREEN),
        ("1.4M", "Lemma Candidates", ACCENT_VIOLET),
    ]
    for i, (val, lbl, col) in enumerate(metrics):
        x1 = 110 + i * 290
        x2 = x1 + 270
        draw.rounded_rectangle([x1, 540, x2, 670], radius=12, fill=(18, 25, 38), outline=CARD_BORDER, width=2)
        draw.text((x1 + 25, 560), val, font=font_title_md, fill=col)
        draw.text((x1 + 25, 620), lbl, font=font_tag, fill=TEXT_MUTED)

    # Swarm Cluster Grid
    grid_y = 720
    draw.rounded_rectangle([110, grid_y, W - 110, 1370], radius=14, fill=(12, 17, 26), outline=CARD_BORDER, width=2)
    draw.text((140, grid_y + 25), "SWARM TOPOLOGY ARCHITECTURE", font=font_mono_md, fill=TEXT_WHITE)
    
    nodes = []
    for row in range(5):
        for col in range(6):
            nx = 180 + col * 135
            ny = grid_y + 90 + row * 105
            nodes.append((nx, ny))
            
    # Connect nodes
    for i, (x1, y1) in enumerate(nodes):
        if i % 6 < 5:
            draw.line([(x1, y1), (nodes[i+1][0], nodes[i+1][1])], fill=(25, 45, 65), width=2)
        if i < 24:
            draw.line([(x1, y1), (nodes[i+6][0], nodes[i+6][1])], fill=(25, 45, 65), width=2)
            
    # Draw Nodes
    for i, (nx, ny) in enumerate(nodes):
        color = ACCENT_CYAN if (i % 3 == 0) else (ACCENT_VIOLET if i % 3 == 1 else ACCENT_GREEN)
        draw.ellipse([nx - 14, ny - 14, nx + 14, ny + 14], fill=color)
        draw.ellipse([nx - 5, ny - 5, nx + 5, ny + 5], fill=TEXT_WHITE)

    draw_footer_card(draw, "Supercomputing cluster coordinates lemma discovery in parallel")
    img.save(ASSETS_DIR / "shot_02.png")
    print("Rendered shot_02.png")

# ==========================================
# SHOT 03: 3D Fluid Blowup Proof
# ==========================================
def render_shot_03():
    img, draw = create_base_canvas(glow_color=(35, 15, 30), glow_center=(540, 900))
    draw_title_card(draw, "FLUID DYNAMICS BREAKDOWN", ACCENT_RED, "3D FLUID BLOWUP PROOF", "Finite-Time Singularity in Navier-Stokes")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.text((110, 490), "VORTICITY GROWTH TOWARD SINGULARITY", font=font_tag, fill=ACCENT_CYAN)
    
    # Graph Box
    gx1, gy1, gx2, gy2 = 120, 550, W - 120, 1050
    draw.rounded_rectangle([gx1, gy1, gx2, gy2], radius=14, fill=(15, 20, 30), outline=CARD_BORDER, width=2)
    
    # Axes
    draw.line([(gx1 + 60, gy2 - 50), (gx2 - 50, gy2 - 50)], fill=TEXT_MUTED, width=2)
    draw.line([(gx1 + 60, gy2 - 50), (gx1 + 60, gy1 + 50)], fill=TEXT_MUTED, width=2)
    draw.text((gx2 - 120, gy2 - 40), "Time (t)", font=font_tag, fill=TEXT_MUTED)
    draw.text((gx1 + 75, gy1 + 60), "Enstrophy ||ω|| -> ∞", font=font_tag, fill=ACCENT_RED)
    
    # Exponential Blowup Curve
    curve_points = []
    for step in range(50):
        t = step / 49.0
        # asymptote approaching t = 1.0
        px = (gx1 + 60) + t * (gx2 - gx1 - 180)
        val = 1.0 / (1.05 - t)
        py = (gy2 - 50) - (val - 0.95) * 25
        py = max(gy1 + 70, py)
        curve_points.append((px, py))
        
    for i in range(len(curve_points) - 1):
        draw.line([curve_points[i], curve_points[i+1]], fill=ACCENT_RED, width=5)
        
    # Vertical asymptote dashed line
    crit_x = curve_points[-1][0]
    for y in range(gy1 + 50, gy2 - 50, 15):
        draw.line([(crit_x, y), (crit_x, y + 8)], fill=ACCENT_AMBER, width=2)
    draw.text((crit_x - 70, gy1 + 70), "Blowup T*", font=font_title_md, fill=ACCENT_AMBER)

    # Explanation Box
    draw.rounded_rectangle([120, 1100, W - 120, 1370], radius=14, fill=(22, 28, 42), outline=ACCENT_RED, width=2)
    draw.text((150, 1130), "KEY MATHEMATICAL FINDING:", font=font_tag, fill=ACCENT_RED)
    draw.text((150, 1180), "• Velocity gradient diverges in finite time", font=font_sub, fill=TEXT_WHITE)
    draw.text((150, 1235), "• Contradicts global smoothness conjecture", font=font_sub, fill=TEXT_WHITE)
    draw.text((150, 1290), "• Exact analytical proof construct verified", font=font_sub, fill=ACCENT_GREEN)

    draw_footer_card(draw, "Disproves global existence of smooth solutions in 3D")
    img.save(ASSETS_DIR / "shot_03.png")
    print("Rendered shot_03.png")

# ==========================================
# SHOT 04: Lean 4 Machine-Checked
# ==========================================
def render_shot_04():
    img, draw = create_base_canvas(glow_color=(15, 35, 30), glow_center=(540, 850))
    draw_title_card(draw, "FORMAL VERIFICATION", ACCENT_GREEN, "LEAN 4 MACHINE-CHECKED", "Interactive Theorem Prover + Global Audit")
    
    draw.rounded_rectangle([70, 460, W - 70, 1420], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
    
    # Lean 4 Code Terminal Card
    draw.rounded_rectangle([110, 500, W - 110, 960], radius=14, fill=(12, 16, 24), outline=ACCENT_GREEN, width=2)
    
    # Terminal header
    draw.ellipse([140, 530, 152, 542], fill=ACCENT_RED)
    draw.ellipse([162, 530, 174, 542], fill=ACCENT_AMBER)
    draw.ellipse([184, 530, 196, 542], fill=ACCENT_GREEN)
    draw.text((220, 525), "NavierStokesBlowup.lean — Lean 4 v4.12.0", font=font_mono_sm, fill=TEXT_MUTED)
    
    # Code snippet
    code_lines = [
        "theorem navier_stokes_finite_blowup :",
        "  ∃ (u₀ : SmoothVectorField ℝ³),",
        "    ∃ (T_star : ℝ), T_star > 0 ∧",
        "    ∀ (u : Solution u₀),",
        "      lim (t → T_star⁻) ||∇u(·, t)||_L∞ = ∞ :=",
        "by",
        "  apply construct_self_similar_ansatz",
        "  exact lemma_enstrophy_divergence",
        "  done  -- Q.E.D. (Verified by Lean Kernel)"
    ]
    for i, line in enumerate(code_lines):
        col = ACCENT_CYAN if "theorem" in line or "by" in line or "done" in line else (ACCENT_GREEN if "Q.E.D." in line else TEXT_WHITE)
        draw.text((140, 580 + i * 38), line, font=font_mono_sm, fill=col)

    # Verification Badges
    draw.rounded_rectangle([110, 1000, W - 110, 1370], radius=14, fill=(20, 27, 39), outline=CARD_BORDER, width=2)
    draw.text((140, 1030), "INDEPENDENT VERIFICATION STATUS", font=font_tag, fill=ACCENT_CYAN)
    
    badges = [
        ("Lean 4 Kernel Check", "PASSED • 0 ERRORS", ACCENT_GREEN),
        ("Clay Math Institute Audit", "UNDER PEER REVIEW", ACCENT_AMBER),
        ("External Topology Review", "ACTIVE EVALUATION", ACCENT_CYAN)
    ]
    for i, (b_title, b_status, col) in enumerate(badges):
        by = 1080 + i * 90
        draw.rounded_rectangle([140, by, W - 140, by + 70], radius=10, fill=(14, 19, 29), outline=col, width=1)
        draw.text((160, by + 20), b_title, font=font_sub, fill=TEXT_WHITE)
        draw.text((W - 420, by + 22), b_status, font=font_tag, fill=col)

    draw_footer_card(draw, "Formal proof eliminates human algebraic oversight")
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
    draw.text((150, 1220), "• Peer-reviewed AI research", font=font_sub, fill=TEXT_WHITE)
    draw.text((150, 1270), "• Technical architecture diagrams", font=font_sub, fill=TEXT_WHITE)
    draw.text((150, 1320), "• Zero hype, strict provenance", font=font_sub, fill=ACCENT_GREEN)

    draw_footer_card(draw, "Follow @lidoailab for daily autonomous AI intelligence")
    img.save(ASSETS_DIR / "shot_05.png")
    print("Rendered shot_05.png")

def main():
    print("Rendering Navier-Stokes Visual Frames...")
    render_shot_01()
    render_shot_02()
    render_shot_03()
    render_shot_04()
    render_shot_05()
    print("All 5 Navier-Stokes visual frames rendered successfully!")

if __name__ == "__main__":
    main()
