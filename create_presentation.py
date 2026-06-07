from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# Colors matching the original slide
ORANGE = RGBColor(0xD4, 0x7E, 0x0A)      # Gold/Orange for 才幹
DARK_BLUE = RGBColor(0x2C, 0x3E, 0x7B)    # Dark blue for 恩賜
LIGHT_BG = RGBColor(0xF5, 0xF5, 0xF5)    # Light background
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TEXT_DARK = RGBColor(0x1A, 0x1A, 0x2E)
GOLD = RGBColor(0xE8, 0x9B, 0x0F)
ACCENT_BLUE = RGBColor(0x3A, 0x5A, 0xC4)

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

BLANK = prs.slide_layouts[6]  # blank layout


def add_rect(slide, left, top, width, height, fill_color=None, line_color=None):
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if line_color:
        shape.line.color.rgb = line_color
    else:
        shape.line.fill.background()
    return shape


def add_text_box(slide, text, left, top, width, height,
                 font_size=18, bold=False, color=TEXT_DARK,
                 align=PP_ALIGN.LEFT, font_name="微軟正黑體", wrap=True):
    txBox = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font_name
    return txBox


def add_slide_header(slide, title, subtitle=None, bg_color=DARK_BLUE):
    # Top color band
    hdr = add_rect(slide, 0, 0, 13.33, 1.6, fill_color=bg_color)
    add_text_box(slide, title, 0.5, 0.2, 12.0, 0.9,
                 font_size=36, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
    if subtitle:
        add_text_box(slide, subtitle, 0.5, 1.0, 12.0, 0.5,
                     font_size=20, bold=False, color=RGBColor(0xCC, 0xDD, 0xFF),
                     align=PP_ALIGN.LEFT)


def add_footer(slide, page_num, total=10):
    add_rect(slide, 0, 7.1, 13.33, 0.4, fill_color=DARK_BLUE)
    add_text_box(slide, f"{page_num} / {total}", 11.8, 7.1, 1.3, 0.4,
                 font_size=13, color=WHITE, align=PP_ALIGN.RIGHT)
    add_text_box(slide, "恩賜 VS. 才幹", 0.3, 7.1, 4, 0.4,
                 font_size=13, color=RGBColor(0xCC, 0xDD, 0xFF))


# ───────────────────────────────────────────
# Slide 1: Title
# ───────────────────────────────────────────
slide1 = prs.slides.add_slide(BLANK)
# Full background
bg = add_rect(slide1, 0, 0, 13.33, 7.5, fill_color=DARK_BLUE)

# Decorative gold bar
add_rect(slide1, 0, 3.3, 13.33, 0.08, fill_color=GOLD)

# Main title
add_text_box(slide1, "恩賜 VS. 才幹", 1, 1.5, 11, 1.6,
             font_size=64, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# Subtitle
add_text_box(slide1, "認識神的恩典與人的天賦", 1, 3.5, 11, 0.8,
             font_size=30, color=GOLD, align=PP_ALIGN.CENTER)

# Scripture reference
add_text_box(slide1, "彼前 4:10  ·  太 25:21", 1, 4.6, 11, 0.6,
             font_size=22, color=RGBColor(0xAA, 0xCC, 0xFF), align=PP_ALIGN.CENTER)

add_text_box(slide1, "1 / 10", 11.8, 7.0, 1.3, 0.4,
             font_size=13, color=RGBColor(0x99, 0xAA, 0xCC), align=PP_ALIGN.RIGHT)


# ───────────────────────────────────────────
# Slide 2: Overview — 恩賜 VS. 才幹
# ───────────────────────────────────────────
slide2 = prs.slides.add_slide(BLANK)
add_rect(slide2, 0, 0, 13.33, 7.5, fill_color=LIGHT_BG)
add_slide_header(slide2, "一、恩賜 VS. 才幹", "概覽：兩者的核心對比")

# Left card — 恩賜
add_rect(slide2, 0.4, 1.9, 5.6, 4.6, fill_color=DARK_BLUE)
add_text_box(slide2, "🎁  恩賜", 0.6, 2.1, 5.2, 0.7,
             font_size=26, bold=True, color=WHITE)
add_text_box(slide2, (
    "• 聖靈賜下的超自然能力\n"
    "• 為建立教會、榮耀神\n"
    "• 因信心與聖靈而運作\n"
    "• 彼前 4:10"
), 0.6, 2.9, 5.2, 3.0, font_size=18, color=WHITE)

# VS
add_text_box(slide2, "VS.", 5.9, 3.5, 1.5, 0.9,
             font_size=32, bold=True, color=DARK_BLUE, align=PP_ALIGN.CENTER)

# Right card — 才幹
add_rect(slide2, 7.3, 1.9, 5.6, 4.6, fill_color=ORANGE)
add_text_box(slide2, "🏅  才幹", 7.5, 2.1, 5.2, 0.7,
             font_size=26, bold=True, color=WHITE)
add_text_box(slide2, (
    "• 天生或後天培養的能力\n"
    "• 可在信徒與非信徒中見\n"
    "• 需要練習與努力\n"
    "• 太 25:21"
), 7.5, 2.9, 5.2, 3.0, font_size=18, color=WHITE)

add_footer(slide2, 2)


# ───────────────────────────────────────────
# Slide 3: 什麼是恩賜？
# ───────────────────────────────────────────
slide3 = prs.slides.add_slide(BLANK)
add_rect(slide3, 0, 0, 13.33, 7.5, fill_color=LIGHT_BG)
add_slide_header(slide3, "什麼是恩賜？", "Spiritual Gifts")

# Scripture box
add_rect(slide3, 0.5, 1.8, 12.3, 1.4, fill_color=DARK_BLUE)
add_text_box(slide3,
    "各人要照所得的恩賜彼此服事，作神百般恩賜的好管家。",
    0.7, 1.9, 12.0, 0.7, font_size=22, bold=True, color=WHITE)
add_text_box(slide3, "彼得前書 4:10", 10.0, 2.6, 2.8, 0.5,
             font_size=16, color=GOLD, align=PP_ALIGN.RIGHT)

# Body bullets
bullets = [
    ("定義", "聖靈賜給每位信徒特別的能力，用來服事神的家"),
    ("來源", "來自聖靈，非人力可取，是神主動賜下"),
    ("目的", "建立基督的身體（教會），使萬民認識神"),
    ("運作", "透過信心順服聖靈，超越自身能力的限制"),
]
for i, (label, content) in enumerate(bullets):
    y = 3.4 + i * 0.8
    add_rect(slide3, 0.5, y, 2.0, 0.6, fill_color=DARK_BLUE)
    add_text_box(slide3, label, 0.55, y + 0.05, 1.9, 0.55,
                 font_size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text_box(slide3, content, 2.7, y + 0.05, 10.1, 0.6,
                 font_size=18, color=TEXT_DARK)

add_footer(slide3, 3)


# ───────────────────────────────────────────
# Slide 4: 常見的屬靈恩賜
# ───────────────────────────────────────────
slide4 = prs.slides.add_slide(BLANK)
add_rect(slide4, 0, 0, 13.33, 7.5, fill_color=LIGHT_BG)
add_slide_header(slide4, "常見的屬靈恩賜", "林前 12  ·  羅 12  ·  弗 4")

gifts = [
    ("先知講道", "傳達神的信息，勸勉、安慰、造就"),
    ("服事幫助", "實際行動服事他人需要"),
    ("教導",     "清晰解釋並傳授聖經真理"),
    ("勸慰",     "鼓勵他人靈命成長"),
    ("施捨",     "慷慨奉獻，供應他人所需"),
    ("治理領導", "帶領、組織、管理事工"),
    ("憐憫",     "以同理心關懷受苦的人"),
    ("信心",     "對神有超越常人的信靠與委身"),
]

cols = 2
for i, (name, desc) in enumerate(gifts):
    col = i % cols
    row = i // cols
    x = 0.4 + col * 6.5
    y = 1.85 + row * 1.3
    add_rect(slide4, x, y, 6.0, 1.1, fill_color=DARK_BLUE)
    add_text_box(slide4, name, x + 0.15, y + 0.05, 5.7, 0.45,
                 font_size=20, bold=True, color=GOLD)
    add_text_box(slide4, desc, x + 0.15, y + 0.5, 5.7, 0.55,
                 font_size=16, color=WHITE)

add_footer(slide4, 4)


# ───────────────────────────────────────────
# Slide 5: 什麼是才幹？
# ───────────────────────────────────────────
slide5 = prs.slides.add_slide(BLANK)
add_rect(slide5, 0, 0, 13.33, 7.5, fill_color=LIGHT_BG)
add_slide_header(slide5, "什麼是才幹？", "Talents & Natural Abilities", bg_color=ORANGE)

# Scripture box
add_rect(slide5, 0.5, 1.8, 12.3, 2.0, fill_color=ORANGE)
add_text_box(slide5, (
    "主人說：好，你這又良善又忠心的僕人，\n"
    "你在不多的事上有忠心，我要把許多事派你管理；\n"
    "可以進來享受你主人的快樂。"
), 0.7, 1.85, 12.0, 1.7, font_size=20, bold=True, color=WHITE)
add_text_box(slide5, "馬太福音 25:21", 9.8, 3.7, 3.0, 0.5,
             font_size=16, color=ORANGE, align=PP_ALIGN.RIGHT)

# Body bullets
bullets5 = [
    ("定義", "神創造時賦予每人天生的能力，或後天習得的技能"),
    ("來源", "來自神的創造，信徒與非信徒皆可擁有"),
    ("目的", "在世上盡本分，忠心管理神所給的一切"),
    ("特點", "需要培育、練習，在努力中逐漸成熟"),
]
for i, (label, content) in enumerate(bullets5):
    y = 4.35 + i * 0.65
    add_rect(slide5, 0.5, y, 2.0, 0.55, fill_color=ORANGE)
    add_text_box(slide5, label, 0.55, y + 0.05, 1.9, 0.5,
                 font_size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text_box(slide5, content, 2.7, y + 0.05, 10.1, 0.55,
                 font_size=17, color=TEXT_DARK)

add_footer(slide5, 5)


# ───────────────────────────────────────────
# Slide 6: 才幹的種類
# ───────────────────────────────────────────
slide6 = prs.slides.add_slide(BLANK)
add_rect(slide6, 0, 0, 13.33, 7.5, fill_color=LIGHT_BG)
add_slide_header(slide6, "才幹的種類", "各人都有不同的天賦", bg_color=ORANGE)

talents = [
    ("🎨  藝術創作", "音樂、繪畫、設計、寫作"),
    ("📊  分析思考", "數學、邏輯、研究、策略"),
    ("🗣️  溝通表達", "演講、談判、教學、語言"),
    ("🤝  人際關係", "同理心、領導、輔導、調解"),
    ("🔧  技術操作", "工程、建造、編程、手藝"),
    ("🌱  組織管理", "計劃、行政、協調、時間管理"),
]

for i, (name, desc) in enumerate(talents):
    col = i % 3
    row = i // 3
    x = 0.4 + col * 4.3
    y = 1.85 + row * 2.5
    add_rect(slide6, x, y, 3.9, 2.1, fill_color=ORANGE)
    add_text_box(slide6, name, x + 0.1, y + 0.15, 3.7, 0.7,
                 font_size=20, bold=True, color=WHITE)
    add_text_box(slide6, desc, x + 0.1, y + 0.85, 3.7, 0.9,
                 font_size=16, color=WHITE)

add_footer(slide6, 6)


# ───────────────────────────────────────────
# Slide 7: 比較表
# ───────────────────────────────────────────
slide7 = prs.slides.add_slide(BLANK)
add_rect(slide7, 0, 0, 13.33, 7.5, fill_color=LIGHT_BG)
add_slide_header(slide7, "恩賜 vs. 才幹 — 比較表")

headers = ["面向", "恩賜", "才幹"]
col_w = [3.0, 4.7, 4.7]
col_x = [0.3, 3.4, 8.2]

# Header row
for j, h in enumerate(headers):
    color = DARK_BLUE if j != 2 else ORANGE
    add_rect(slide7, col_x[j], 1.75, col_w[j], 0.65, fill_color=color)
    add_text_box(slide7, h, col_x[j] + 0.05, 1.78, col_w[j] - 0.1, 0.6,
                 font_size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

rows = [
    ("來源",     "聖靈直接賜下",           "神創造 / 後天培養"),
    ("對象",     "只有信徒",               "信徒與非信徒皆有"),
    ("目的",     "建立教會、榮耀神",        "在世盡職、忠心管理"),
    ("運作",     "藉信心與聖靈能力",        "藉努力與練習"),
    ("聖經根據", "彼前 4:10  林前 12",     "太 25:14-30"),
]

for i, (aspect, gift, talent) in enumerate(rows):
    y = 2.5 + i * 0.85
    bg = LIGHT_BG if i % 2 == 0 else RGBColor(0xE2, 0xE8, 0xF5)
    add_rect(slide7, col_x[0], y, col_w[0], 0.8, fill_color=RGBColor(0xDD, 0xE8, 0xFF))
    add_text_box(slide7, aspect, col_x[0] + 0.1, y + 0.1, col_w[0] - 0.2, 0.6,
                 font_size=17, bold=True, color=DARK_BLUE, align=PP_ALIGN.CENTER)
    add_rect(slide7, col_x[1], y, col_w[1], 0.8, fill_color=bg)
    add_text_box(slide7, gift, col_x[1] + 0.1, y + 0.1, col_w[1] - 0.2, 0.6,
                 font_size=16, color=DARK_BLUE)
    add_rect(slide7, col_x[2], y, col_w[2], 0.8, fill_color=bg)
    add_text_box(slide7, talent, col_x[2] + 0.1, y + 0.1, col_w[2] - 0.2, 0.6,
                 font_size=16, color=RGBColor(0x8B, 0x50, 0x00))

add_footer(slide7, 7)


# ───────────────────────────────────────────
# Slide 8: 如何發現您的恩賜？
# ───────────────────────────────────────────
slide8 = prs.slides.add_slide(BLANK)
add_rect(slide8, 0, 0, 13.33, 7.5, fill_color=LIGHT_BG)
add_slide_header(slide8, "如何發現您的恩賜？", "四個實踐步驟")

steps = [
    ("1", "禱告求問", "誠心向神禱告，求聖靈啟示你的恩賜"),
    ("2", "嘗試事奉", "積極參與教會各項事工，親身體驗"),
    ("3", "尋求確認", "從他人的回饋與肯定中辨別恩賜"),
    ("4", "結果驗證", "觀察事奉是否有果效，並感到喜悅"),
]

for i, (num, title, desc) in enumerate(steps):
    y = 1.85 + i * 1.3
    # Number circle
    add_rect(slide8, 0.4, y, 0.9, 0.9, fill_color=DARK_BLUE)
    add_text_box(slide8, num, 0.4, y + 0.05, 0.9, 0.8,
                 font_size=30, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    # Step bar
    add_rect(slide8, 1.4, y, 11.5, 0.9, fill_color=RGBColor(0xE0, 0xE8, 0xFF))
    add_text_box(slide8, title, 1.55, y + 0.05, 3.0, 0.5,
                 font_size=20, bold=True, color=DARK_BLUE)
    add_text_box(slide8, desc, 4.6, y + 0.1, 8.2, 0.7,
                 font_size=17, color=TEXT_DARK)

# Bottom scripture
add_rect(slide8, 0.4, 7.0, 12.5, 0.02, fill_color=DARK_BLUE)
add_footer(slide8, 8)


# ───────────────────────────────────────────
# Slide 9: 如何使用恩賜事奉？
# ───────────────────────────────────────────
slide9 = prs.slides.add_slide(BLANK)
add_rect(slide9, 0, 0, 13.33, 7.5, fill_color=LIGHT_BG)
add_slide_header(slide9, "如何使用恩賜與才幹事奉？", "忠心管理神所賜的一切")

principles = [
    ("謙遜使用",
     "恩賜是神所賜，非個人榮耀。以謙卑服事，一切榮耀歸主。"),
    ("彼此配搭",
     "每人的恩賜各有不同，互補不足，如身體的各個肢體。"),
    ("持續操練",
     "才幹需要鍛鍊，恩賜需要使用，才能在神國度發揮最大影響。"),
    ("愛為根基",
     "林前 13：即使有各樣恩賜，若沒有愛，也是徒然。"),
]

for i, (title, desc) in enumerate(principles):
    col = i % 2
    row = i // 2
    x = 0.4 + col * 6.5
    y = 1.85 + row * 2.55
    color = DARK_BLUE if col == 0 else ORANGE
    add_rect(slide9, x, y, 6.1, 2.3, fill_color=color)
    add_text_box(slide9, title, x + 0.15, y + 0.1, 5.8, 0.65,
                 font_size=22, bold=True, color=WHITE)
    add_text_box(slide9, desc, x + 0.15, y + 0.75, 5.8, 1.4,
                 font_size=17, color=WHITE)

add_footer(slide9, 9)


# ───────────────────────────────────────────
# Slide 10: 結語
# ───────────────────────────────────────────
slide10 = prs.slides.add_slide(BLANK)
add_rect(slide10, 0, 0, 13.33, 7.5, fill_color=DARK_BLUE)

# Gold bar top
add_rect(slide10, 0, 0, 13.33, 0.15, fill_color=GOLD)

add_text_box(slide10, "結語", 0.5, 0.4, 12.3, 0.9,
             font_size=40, bold=True, color=GOLD, align=PP_ALIGN.CENTER)

# Summary box
add_rect(slide10, 0.8, 1.5, 11.7, 3.2, fill_color=RGBColor(0x1A, 0x2A, 0x55))
summary = (
    "恩賜是聖靈主動賜給信徒，為建立教會而用；\n"
    "才幹是神創造時賦予每人，需要培育與忠心使用。\n\n"
    "兩者都是神的禮物，都當為神的榮耀而使用，\n"
    "在愛中彼此服事，作神百般恩賜的好管家。"
)
add_text_box(slide10, summary, 1.0, 1.65, 11.3, 2.8,
             font_size=22, color=WHITE, align=PP_ALIGN.CENTER)

# Two scriptures
add_rect(slide10, 0.8, 4.9, 5.6, 1.2, fill_color=ACCENT_BLUE)
add_text_box(slide10, "「各人要照所得的恩賜\n彼此服事。」\n彼前 4:10",
             0.9, 4.95, 5.4, 1.1, font_size=16, color=WHITE, align=PP_ALIGN.CENTER)

add_rect(slide10, 6.9, 4.9, 5.6, 1.2, fill_color=ORANGE)
add_text_box(slide10, "「你這又良善又忠心的\n僕人……」\n太 25:21",
             7.0, 4.95, 5.4, 1.1, font_size=16, color=WHITE, align=PP_ALIGN.CENTER)

add_text_box(slide10, "10 / 10", 11.5, 7.1, 1.6, 0.4,
             font_size=13, color=RGBColor(0x88, 0xAA, 0xCC), align=PP_ALIGN.RIGHT)

# Save
output_path = "/home/user/gpt-ai-assistant/恩賜VS才幹_簡報.pptx"
prs.save(output_path)
print(f"Saved: {output_path}")
