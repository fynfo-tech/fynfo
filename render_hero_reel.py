import math
import random
import subprocess
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 720, 720
FPS = 30
DURATION_SEC = 8
TOTAL_FRAMES = FPS * DURATION_SEC  # 240 frames
OUTPUT_FILE = 'images/fynfo-reel.mp4'

font_dir = '/home/karthick/.gemini/antigravity-ide/brain/f1681838-950c-4e79-8c28-0b42c2a0d57a/scratch/fonts/'
font_welcome = ImageFont.truetype(font_dir + 'Outfit-700.ttf', 26)
font_brand = ImageFont.truetype(font_dir + 'Outfit-800.ttf', 40)

icon_raw = Image.open('images/fynfo-icon.png').convert('RGBA')

# Pre-generate smooth atmospheric obsidian background
def create_smooth_background():
    bg = Image.new('RGBA', (W, H), (6, 8, 14, 255))
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    cx, cy = W // 2, H // 2
    
    # Outer subtle dark amber aura
    glow_draw.ellipse([cx - 310, cy - 280, cx + 310, cy + 280], fill=(212, 160, 40, 42))
    # Medium warm golden halo
    glow_draw.ellipse([cx - 195, cy - 175, cx + 195, cy + 175], fill=(245, 195, 65, 68))
    # Core radiant bright bloom
    glow_draw.ellipse([cx - 110, cy - 100, cx + 110, cy + 100], fill=(255, 230, 120, 95))
    
    # Heavy Gaussian blur to make it completely smooth without banding
    blurred_glow = glow.filter(ImageFilter.GaussianBlur(radius=62))
    bg = Image.alpha_composite(bg, blurred_glow)
    return bg

BASE_BG = create_smooth_background()

# Pre-generate stable celestial particles around center
random.seed(4242)
particles = []
for _ in range(55):
    ang = random.uniform(0, 2 * math.pi)
    dist = random.uniform(60, 330)
    particles.append({
        'base_dist': dist,
        'base_angle': ang,
        'speed': random.uniform(0.12, 0.38) * (1 if random.random() > 0.5 else -1),
        'size': random.uniform(1.2, 2.6),
        'alpha': random.uniform(0.35, 0.90)
    })

def render_frame(f_idx):
    t = f_idx / TOTAL_FRAMES
    angle = t * 2 * math.pi

    frame = BASE_BG.copy()
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    cx = W // 2
    cy = H // 2 + 10  # Optical visual center

    # 1. Celestial Gold Stardust Particle Field
    for p in particles:
        p_ang = p['base_angle'] + p['speed'] * angle
        p_dist = p['base_dist'] + 8 * math.sin(p_ang * 2)
        px = cx + p_dist * math.cos(p_ang)
        py = cy + p_dist * 0.85 * math.sin(p_ang)
        if 15 <= px <= W - 15 and 15 <= py <= H - 15:
            p_size = p['size'] * (1.0 + 0.22 * math.sin(p_ang * 3))
            p_a = int(255 * p['alpha'] * (0.65 + 0.35 * math.sin(p_ang * 4)))
            draw_ov.ellipse(
                [px - p_size, py - p_size, px + p_size, py + p_size],
                fill=(245, 225, 140, p_a)
            )

    # 2. Luxury Holographic Orbital Rings (Centered on Logo)
    # Outer Orbit Ring (Radius 230)
    r_outer = 230
    draw_ov.ellipse(
        [cx - r_outer, cy - int(r_outer * 0.92), cx + r_outer, cy + int(r_outer * 0.92)],
        outline=(212, 175, 55, 42), width=1
    )
    # 8 Cardinal & Diagonal Micro-Nodes rotating smoothly
    for n_idx, n_ang in enumerate([0, math.pi/4, math.pi/2, 3*math.pi/4, math.pi, 5*math.pi/4, 3*math.pi/2, 7*math.pi/4]):
        cur_ang = n_ang + angle * 0.4
        nx = cx + r_outer * math.cos(cur_ang)
        ny = cy + int(r_outer * 0.92) * math.sin(cur_ang)
        n_rad = 2.2 if n_idx % 2 == 0 else 1.3
        draw_ov.ellipse([nx - n_rad, ny - n_rad, nx + n_rad, ny + n_rad], fill=(245, 220, 110, 140))

    # Middle Orbit with 2 Traveling Golden Photons (Radius 180)
    r_mid = 180
    draw_ov.ellipse(
        [cx - r_mid, cy - int(r_mid * 0.90), cx + r_mid, cy + int(r_mid * 0.90)],
        outline=(212, 175, 55, 70), width=1
    )
    # Photon 1
    p1_a = angle * 2
    p1_x = cx + r_mid * math.cos(p1_a)
    p1_y = cy + int(r_mid * 0.90) * math.sin(p1_a)
    draw_ov.ellipse([p1_x - 7, p1_y - 7, p1_x + 7, p1_y + 7], fill=(255, 225, 100, 65))
    draw_ov.ellipse([p1_x - 3.5, p1_y - 3.5, p1_x + 3.5, p1_y + 3.5], fill=(255, 255, 255, 255))

    # Photon 2 (Opposite Phase)
    p2_a = angle * 2 + math.pi
    p2_x = cx + r_mid * math.cos(p2_a)
    p2_y = cy + int(r_mid * 0.90) * math.sin(p2_a)
    draw_ov.ellipse([p2_x - 6, p2_y - 6, p2_x + 6, p2_y + 6], fill=(212, 175, 55, 55))
    draw_ov.ellipse([p2_x - 3, p2_y - 3, p2_x + 3, p2_y + 3], fill=(255, 240, 190, 240))

    # Inner Delicate Ring (Radius 132)
    r_inner = 132
    draw_ov.ellipse(
        [cx - r_inner, cy - int(r_inner * 0.88), cx + r_inner, cy + int(r_inner * 0.88)],
        outline=(212, 175, 55, 50), width=1
    )

    # 3. Floating 3D FYNFO Logo (Hero Size: ~205x193)
    float_dy = int(8 * math.sin(angle))
    scale_fac = 1.0 + 0.02 * math.cos(angle)
    icon_w = int(205 * scale_fac)
    icon_h = int(193 * scale_fac)
    scaled_icon = icon_raw.resize((icon_w, icon_h), Image.Resampling.LANCZOS)

    # Soft, Diffuse Ambient Drop Shadow below emblem
    shadow_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(shadow_layer)
    sh_w = int(icon_w * 0.88)
    sh_h = 24
    sh_y = cy + 108
    sh_draw.ellipse(
        [cx - sh_w // 2, sh_y - sh_h // 2, cx + sh_w // 2, sh_y + sh_h // 2],
        fill=(0, 0, 0, 160)
    )
    blurred_shadow = shadow_layer.filter(ImageFilter.GaussianBlur(radius=12))
    overlay = Image.alpha_composite(overlay, blurred_shadow)

    # Merge overlay with frame
    frame = Image.alpha_composite(frame, overlay)

    # Paste Emblem with levitation
    paste_x = cx - icon_w // 2
    paste_y = cy - icon_h // 2 + float_dy
    frame.paste(scaled_icon, (paste_x, paste_y), scaled_icon)

    # Specular Glint Light Beam sweeping across the golden emblem
    cycle_prog = (f_idx % 120) / 120.0
    if 0.10 <= cycle_prog <= 0.40:
        beam_prog = (cycle_prog - 0.10) / 0.30
        sweep_x = paste_x - 60 + int(beam_prog * (icon_w + 120))
        sheen_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        sheen_draw = ImageDraw.Draw(sheen_layer)
        alpha_sheen = int(120 * math.sin(beam_prog * math.pi))
        sheen_draw.polygon([
            (sweep_x - 20, paste_y - 35),
            (sweep_x + 20, paste_y - 35),
            (sweep_x + 65, paste_y + icon_h + 35),
            (sweep_x + 25, paste_y + icon_h + 35)
        ], fill=(255, 252, 230, alpha_sheen))
        
        mask_im = Image.new('L', (W, H), 0)
        mask_im.paste(scaled_icon.split()[3], (paste_x, paste_y))
        sheen_layer.putalpha(Image.composite(sheen_layer.split()[3], Image.new('L', (W, H), 0), mask_im))
        frame = Image.alpha_composite(frame, sheen_layer)

    # 4. Typography: WELCOME TO (Enlarged) above, FYNFO below
    draw_txt = ImageDraw.Draw(frame)

    # Top: "—  W E L C O M E   T O  —" (Enlarged size 26)
    top_text = "W E L C O M E   T O"
    bb_top = draw_txt.textbbox((0, 0), top_text, font=font_welcome)
    tw = bb_top[2] - bb_top[0]
    th = bb_top[3] - bb_top[1]
    top_y = paste_y - th - 24

    # Drop shadow for welcome text
    draw_txt.text((cx - tw // 2, top_y + 2), top_text, fill=(0, 0, 0, 200), font=font_welcome)
    # Bright Champagne Gold
    draw_txt.text((cx - tw // 2, top_y), top_text, fill=(235, 205, 95), font=font_welcome)

    # Hairline accents matching enlarged text height
    line_y = top_y + th // 2 + 2
    draw_txt.line([(cx - tw // 2 - 40, line_y), (cx - tw // 2 - 14, line_y)], fill=(212, 175, 55, 180), width=2)
    draw_txt.line([(cx + tw // 2 + 14, line_y), (cx + tw // 2 + 40, line_y)], fill=(212, 175, 55, 180), width=2)

    # Bottom: "F  Y  N  F  O" (Size 40 ExtraBold)
    brand_text = "F  Y  N  F  O"
    bb_b = draw_txt.textbbox((0, 0), brand_text, font=font_brand)
    bw = bb_b[2] - bb_b[0]
    brand_y = paste_y + icon_h + 24

    draw_txt.text((cx - bw // 2, brand_y + 3), brand_text, fill=(0, 0, 0, 220), font=font_brand)
    draw_txt.text((cx - bw // 2, brand_y), brand_text, fill=(255, 252, 245), font=font_brand)

    return frame.convert('RGB')

def render_full_video():
    poster = render_frame(30)
    poster.save('images/fynfo-reel-poster.png', 'PNG')
    print("Poster saved: images/fynfo-reel-poster.png")

    cmd = [
        'gst-launch-1.0', '-q',
        'fdsrc', 'fd=0',
        '!', f'rawvideoparse', f'width={W}', f'height={H}', 'format=rgb', f'framerate={FPS}/1',
        '!', 'videoconvert',
        '!', 'video/x-raw,format=I420',
        '!', 'x264enc', 'speed-preset=medium', 'bitrate=3000',
        '!', 'video/x-h264,profile=baseline',
        '!', 'mp4mux', 'faststart=true',
        '!', 'filesink', f'location={OUTPUT_FILE}'
    ]
    
    print(f"Starting video encode: {TOTAL_FRAMES} frames ({DURATION_SEC}s @ {FPS}fps) to {OUTPUT_FILE}...")
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    
    for f_idx in range(TOTAL_FRAMES):
        img = render_frame(f_idx)
        proc.stdin.write(img.tobytes())
        if (f_idx + 1) % 30 == 0:
            print(f"Rendered {f_idx + 1}/{TOTAL_FRAMES} frames ({(f_idx + 1)/TOTAL_FRAMES*100:.0f}%)...")
            
    proc.stdin.close()
    proc.wait()
    print("Video generation with enlarged WELCOME TO complete successfully!")

if __name__ == '__main__':
    render_full_video()
