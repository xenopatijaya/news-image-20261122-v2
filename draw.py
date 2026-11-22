"""Draw the news-image-20261122 v2 entry: one 1024x1024 front page that
sums up world news on Sunday 22 November 2026.

v2 discipline, learned from v1's 10W-1D-1L dev grade: every story on the
page was first reported on Sunday 22 November 2026 itself. Stories from
19-21 November that v1 carried (the Rikers plan, the Nitish Setu opening,
the ANC election aftermath, the airline warning, the Melania interview)
are gone. Forty dated stories, seven regions, all pictures drawn with
Pillow primitives - no photos, no downloaded images."""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 241, 227)
PAPER = (252, 248, 238)
INK = (26, 26, 26)
RED = (176, 30, 36)
NAVY = (31, 58, 95)
TEAL = (15, 118, 110)
GOLD = (184, 134, 11)
SKY = (168, 205, 225)
SKY_D = (120, 170, 205)
GREY = (90, 88, 82)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Greedy word wrap: the lines of text that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, lines, font, leading=None, fill=INK):
    if leading is None:
        leading = int(font.size * 1.18)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def fit_font(d, text, path, size, max_w, floor=8):
    """Largest size <= size at which text fits max_w (never below floor)."""
    while size > floor and d.textlength(text, font=F(path, size)) > max_w:
        size -= 1
    return F(path, size)


def chip(d, x, y, text, fill, size=10):
    f = F(SANS_B, size)
    w = d.textlength(text, font=f) + 14
    d.rounded_rectangle([x, y, x + w, y + size + 9], radius=4, fill=fill)
    d.text((x + 7, y + 4), text, font=f, fill=(255, 255, 255))
    return w


def banner(d, x, y, w, text, fill=RED, size=11):
    """Centred white caption strip along the bottom of a scene."""
    f = fit_font(d, text, SANS_B, size, w - 8)
    d.rectangle([x, y, x + w, y + size + 9], fill=fill)
    tw = d.textlength(text, font=f)
    d.text((x + (w - tw) / 2, y + 4), text, font=f, fill=(255, 255, 255))


def sun(d, cx, cy, r, fill=(240, 180, 60)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    for a in range(0, 360, 30):
        x1 = cx + (r + 2) * math.cos(math.radians(a))
        y1 = cy + (r + 2) * math.sin(math.radians(a))
        x2 = cx + (r + 8) * math.cos(math.radians(a))
        y2 = cy + (r + 8) * math.sin(math.radians(a))
        d.line([x1, y1, x2, y2], fill=fill, width=3)


def flag_us(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    for i in range(0, 13, 2):
        d.rectangle([x, y + i * h / 13, x + w, y + (i + 1) * h / 13],
                    fill=(178, 34, 52))
    d.rectangle([x, y, x + w * 0.4, y + h * 7 / 13], fill=NAVY)
    for r in range(3):
        for c in range(4):
            d.ellipse([x + 3 + c * w * 0.09, y + 2 + r * h * 0.18,
                       x + 6 + c * w * 0.09, y + 5 + r * h * 0.18],
                      fill=(255, 255, 255))


# ---------------------------------------------------------------- data
LEADS = [
    dict(num=1, chip="CLIMATE  •  ANTALYA", scene="cop",
         head="COP31 runs into Sunday with no deal",
         deck="Second day of overtime: the draft drops every mention of "
              "fossil fuels; the adaptation target is cut.",
         src="REUTERS / AP — SUN 22 NOV"),
    dict(num=2, chip="ASIA  •  HONG KONG", scene="hk",
         head="Hong Kong votes to fill its Election Committee",
         deck="Polling day: 5,700 voters choose 723 of the 1,500 seats on "
              "the body that picks the city's leader.",
         src="SCMP / HK GOV — SUN 22 NOV"),
    dict(num=3, chip="OCEANIA  •  AUKUS", scene="aukus",
         head="Marles: U.S. report on AUKUS subs is 'wrong'",
         deck="Canberra's defence chief rejects the warning that selling "
              "Virginia-class boats would thin the U.S. fleet for years.",
         src="ABC NEWS — SUN 22 NOV"),
]

CARDS = [
    dict(num=4, scene="barrage", src="KYIV IND. / REUTERS",
         head="Russia fires 186 drones in one night barrage",
         sub="Kryvyi Rih missile kills two; Ukraine hits a Russian ship."),
    dict(num=5, scene="bahrain", src="BAHRAIN MIN. / IRGC",
         head="Bahrain says Iranian strike hit an industrial site",
         sub="Tehran's Guards claim two U.S. Patriot systems disabled."),
    dict(num=6, scene="gaza", src="WAFA / MEDICS",
         head="Israeli strikes kill at least four in Gaza City",
         sub="Bombardment amid the truce; an aid vehicle is hit."),
    dict(num=7, scene="taxi", src="REPORTS — JAPAN",
         head="Passenger air taxi flies itself over Japan",
         sub="No pilot aboard for the demonstration flight."),
    dict(num=8, scene="fire", src="SAR / REPORTS",
         head="Fire tears through a Banten candy factory",
         sub="Three dead, 36 missing at Cikande; rescuers search on."),
    dict(num=9, scene="trump", src="CNBC — SUN 22 NOV",
         head="Trump sees a possible upside in the FBI breach",
         sub="'Not good,' he says of the crime-database hack, 'but it "
             "might provide benefits.'"),
    dict(num=10, scene="f1", src="REUTERS — LAS VEGAS",
         head="Verstappen wins a Las Vegas thriller",
         sub="35 lead changes in 50 laps; Norris 2nd, Piastri 3rd."),
    dict(num=11, scene="denmark", src="REPORTS — COPENHAGEN",
         head="Denmark expels a Russian attaché",
         sub="Alleged plot cited as hybrid pressure on NATO grows."),
    dict(num=12, scene="lebanon", src="REPORTS — BEIRUT",
         head="Aoun: Israel and Iran threaten our sovereignty",
         sub="Lebanon's president names two hurdles to state control."),
    dict(num=13, scene="poland", src="REPORTS — WARSAW",
         head="Rocket and drone stray into Poland",
         sub="Warsaw reports the incursion on NATO's eastern flank."),
    dict(num=14, scene="thailand", src="REUTERS — BANGKOK",
         head="Thailand to bar chemical exports to Myanmar mines",
         sub="Bangkok moves on rare-earth mining pollution."),
]

BRIEFS = [
    (15, "COP31:", " closing session set for 0600 GMT Sunday. — REUTERS"),
    (16, "COP31 draft:", " 144 paragraphs cut to 80. — AP"),
    (17, "COP31:", " $120bn adaptation target cut from the text. — REUTERS"),
    (18, "EU at COP31:", " 'a good deal or no deal.' — REUTERS"),
    (19, "Activists:", " draft's fossil-fuel silence denounced. — REPORTS"),
    (20, "Next COP:", " Addis Ababa, November 2027. — AP"),
    (21, "Hong Kong:", " 856 candidates chase the 723 seats. — SCMP"),
    (22, "Hong Kong:", " polls run 9am–6pm for 5,700 voters. — SCMP"),
    (23, "AUKUS:", " sales of 3–5 Virginia-class from 2032. — U.S. REPORT"),
    (24, "UN chief race:", " U.S. open to a Latin American, says Waltz."),
    (25, "Istanbul:", " Turkish intel chief meets a Hamas delegation."),
    (26, "Spain:", " bank tax to expand to fund housing, says PM."),
    (27, "Paris:", " police officers convicted of a racial assault."),
    (28, "Finland:", " flight curbs return over the Gulf of Finland."),
    (29, "Yemen:", " Houthis strike after the Hodeida operation."),
    (30, "Pakistan:", " 15 militants killed in Mastung operations."),
    (31, "Seoul:", " education minister's resignation accepted."),
    (32, "Chicago:", " Blackhawks star Bedard faces shoulder surgery."),
    (33, "Haiti:", " El Salvador deal to build detention centres."),
    (34, "Guatemala:", " wanted Mexican fugitive arrested."),
    (35, "Washington:", " contractors told to report Congress's requests."),
    (36, "London:", " UK–EU deals struck; Burnham eyes rejoining."),
    (37, "Italy:", " jeweller Paolo Bulgari dies. — REPORTS"),
    (38, "Nigeria:", " boat capsize toll rises to 24. — CITIZEN DIGITAL"),
    (39, "Kenya:", " floods kill six and displace hundreds."),
    (40, "Mogadishu:", " Somalia orders the UAE envoy out in 72 hours."),
]

REGIONS = ("SEVEN REGIONS — MIDDLE EAST 10 • EUROPE 9 • ASIA 8 • "
           "NORTH AMERICA 5 • AFRICA 4 • LATIN AMERICA 2 • OCEANIA 2")


# ---------------------------------------------------------------- scenes
def scene_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    sun(d, x + w - 36, y + 20, 12)
    d.rectangle([x, y + h - 30, x + w, y + h - 24], fill=(64, 120, 160))
    # summit hall with a row of national flags
    d.rectangle([x + 12, y + 40, x + w - 12, y + h - 30], fill=(240, 234, 218))
    d.rectangle([x + 12, y + 40, x + w - 12, y + 48], fill=TEAL)
    d.polygon([(x + 12, y + 40), (x + w // 2, y + 14), (x + w - 12, y + 40)],
              fill=(200, 60, 50))
    flag_cols = [RED, (240, 200, 40), (30, 130, 76), NAVY, (240, 120, 30),
                 (120, 60, 160)]
    for i, col in enumerate(flag_cols):
        fx = x + 26 + i * 44
        d.line([fx + 12, y + 60, fx + 12, y + 52], fill=INK, width=2)
        d.polygon([(fx + 12, y + 52), (fx + 24, y + 56), (fx + 12, y + 60)],
                  fill=col)
        d.rectangle([fx, y + 60, fx + 25, y + h - 32], fill=(150, 190, 215))
    banner(d, x, y + h - 24, w, "NO DEAL YET — TALKS INTO SUNDAY", size=12)


def scene_hk(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    sun(d, x + w - 28, y + 20, 11)
    base = y + h - 40
    towers = [(6, 25), (30, 36), (52, 22), (72, 49), (100, 30), (122, 40),
              (146, 24), (166, 44), (192, 29), (214, 37), (240, 23), (262, 34),
              (286, 26)]
    for tx, th in towers:
        d.rectangle([x + tx, base - th, x + tx + 18, base], fill=(52, 68, 92))
    d.rectangle([x + 70, base - 56, x + 92, base], fill=(38, 52, 74))
    d.line([x + 81, base - 56, x + 81, base - 64], fill=(38, 52, 74), width=3)
    d.rectangle([x, base, x + w, y + h - 24], fill=(64, 120, 160))
    for i in range(4):
        d.arc([x + 16 + i * 76, base + 3, x + 56 + i * 76, base + 12],
              180, 360, fill=(255, 255, 255), width=2)
    # ballot box on the quay with a paper going in
    bx, by = x + 120, y + h - 68
    d.polygon([(bx + 22, by - 14), (bx + 40, by - 10), (bx + 34, by + 4),
               (bx + 16, by)], fill=(255, 255, 255), outline=INK)
    d.rectangle([bx, by, bx + 58, by + 42], fill=(250, 248, 240),
                outline=INK, width=2)
    d.rectangle([bx + 10, by + 6, bx + 48, by + 11], fill=INK)
    d.text((bx + 9, by + 19), "VOTE", font=F(SANS_B, 13), fill=RED)
    banner(d, x, y + h - 24, w, "POLLING DAY — 723 SEATS AT STAKE",
           fill=NAVY, size=12)


def scene_aukus(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 52, 84))
    for rx in (30, 110, 200):
        d.polygon([(x + rx, y), (x + rx + 26, y), (x + rx + 58, y + h - 24),
                   (x + rx + 44, y + h - 24)], fill=(36, 70, 108))
    sy = y + 60
    d.ellipse([x + 34, sy - 16, x + w - 34, sy + 16], fill=(16, 20, 28))
    d.rectangle([x + 60, sy - 16, x + w - 60, sy + 16], fill=(16, 20, 28))
    d.rectangle([x + w // 2 - 16, sy - 34, x + w // 2 + 18, sy - 12],
                fill=(16, 20, 28))
    d.rectangle([x + w // 2 + 2, sy - 46, x + w // 2 + 6, sy - 34],
                fill=(16, 20, 28))
    d.polygon([(x + w - 44, sy - 4), (x + w - 22, sy - 22), (x + w - 22, sy + 2)],
              fill=(16, 20, 28))
    d.polygon([(x + w - 44, sy + 4), (x + w - 22, sy + 22), (x + w - 22, sy - 2)],
              fill=(16, 20, 28))
    for i in range(5):
        d.ellipse([x + 84 + i * 26, sy - 4, x + 90 + i * 26, sy + 2],
                  fill=(240, 200, 90))
    for bx, by, r in [(x + 52, sy - 30, 4), (x + 66, sy - 44, 3),
                      (x + 44, sy - 52, 2), (x + w - 70, sy - 28, 3)]:
        d.ellipse([bx - r, by - r, bx + r, by + r],
                  outline=(180, 210, 235), width=1)
    banner(d, x, y + h - 24, w, "AUKUS — 'THEY ARE WRONG'", size=12)


def scene_barrage(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 28, 48))
    # rooftops of Kryvyi Rih
    for bx, bh in [(2, 18), (20, 26), (40, 15), (56, 24), (74, 17)]:
        d.rectangle([x + bx, y + h - bh, x + bx + 16, y + h], fill=(10, 12, 22))
        d.rectangle([x + bx + 3, y + h - bh + 4, x + bx + 6, y + h - bh + 7],
                    fill=(240, 200, 90))
    # drone swarm with dotted trails
    for dx, dy in [(8, 8), (26, 14), (44, 6), (62, 16), (78, 9), (52, 22)]:
        d.line([x + dx - 6, y + dy - 5, x + dx, y + dy], fill=(150, 160, 190),
               width=1)
        d.ellipse([x + dx - 2, y + dy - 2, x + dx + 3, y + dy + 3],
                  fill=(230, 230, 240))
    # one burst over the city
    cx, cy = x + w - 16, y + 16
    for a in range(0, 360, 45):
        d.line([cx, cy, cx + 7 * math.cos(math.radians(a)),
                cy + 7 * math.sin(math.radians(a))], fill=(255, 170, 60),
               width=2)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 220, 130))


def scene_bahrain(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 205, 165))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(190, 165, 120))
    # industrial plant: tanks, flare stack, chimney smoke
    d.rectangle([x + 8, y + h - 26, x + 30, y + h - 12], fill=(150, 150, 145))
    d.ellipse([x + 8, y + h - 30, x + 30, y + h - 22], fill=(170, 170, 165))
    d.rectangle([x + 38, y + h - 24, x + 58, y + h - 12], fill=(130, 130, 125))
    d.rectangle([x + 70, y + 10, x + 74, y + h - 12], fill=(90, 90, 90))
    d.polygon([(x + 68, y + 4), (x + 72, y + 12), (x + 76, y + 4)],
              fill=(255, 140, 40))
    for sx, sy, r in [(x + 46, y + 12, 5), (x + 54, y + 7, 4)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(200, 195, 185))
    # incoming missile trail
    d.arc([x - 30, y - 26, x + 62, y + 34], 20, 95, fill=RED, width=2)
    d.polygon([(x + 52, y + 24), (x + 60, y + 28), (x + 53, y + 31)],
              fill=RED)


def scene_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 196, 168))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(150, 130, 105))
    blocks = [(4, 26), (18, 36), (34, 22), (48, 32), (64, 24), (78, 30)]
    for bx, bh in blocks:
        d.rectangle([x + bx, y + h - 10 - bh, x + bx + 12, y + h - 10],
                    fill=(120, 112, 100))
        d.rectangle([x + bx + 3, y + h - 16 - bh, x + bx + 6, y + h - 13 - bh],
                    fill=(240, 220, 150))
    # smoke plumes
    for sx, sy, r in [(x + 30, y + 12, 7), (x + 40, y + 7, 5), (x + 66, y + 14, 6)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(105, 100, 95))
    # strike flash
    cx, cy = x + 24, y + h - 34
    for a in range(0, 360, 60):
        d.line([cx, cy, cx + 6 * math.cos(math.radians(a)),
                cy + 6 * math.sin(math.radians(a))], fill=(255, 160, 50),
               width=2)


def scene_taxi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.ellipse([x + 6, y + h - 14, x + 30, y + h - 8], fill=(255, 255, 255))
    d.ellipse([x + w - 34, y + 8, x + w - 8, y + 15], fill=(255, 255, 255))
    # quadcopter cabin with two passengers, no pilot seat filled up front
    cx, cy = x + w // 2, y + h // 2 + 2
    d.ellipse([cx - 20, cy - 10, cx + 20, cy + 10], fill=(245, 245, 245),
              outline=INK, width=1)
    d.ellipse([cx - 11, cy - 7, cx - 3, cy + 1], fill=(90, 140, 190))
    d.ellipse([cx + 3, cy - 7, cx + 11, cy + 1], fill=(90, 140, 190))
    d.ellipse([cx - 9, cy - 5, cx - 5, cy - 1], fill=(215, 175, 135))
    d.ellipse([cx + 5, cy - 5, cx + 9, cy - 1], fill=(180, 140, 105))
    for ax, ay in [(cx - 26, cy - 14), (cx + 26, cy - 14), (cx - 26, cy + 12),
                   (cx + 26, cy + 12)]:
        d.line([cx, cy, ax, ay], fill=INK, width=1)
        d.ellipse([ax - 5, ay - 2, ax + 5, ay + 2], outline=INK, width=1)
    d.line([cx - 12, cy + 10, cx - 16, cy + 16], fill=INK, width=2)
    d.line([cx + 12, cy + 10, cx + 16, cy + 16], fill=INK, width=2)


def scene_fire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(70, 62, 58))
    # factory block with windows
    d.rectangle([x + 8, y + 22, x + w - 8, y + h - 6], fill=(150, 140, 128))
    for r in range(2):
        for c in range(5):
            d.rectangle([x + 13 + c * 15, y + 27 + r * 12,
                         x + 21 + c * 15, y + 34 + r * 12],
                        fill=(60, 55, 50))
    # flames along the roofline
    for fx in range(x + 10, x + w - 10, 9):
        d.polygon([(fx, y + 24), (fx + 4, y + 10 + (fx % 3) * 3),
                    (fx + 8, y + 24)], fill=(240, 120, 30))
        d.polygon([(fx + 2, y + 24), (fx + 4, y + 16 + (fx % 3) * 2),
                    (fx + 6, y + 24)], fill=(250, 200, 70))
    for sx, sy, r in [(x + 24, y + 8, 6), (x + 48, y + 5, 8), (x + 70, y + 9, 5)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(95, 90, 88))


def scene_trump(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(110, 140, 90))
    # White House facade
    d.rectangle([x + 14, y + 22, x + w - 14, y + h - 10], fill=(250, 248, 240))
    d.polygon([(x + 10, y + 22), (x + w // 2, y + 10), (x + w - 10, y + 22)],
              fill=(205, 205, 195))
    for i in range(5):
        cx = x + 20 + i * 14
        d.rectangle([cx, y + 28, cx + 5, y + h - 14], fill=(185, 185, 175))
    d.rectangle([x + w // 2 - 5, y + h - 24, x + w // 2 + 5, y + h - 10],
                fill=(60, 60, 60))
    flag_us(d, x + w // 2 - 11, y + 2, 22, 13)
    # speech bubble
    d.rounded_rectangle([x + w - 40, y + 16, x + w - 4, y + 30], radius=4,
                        fill=(255, 255, 255), outline=INK, width=1)
    d.polygon([(x + w - 34, y + 30), (x + w - 28, y + 30), (x + w - 33, y + 35)],
              fill=(255, 255, 255), outline=INK)
    d.text((x + w - 36, y + 19), "?!", font=F(SANS_B, 10), fill=RED)


def scene_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 20, 34))
    # strip lights and speed streaks
    for sx in (6, 30, 54, 78):
        d.ellipse([x + sx, y + 4, x + sx + 5, y + 9], fill=(255, 240, 190))
    for sy, ln in [(16, 30), (24, 44), (44, 26), (52, 40)]:
        d.line([x + 2, y + sy, x + 2 + ln, y + sy], fill=(120, 140, 190),
               width=1)
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(40, 40, 48))
    # open-wheel car silhouette
    cy = y + h - 22
    d.rectangle([x + 16, cy + 4, x + 62, cy + 8], fill=(200, 40, 40))
    d.rectangle([x + 30, cy - 3, x + 48, cy + 4], fill=(200, 40, 40))
    d.ellipse([x + 36, cy - 7, x + 44, cy + 1], fill=(240, 200, 90))
    d.rectangle([x + 8, cy - 2, x + 14, cy + 8], fill=(160, 30, 30))
    d.rectangle([x + 64, cy - 4, x + 70, cy + 8], fill=(160, 30, 30))
    for wx in (x + 18, x + 56):
        d.ellipse([wx, cy + 6, wx + 11, cy + 15], fill=(8, 8, 10))
    d.line([x + 70, cy + 2, x + w - 2, cy + 2], fill=(255, 220, 120), width=1)


def scene_denmark(d, x, y, w, h):
    # Danish flag field
    d.rectangle([x, y, x + w, y + h], fill=(198, 40, 48))
    d.rectangle([x + 24, y, x + 32, y + h], fill=(255, 255, 255))
    d.rectangle([x, y + h // 2 - 4, x + w, y + h // 2 + 4],
                fill=(255, 255, 255))
    # door ajar with an arrow pointing out
    d.rectangle([x + w - 34, y + 12, x + w - 8, y + h - 8],
                fill=(250, 246, 238), outline=INK, width=1)
    d.polygon([(x + w - 30, y + 16), (x + w - 12, y + 16), (x + w - 16, y + h - 12),
               (x + w - 30, y + h - 12)], fill=(210, 200, 180))
    d.line([x + w - 44, y + h // 2, x + w - 36, y + h // 2], fill=INK, width=2)
    d.polygon([(x + w - 36, y + h // 2 - 4), (x + w - 30, y + h // 2),
               (x + w - 36, y + h // 2 + 4)], fill=INK)


def scene_lebanon(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.rectangle([x, y, x + w, y + 12], fill=(237, 28, 36))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(237, 28, 36))
    # cedar of Lebanon
    cx = x + w // 2
    for wd, yy in [(10, 20), (18, 27), (26, 34), (32, 41)]:
        d.polygon([(cx, y + yy - 6), (cx - wd, y + yy + 4),
                   (cx + wd, y + yy + 4)], fill=(0, 122, 61))
    d.rectangle([cx - 2, y + 42, cx + 2, y + h - 14], fill=(110, 75, 40))


def scene_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 214, 190))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(140, 165, 120))
    # border post in white and red
    d.rectangle([x + 8, y + 16, x + 16, y + h - 8], fill=(255, 255, 255),
                outline=INK, width=1)
    d.rectangle([x + 8, y + 16, x + 16, y + 28], fill=(220, 20, 60))
    d.text((x + 9, y + 30), "PL", font=F(SANS_B, 7), fill=INK)
    # drone crossing overhead
    dx, dy = x + w - 26, y + 12
    d.line([dx - 12, dy + 8, dx, dy], fill=(90, 90, 90), width=1)
    d.ellipse([dx - 4, dy - 3, dx + 6, dy + 3], fill=(50, 50, 55))
    d.polygon([(dx + 6, dy - 1), (dx + 12, dy - 5), (dx + 12, dy + 2)],
              fill=(50, 50, 55))
    # rocket trail arcing in
    d.arc([x + 20, y - 18, x + w + 10, y + 30], 30, 100, fill=RED, width=2)


def scene_thailand(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 228, 205))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(90, 130, 160))
    # export crates, one stopped at a barrier
    for bx, by, col in [(8, 34, (178, 140, 90)), (26, 34, (160, 125, 80)),
                        (8, 20, (190, 150, 100))]:
        d.rectangle([x + bx, y + by, x + bx + 16, y + by + 13], fill=col,
                    outline=(110, 85, 50), width=1)
        d.line([x + bx, y + by, x + bx + 16, y + by + 13],
               fill=(110, 85, 50), width=1)
    # barrier arm down across the dock
    d.rectangle([x + w - 14, y + 16, x + w - 9, y + h - 10], fill=(70, 70, 70))
    for i in range(4):
        d.rectangle([x + 40 + i * 11, y + 18 + i * 2, x + 49 + i * 11,
                     y + 22 + i * 2], fill=(220, 40, 40) if i % 2 else (255, 255, 255))
    d.text((x + 46, y + 34), "STOP", font=F(SANS_B, 8), fill=RED)


SCENES = {"cop": scene_cop, "hk": scene_hk, "aukus": scene_aukus,
          "barrage": scene_barrage, "bahrain": scene_bahrain,
          "gaza": scene_gaza, "taxi": scene_taxi, "fire": scene_fire,
          "trump": scene_trump, "f1": scene_f1, "denmark": scene_denmark,
          "lebanon": scene_lebanon, "poland": scene_poland,
          "thailand": scene_thailand}


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 28
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=3)
    d.rectangle([12, 12, W - 13, H - 13], outline=RED, width=1)

    def centered(text, y, font, fill):
        d.text((W // 2 - d.textlength(text, font=font) / 2, y), text,
               font=font, fill=fill)

    centered("THE SUNDAY EDITION  •  ONE PAGE  •  EVERY STORY REPORTED "
             "ON THE DAY ITSELF", 20, F(SANS_B, 12), GREY)
    centered("THE WORLD IN ONE DAY", 34, F(SERIF, 54), INK)
    centered("SUNDAY 22 NOVEMBER 2026", 94, F(SERIF, 46), RED)
    d.line([M, 150, W - M, 150], fill=INK, width=2)
    centered("40 DATED STORIES  •  7 REGIONS  •  3 LEADS  •  11 CARDS  •  "
             "26 BRIEFS", 157, F(SANS_B, 14), NAVY)
    d.line([M, 180, W - M, 180], fill=INK, width=2)

    col_w = (W - 2 * M - 2 * 12) // 3

    # ---- leads
    ly, lead_h = 188, 232
    for i, lead in enumerate(LEADS):
        x = M + i * (col_w + 12)
        d.rectangle([x, ly, x + col_w, ly + lead_h], outline=INK, width=1,
                    fill=PAPER)
        d.text((x + 8, ly + 4), str(lead["num"]), font=F(SERIF, 24), fill=RED)
        chip(d, x + 36, ly + 7, lead["chip"], NAVY, size=10)
        SCENES[lead["scene"]](d, x + 1, ly + 30, col_w - 2, 106)
        hy = block(d, x + 8, ly + 142,
                   wrap(d, lead["head"], F(SERIF, 19), col_w - 16)[:2],
                   F(SERIF, 19), leading=21)
        block(d, x + 8, hy + 2,
              wrap(d, lead["deck"], F(SANS, 10), col_w - 16)[:3],
              F(SANS, 10), leading=12, fill=(60, 60, 60))
        d.text((x + 8, ly + lead_h - 13), lead["src"], font=F(SANS_B, 9),
               fill=GREY)

    # ---- cards, 3 cols x 4 rows; last slot is the regions panel
    cy = ly + lead_h + 8
    card_h = 70
    for slot in range(12):
        r, c = divmod(slot, 3)
        x = M + c * (col_w + 12)
        y = cy + r * (card_h + 8)
        if slot == 11:
            d.rectangle([x, y, x + col_w, y + card_h], fill=NAVY)
            d.text((x + 10, y + 6), "SEVEN REGIONS", font=F(SERIF, 15),
                   fill=(255, 255, 255))
            block(d, x + 10, y + 28,
                  wrap(d, REGIONS.split("— ", 1)[1], F(SANS_B, 9),
                       col_w - 20)[:2], F(SANS_B, 9), leading=11,
                  fill=(210, 222, 238))
            d.text((x + 10, y + card_h - 13),
                   "No story older than the day itself.",
                   font=F(SERIF_R, 9), fill=(180, 195, 215))
            continue
        card = CARDS[slot]
        d.rectangle([x, y, x + col_w, y + card_h], outline=INK, width=1,
                    fill=PAPER)
        SCENES[card["scene"]](d, x + 1, y + 1, 92, card_h - 2)
        d.text((x + 99, y + 3), str(card["num"]), font=F(SERIF, 16), fill=RED)
        block(d, x + 120, y + 4,
              wrap(d, card["head"], F(SERIF, 13), col_w - 128)[:2],
              F(SERIF, 13), leading=15)
        block(d, x + 99, y + 37,
              wrap(d, card["sub"], F(SANS, 8), col_w - 107)[:2],
              F(SANS, 8), leading=10, fill=(70, 70, 70))
        d.text((x + 99, y + card_h - 11), card["src"], font=F(SANS_B, 7),
               fill=GREY)

    # ---- briefs
    by = cy + 4 * (card_h + 8) + 6
    d.line([M, by - 4, W - M, by - 4], fill=INK, width=1)
    d.text((M, by + 2), "THE REST OF THE DAY — BRIEFS 15–40",
           font=F(SANS_B, 12), fill=NAVY)
    note = "each one reported Sunday 22 November 2026"
    d.text((W - M - d.textlength(note, font=F(SANS, 10)), by + 3), note,
           font=F(SANS, 10), fill=GREY)
    col2_x = M + (W - 2 * M) // 2 + 6
    col_w_b = (W - 2 * M) // 2 - 12
    for idx, (num, lead, rest) in enumerate(BRIEFS):
        r, c = idx % 13, idx // 13
        x = M if c == 0 else col2_x
        y = by + 20 + r * 15
        size = 10
        while size > 8:
            f_b, f_r = F(SANS_B, size), F(SANS, size)
            total = (d.textlength(str(num) + ". ", font=f_b)
                     + d.textlength(lead, font=f_b)
                     + d.textlength(rest, font=f_r))
            if total <= col_w_b:
                break
            size -= 1
        f_b, f_r = F(SANS_B, size), F(SANS, size)
        d.text((x, y), str(num) + ". ", font=f_b, fill=RED)
        off = d.textlength(str(num) + ". ", font=f_b)
        d.text((x + off, y), lead, font=f_b, fill=INK)
        off += d.textlength(lead, font=f_b)
        d.text((x + off, y), rest, font=f_r, fill=(50, 50, 50))

    # ---- footer
    fy = by + 20 + 13 * 15 + 8
    d.line([M, fy - 4, W - M, fy - 4], fill=INK, width=1)
    d.text((M, fy + 2),
           "Method: wire and broadsheet reports published on Sunday 22 "
           "November 2026 (Reuters, AP, BBC, SCMP, ABC News, Citizen "
           "Digital and others). Claims are attributed to their reporters; "
           "figures as reported on the day.",
           font=F(SANS, 9), fill=GREY)
    d.text((M, fy + 15),
           "Every picture on this page is drawn in code with Pillow — no "
           "photographs, no downloaded images.",
           font=F(SANS, 9), fill=GREY)
    return img


if __name__ == "__main__":
    build().save("entry.png", optimize=True)
    print("saved entry.png")
