"""
AOI System Customer Acceptance Presentation
iGuard AOI — Prepreg / CCL Inspection
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ExifTags
import io, os, copy

# ── Paths ──────────────────────────────────────────────────────────────────
UP = "/root/.claude/uploads/7995871e-2904-5c65-bebb-dd5f1424b688"
OUT = "/home/user/gpt-ai-assistant/iGuard_AOI_Acceptance.pptx"

# filename → (description, rotation_needed)
# All photos are sideways (landscape sensor, portrait orientation)
# We fix via EXIF transpose
IMGS = {
    "c134e148-5922.jpg": "engineer_inspect_frame",
    "36904af0-5920.jpg": "engineer_examine_machine",
    "f70770e5-5919.jpg": "team_assembly",
    "566f775c-5918.jpg": "team_assemble_machine",
    "30c03f19-5917.jpg": "machine_full_view",
    "d4329ee6-5916.jpg": "loading_roll_machine",
    "61bc114c-5915.jpg": "prepreg_roll_closeup",
    "db7d8cf6-5914.jpg": "engineer_roll_load",
    "0318905f-5913.jpg": "team_unpack_doosan",
    "45e19896-5912.jpg": "team_discuss_material",
    "6fcd566d-5911.jpg": "iguard_full_machine",
    "6dd1d6e3-5910.jpg": "monitor_results",
    "e6a2d99f-5909.jpg": "machine_running",
    "84500fd0-5908.jpg": "prepreg_surface",
    "9d6dd958-5907.jpg": "group_review_machine",
    "c8d31686-5904.jpg": "team_gather_machine",
    "46cdc9da-5905.jpg": "electrical_cabinet",
    "ee17691c-5906.jpg": "team_examine_machine",
    "6f430e2d-5901.jpg": "client_discuss",
    "8a891a71-5899.jpg": "engineer_check_sensor",
}

def load_img(fname, max_w=None, max_h=None):
    """Load image, apply EXIF rotation, return BytesIO at target size."""
    path = os.path.join(UP, fname)
    img = Image.open(path)
    # Apply EXIF rotation
    try:
        for k, v in ExifTags.TAGS.items():
            if v == "Orientation":
                orient_key = k
                break
        exif = img._getexif()
        if exif and orient_key in exif:
            o = exif[orient_key]
            if o == 3:   img = img.rotate(180, expand=True)
            elif o == 6: img = img.rotate(270, expand=True)
            elif o == 8: img = img.rotate(90,  expand=True)
    except Exception:
        pass
    # Resize
    if max_w and max_h:
        img.thumbnail((max_w, max_h), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    buf.seek(0)
    return buf

# ── Color Palette ──────────────────────────────────────────────────────────
NAVY   = RGBColor(0x0D, 0x2B, 0x55)
BLUE   = RGBColor(0x1A, 0x5F, 0xA8)
CYAN   = RGBColor(0x00, 0xA8, 0xD6)
LGRAY  = RGBColor(0xF4, 0xF6, 0xF9)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
DKGRAY = RGBColor(0x33, 0x3C, 0x4A)
ACCENT = RGBColor(0x00, 0xC2, 0x9A)   # teal green
ORANGE = RGBColor(0xFF, 0x6B, 0x35)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

# ── Helpers ────────────────────────────────────────────────────────────────
def rect(slide, l, t, w, h, fill=None, line=None, alpha=None):
    s = slide.shapes.add_shape(1,
        Inches(l), Inches(t), Inches(w), Inches(h))
    if fill:
        s.fill.solid(); s.fill.fore_color.rgb = fill
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = line
        s.line.width = Pt(1)
    else:
        s.line.fill.background()
    return s

def txt(slide, text, l, t, w, h,
        size=16, bold=False, color=DKGRAY,
        align=PP_ALIGN.LEFT, font="微軟正黑體", wrap=True, italic=False):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = wrap
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
    r.font.color.rgb = color; r.font.name = font
    return tb

def pic(slide, fname, l, t, w, h, max_px=2400):
    buf = load_img(fname, max_px, max_px)
    slide.shapes.add_picture(buf, Inches(l), Inches(t), Inches(w), Inches(h))

def header_band(slide, title, sub=None, bg=NAVY, h=1.5):
    rect(slide, 0, 0, 13.33, h, fill=bg)
    rect(slide, 0, h, 13.33, 0.06, fill=CYAN)
    txt(slide, title, 0.45, 0.1, 12.0, 0.85,
        size=34, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
    if sub:
        txt(slide, sub, 0.45, 0.95, 12.0, 0.5,
            size=17, color=RGBColor(0xAA, 0xCC, 0xFF))

def footer(slide, n, total=10):
    rect(slide, 0, 7.1, 13.33, 0.4, fill=NAVY)
    txt(slide, "iGuard AOI System  |  Prepreg & CCL Acceptance", 0.3, 7.12, 9, 0.35,
        size=12, color=RGBColor(0xAA, 0xBB, 0xCC))
    txt(slide, f"{n} / {total}", 12.0, 7.12, 1.2, 0.35,
        size=12, color=WHITE, align=PP_ALIGN.RIGHT)

def chip(slide, label, l, t, w=2.2, h=0.48, bg=BLUE):
    rect(slide, l, t, w, h, fill=bg)
    txt(slide, label, l+0.08, t+0.04, w-0.16, h-0.08,
        size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════════════
#  SLIDE 1  Cover
# ══════════════════════════════════════════════════════════════════════════
s1 = prs.slides.add_slide(BLANK)
rect(s1, 0, 0, 13.33, 7.5, fill=NAVY)

# Background photo (full-bleed, dimmed)
buf_bg = load_img("6fcd566d-5911.jpg", 1920, 1080)
ph = s1.shapes.add_picture(buf_bg, Inches(0), Inches(0),
                            Inches(13.33), Inches(7.5))
# Semi-transparent overlay (simulate via second rect with transparency workaround)
ov = rect(s1, 0, 0, 13.33, 7.5, fill=NAVY)
from pptx.oxml.ns import qn
from lxml import etree
solidFill = ov.fill._xPr.find(qn('a:solidFill'))
srgb = solidFill.find(qn('a:srgbClr'))
alpha_el = etree.SubElement(srgb, qn('a:alpha'))
alpha_el.set('val', '72000')   # 72% opacity

# Logo text
txt(s1, "iGuard", 0.55, 0.8, 4, 1.0,
    size=52, bold=True, color=CYAN, align=PP_ALIGN.LEFT)
txt(s1, "AOI Inspection System", 0.55, 1.75, 9, 0.7,
    size=26, color=WHITE, align=PP_ALIGN.LEFT)

rect(s1, 0.5, 2.55, 8.5, 0.07, fill=CYAN)

txt(s1, "Prepreg & CCL 材料瑕疵檢測", 0.55, 2.75, 10, 0.85,
    size=30, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
txt(s1, "客戶驗收報告  Customer Acceptance Review", 0.55, 3.6, 10, 0.6,
    size=22, color=RGBColor(0xCC, 0xEE, 0xFF), align=PP_ALIGN.LEFT)

rect(s1, 0.5, 4.4, 5.5, 0.75, fill=BLUE)
txt(s1, f"驗收日期  2026-06-07  ·  AOITEK", 0.65, 4.5, 5.2, 0.55,
    size=16, color=WHITE)

txt(s1, "1 / 10", 12.0, 7.12, 1.2, 0.35,
    size=12, color=WHITE, align=PP_ALIGN.RIGHT)

# ══════════════════════════════════════════════════════════════════════════
#  SLIDE 2  驗收議程
# ══════════════════════════════════════════════════════════════════════════
s2 = prs.slides.add_slide(BLANK)
rect(s2, 0, 0, 13.33, 7.5, fill=LGRAY)
header_band(s2, "驗收議程", "Acceptance Agenda")

agenda = [
    ("01", "系統介紹",      "iGuard AOI 系統架構與功能說明"),
    ("02", "機台安裝確認",  "設備到場後安裝調試過程記錄"),
    ("03", "待測材料說明",  "Prepreg / CCL 卷料樣品確認"),
    ("04", "上料與送料驗證","卷料上料、張力控制、走料順暢"),
    ("05", "系統運行測試",  "全速運行、AOI 掃描功能驗證"),
    ("06", "缺陷檢測展示",  "實際瑕疵影像與分類結果"),
    ("07", "軟體介面確認",  "HMI 操作介面、報表輸出確認"),
    ("08", "客戶審查討論",  "客戶意見紀錄與工程師說明"),
    ("09", "驗收結論",      "通過項目 / 待改善項目 / 後續行動"),
]

cols = 2
for i, (num, title, desc) in enumerate(agenda):
    col = i % cols
    row = i // cols
    x = 0.4 + col * 6.5
    y = 1.7 + row * 1.12
    rect(s2, x, y, 6.1, 0.98, fill=WHITE, line=BLUE)
    rect(s2, x, y, 0.72, 0.98, fill=BLUE)
    txt(s2, num, x+0.02, y+0.17, 0.68, 0.6,
        size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s2, title, x+0.82, y+0.06, 5.1, 0.45,
        size=17, bold=True, color=NAVY)
    txt(s2, desc,  x+0.82, y+0.52, 5.1, 0.42,
        size=13, color=DKGRAY, italic=True)

footer(s2, 2)

# ══════════════════════════════════════════════════════════════════════════
#  SLIDE 3  系統架構總覽
# ══════════════════════════════════════════════════════════════════════════
s3 = prs.slides.add_slide(BLANK)
rect(s3, 0, 0, 13.33, 7.5, fill=LGRAY)
header_band(s3, "iGuard AOI 系統架構總覽", "System Overview")

# Left — machine photo
pic(s3, "6fcd566d-5911.jpg", 0.35, 1.7, 5.4, 5.2)

# Right — spec cards
specs = [
    (BLUE,   "檢測對象",   "Prepreg 玻纖預浸布 / CCL 銅箔基板（卷料）"),
    (ACCENT, "缺陷種類",   "異物、刮傷、凹坑、缺料、折痕、氣泡、邊緣不良"),
    (NAVY,   "掃描方式",   "線掃相機全幅掃描，逐行即時比對分析"),
    (ORANGE, "輸出功能",   "即時標記、等級分類、報表匯出、AI 輔助判讀"),
    (BLUE,   "系統品牌",   "iGuard  ·  AOITEK Co., Ltd."),
]
for i, (c, label, val) in enumerate(specs):
    y = 1.75 + i * 1.08
    rect(s3, 6.1, y, 6.8, 0.95, fill=WHITE, line=c)
    rect(s3, 6.1, y, 1.8, 0.95, fill=c)
    txt(s3, label, 6.12, y+0.2, 1.76, 0.55,
        size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s3, val, 8.05, y+0.12, 4.75, 0.72,
        size=14, color=DKGRAY)

footer(s3, 3)

# ══════════════════════════════════════════════════════════════════════════
#  SLIDE 4  機台安裝確認
# ══════════════════════════════════════════════════════════════════════════
s4 = prs.slides.add_slide(BLANK)
rect(s4, 0, 0, 13.33, 7.5, fill=LGRAY)
header_band(s4, "機台安裝確認", "Equipment Installation & Setup")

photos4 = [
    ("c134e148-5922.jpg", "工程師確認機台結構"),
    ("36904af0-5920.jpg", "機台框架檢視"),
    ("f70770e5-5919.jpg", "團隊協同組裝調試"),
    ("566f775c-5918.jpg", "多人現場組裝確認"),
]
for i, (fn, cap) in enumerate(photos4):
    col = i % 2; row = i // 2
    x = 0.35 + col * 6.5; y = 1.65 + row * 2.75
    pic(s4, fn, x, y, 6.0, 2.45)
    rect(s4, x, y+2.45, 6.0, 0.28, fill=NAVY)
    txt(s4, cap, x+0.1, y+2.47, 5.8, 0.26,
        size=13, color=WHITE, align=PP_ALIGN.CENTER)

footer(s4, 4)

# ══════════════════════════════════════════════════════════════════════════
#  SLIDE 5  待測材料確認
# ══════════════════════════════════════════════════════════════════════════
s5 = prs.slides.add_slide(BLANK)
rect(s5, 0, 0, 13.33, 7.5, fill=LGRAY)
header_band(s5, "待測材料確認", "Test Material — Prepreg / CCL")

# Left col — 2 photos
pic(s5, "61bc114c-5915.jpg",  0.35, 1.65, 5.9, 2.7)
rect(s5, 0.35, 4.35, 5.9, 0.28, fill=NAVY)
txt(s5, "Prepreg 卷料（橄欖綠色，玻纖環氧預浸布）",
    0.45, 4.37, 5.7, 0.26, size=13, color=WHITE, align=PP_ALIGN.CENTER)

pic(s5, "84500fd0-5908.jpg", 0.35, 4.72, 5.9, 2.22)
rect(s5, 0.35, 6.94, 5.9, 0.28, fill=NAVY)
txt(s5, "Prepreg 表面細節（可見輕微折痕瑕疵）",
    0.45, 6.96, 5.7, 0.26, size=13, color=WHITE, align=PP_ALIGN.CENTER)

# Right col — material spec
rect(s5, 6.55, 1.65, 6.45, 5.55, fill=WHITE, line=BLUE)
txt(s5, "材料規格說明", 6.75, 1.75, 6.1, 0.55,
    size=20, bold=True, color=NAVY)
rect(s5, 6.55, 2.3, 6.45, 0.06, fill=CYAN)

mat_info = [
    ("材料類型",  "Prepreg（半固化玻纖預浸布）/ CCL（銅箔基板）"),
    ("供應廠商",  "DOOSAN（東山）"),
    ("外觀特徵",  "卷料形式，橄欖綠 / 棕色，寬幅約 600mm"),
    ("主要瑕疵",  "折痕、表面刮傷、異物、凹坑、氣泡"),
    ("卷料尺寸",  "依實際生產規格（含管芯重量）"),
    ("上機方式",  "退卷軸固定＋張力控制器自動調節"),
]
for i, (k, v) in enumerate(mat_info):
    y = 2.5 + i * 0.75
    rect(s5, 6.6, y, 1.75, 0.62, fill=BLUE)
    txt(s5, k, 6.65, y+0.1, 1.65, 0.45,
        size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s5, v, 8.45, y+0.1, 4.4, 0.55, size=14, color=DKGRAY)

footer(s5, 5)

# ══════════════════════════════════════════════════════════════════════════
#  SLIDE 6  上料與送料驗證
# ══════════════════════════════════════════════════════════════════════════
s6 = prs.slides.add_slide(BLANK)
rect(s6, 0, 0, 13.33, 7.5, fill=LGRAY)
header_band(s6, "上料與送料驗證", "Material Loading & Feed Verification")

# 3 photos with captions
photos6 = [
    ("db7d8cf6-5914.jpg",  "工程師人工上卷料"),
    ("d4329ee6-5916.jpg",  "穿料進入送料滾輪"),
    ("30c03f19-5917.jpg",  "整機送料路徑確認"),
]
for i, (fn, cap) in enumerate(photos6):
    x = 0.3 + i * 4.35
    pic(s6, fn, x, 1.65, 4.1, 4.9)
    rect(s6, x, 6.55, 4.1, 0.28, fill=NAVY)
    txt(s6, cap, x+0.1, 6.57, 3.9, 0.26,
        size=13, color=WHITE, align=PP_ALIGN.CENTER)

# Step flow
steps = ["① 卷料到場確認", "② 安裝退卷軸", "③ 穿帶引料", "④ 張力設定", "⑤ 試走確認"]
for i, s in enumerate(steps):
    c = [BLUE, CYAN, ACCENT, ORANGE, NAVY][i]
    x = 0.3 + i * 2.6
    rect(s6, x, 6.95, 2.45, 0.4, fill=c)
    txt(s6, s, x+0.05, 6.97, 2.35, 0.36,
        size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

footer(s6, 6)

# ══════════════════════════════════════════════════════════════════════════
#  SLIDE 7  系統運行與掃描驗證
# ══════════════════════════════════════════════════════════════════════════
s7 = prs.slides.add_slide(BLANK)
rect(s7, 0, 0, 13.33, 7.5, fill=LGRAY)
header_band(s7, "系統運行與掃描驗證", "System Operation & Scanning Test")

# Left — 2 photos stacked
pic(s7, "e6a2d99f-5909.jpg",  0.35, 1.65, 5.9, 2.55)
rect(s7, 0.35, 4.2,  5.9, 0.28, fill=NAVY)
txt(s7, "AOI 掃描主機運行中",
    0.45, 4.22, 5.7, 0.26, size=13, color=WHITE, align=PP_ALIGN.CENTER)

pic(s7, "ee17691c-5906.jpg", 0.35, 4.58, 5.9, 2.25)
rect(s7, 0.35, 6.83, 5.9, 0.28, fill=NAVY)
txt(s7, "工程師現場確認掃描狀態",
    0.45, 6.85, 5.7, 0.26, size=13, color=WHITE, align=PP_ALIGN.CENTER)

# Right — checklist
rect(s7, 6.55, 1.65, 6.45, 5.55, fill=WHITE, line=ACCENT)
txt(s7, "運行驗證項目", 6.75, 1.75, 6.1, 0.55,
    size=20, bold=True, color=NAVY)
rect(s7, 6.55, 2.3, 6.45, 0.05, fill=ACCENT)

checks = [
    ("✔", ACCENT, "機台啟動正常，無異常警報"),
    ("✔", ACCENT, "送料速度穩定，張力無抖動"),
    ("✔", ACCENT, "線掃相機正常取像，畫面清晰"),
    ("✔", ACCENT, "即時影像顯示流暢（≥30fps）"),
    ("✔", ACCENT, "AOI 演算法正常載入與執行"),
    ("✔", ACCENT, "緊急停機（E-Stop）功能驗證"),
    ("✔", ACCENT, "電控箱接線整齊，無鬆脫"),
]
for i, (icon, c, desc) in enumerate(checks):
    y = 2.45 + i * 0.72
    rect(s7, 6.6, y, 0.55, 0.58, fill=c)
    txt(s7, icon, 6.6, y+0.08, 0.55, 0.45,
        size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s7, desc, 7.25, y+0.1, 5.6, 0.48, size=14, color=DKGRAY)

footer(s7, 7)

# ══════════════════════════════════════════════════════════════════════════
#  SLIDE 8  缺陷檢測結果展示
# ══════════════════════════════════════════════════════════════════════════
s8 = prs.slides.add_slide(BLANK)
rect(s8, 0, 0, 13.33, 7.5, fill=LGRAY)
header_band(s8, "缺陷檢測結果展示", "Defect Detection Results")

# Left — monitor screenshot showing results
pic(s8, "6dd1d6e3-5910.jpg", 0.35, 1.65, 6.1, 5.55)
rect(s8, 0.35, 7.2, 6.1, 0.28, fill=NAVY)
txt(s8, "AOI 軟體即時顯示 CCL 掃描結果（瑕疵標記畫面）",
    0.45, 7.22, 5.9, 0.26, size=12, color=WHITE, align=PP_ALIGN.CENTER)

# Right — defect table
rect(s8, 6.75, 1.65, 6.25, 0.65, fill=BLUE)
txt(s8, "瑕疵分類結果  Defect Classification", 6.85, 1.73, 6.05, 0.52,
    size=17, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

defects = [
    ("折痕  Crease",      "Grade B", ORANGE, "已檢出"),
    ("表面刮傷 Scratch",  "Grade A", BLUE,   "已檢出"),
    ("凹坑   Dent",       "Grade B", ORANGE, "已檢出"),
    ("異物   Inclusion",  "Grade A", BLUE,   "已檢出"),
    ("邊緣不良 Edge",     "Grade C", ACCENT, "已檢出"),
    ("正常   Normal",     "PASS",    ACCENT, "正常通過"),
]
for i, (name, grade, c, status) in enumerate(defects):
    y = 2.38 + i * 0.78
    bg = LGRAY if i % 2 == 0 else WHITE
    rect(s8, 6.75, y, 6.25, 0.75, fill=bg)
    txt(s8, name,   6.85, y+0.12, 3.2, 0.52, size=14, color=DKGRAY)
    rect(s8, 10.15, y+0.1, 1.35, 0.52, fill=c)
    txt(s8, grade, 10.15, y+0.12, 1.35, 0.5,
        size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s8, status, 11.6, y+0.12, 1.3, 0.52,
        size=13, color=DKGRAY, align=PP_ALIGN.CENTER)

footer(s8, 8)

# ══════════════════════════════════════════════════════════════════════════
#  SLIDE 9  客戶審查與討論
# ══════════════════════════════════════════════════════════════════════════
s9 = prs.slides.add_slide(BLANK)
rect(s9, 0, 0, 13.33, 7.5, fill=LGRAY)
header_band(s9, "客戶審查與現場討論", "Customer Review & On-site Discussion")

photos9 = [
    ("9d6dd958-5907.jpg",  "客戶與工程師聯合審查機台"),
    ("c8d31686-5904.jpg",  "現場討論機台配置"),
    ("6f430e2d-5901.jpg",  "客戶代表確認細部機構"),
    ("8a891a71-5899.jpg",  "感測器與電控接線確認"),
]
for i, (fn, cap) in enumerate(photos9):
    col = i % 2; row = i // 2
    x = 0.35 + col * 6.5; y = 1.65 + row * 2.75
    pic(s9, fn, x, y, 6.0, 2.45)
    rect(s9, x, y+2.45, 6.0, 0.28, fill=NAVY)
    txt(s9, cap, x+0.1, y+2.47, 5.8, 0.26,
        size=13, color=WHITE, align=PP_ALIGN.CENTER)

footer(s9, 9)

# ══════════════════════════════════════════════════════════════════════════
#  SLIDE 10  驗收結論與後續行動
# ══════════════════════════════════════════════════════════════════════════
s10 = prs.slides.add_slide(BLANK)
rect(s10, 0, 0, 13.33, 7.5, fill=NAVY)
rect(s10, 0, 0, 13.33, 0.12, fill=CYAN)
rect(s10, 0, 7.38, 13.33, 0.12, fill=CYAN)

txt(s10, "驗收結論  Acceptance Conclusion", 0.5, 0.25, 12, 0.9,
    size=36, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s10, "iGuard AOI System  ·  Prepreg & CCL Inspection", 0.5, 1.1, 12, 0.55,
    size=18, color=CYAN, align=PP_ALIGN.CENTER)

# Pass / Pending columns
rect(s10, 0.4, 1.85, 5.9, 0.55, fill=ACCENT)
txt(s10, "✔  驗收通過項目", 0.55, 1.9, 5.6, 0.48,
    size=18, bold=True, color=WHITE)
pass_items = [
    "機台結構組裝完整，無鬆脫",
    "卷料上料、送料流程順暢",
    "AOI 線掃相機成像品質良好",
    "即時瑕疵檢測功能正常運作",
    "軟體 HMI 操作介面清楚易用",
    "緊急停機功能驗證通過",
]
for i, item in enumerate(pass_items):
    txt(s10, f"  ●  {item}", 0.5, 2.5 + i*0.68, 5.7, 0.6,
        size=15, color=RGBColor(0xCC, 0xFF, 0xEE))

rect(s10, 6.85, 1.85, 6.1, 0.55, fill=ORANGE)
txt(s10, "⚡  後續行動項目", 7.0, 1.9, 5.8, 0.48,
    size=18, bold=True, color=WHITE)
action_items = [
    "確認最終驗收報告簽署",
    "機台出廠前完整清潔包裝",
    "提供操作訓練與保養手冊",
    "安排安裝到廠時程確認",
    "售後保固條款書面確認",
]
for i, item in enumerate(action_items):
    txt(s10, f"  →  {item}", 6.95, 2.5 + i*0.68, 5.8, 0.6,
        size=15, color=RGBColor(0xFF, 0xE0, 0xCC))

rect(s10, 0.4, 7.0, 12.5, 0.04, fill=CYAN)
txt(s10, "Thank you  ·  感謝蒞臨驗收  ·  AOITEK Co., Ltd.  2026-06-07",
    0, 7.05, 13.33, 0.38,
    size=14, color=RGBColor(0xAA, 0xCC, 0xFF), align=PP_ALIGN.CENTER)

# save
prs.save(OUT)
print(f"Saved → {OUT}")
