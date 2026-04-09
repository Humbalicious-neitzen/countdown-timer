from flask import Flask, send_file
from PIL import Image, ImageDraw, ImageFont
import io, os, urllib.request
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

DEADLINE = datetime(2026, 4, 15, 21, 0, 0, tzinfo=timezone(timedelta(hours=5)))
BG_COLOR = (217, 217, 219)
NUMBER_COLOR = (255, 0, 21)
LABEL_COLOR = (0, 0, 0)
WIDTH, HEIGHT = 900, 140

FONT_BOLD_PATH = "/tmp/RobotoBold.ttf"
FONT_REG_PATH = "/tmp/RobotoReg.ttf"

def download_fonts():
    if not os.path.exists(FONT_BOLD_PATH):
        urllib.request.urlretrieve("https://fonts.gstatic.com/s/roboto/v30/KFOlCnqEu92Fr1MmWUlfBBc4.woff2", FONT_BOLD_PATH)
    if not os.path.exists(FONT_REG_PATH):
        urllib.request.urlretrieve("https://fonts.gstatic.com/s/roboto/v30/KFOmCnqEu92Fr1Mu4mxK.woff2", FONT_REG_PATH)

def generate_gif():
    now = datetime.now(tz=timezone(timedelta(hours=5)))
    diff = DEADLINE - now
    if diff.total_seconds() <= 0:
        days, hours, minutes, seconds = 0, 0, 0, 0
    else:
        total_seconds = int(diff.total_seconds())
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
    try:
        download_fonts()
        number_font = ImageFont.truetype(FONT_BOLD_PATH, 95)
        label_font = ImageFont.truetype(FONT_REG_PATH, 18)
    except:
        number_font = ImageFont.load_default(size=60)
        label_font = ImageFont.load_default(size=16)
    frames = []
    for s in range(seconds, seconds - 2, -1):
        sec = max(s, 0)
        img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
        draw = ImageDraw.Draw(img)
        sections = [(f"{days:02d}", "Days"), (f"{hours:02d}", "Hrs"), (f"{minutes:02d}", "Mins"), (f"{sec:02d}", "Secs")]
        x = 40
        for num, label in sections:
            num_bbox = draw.textbbox((0, 0), num, font=number_font)
            num_w = num_bbox[2] - num_bbox[0]
            num_h = num_bbox[3] - num_bbox[1]
            draw.text((x, 20), num, font=number_font, fill=NUMBER_COLOR)
            label_bbox = draw.textbbox((0, 0), label, font=label_font)
            label_h = label_bbox[3] - label_bbox[1]
            label_w = label_bbox[2] - label_bbox[0]
            label_y = 20 + num_h - label_h - 2
            draw.text((x + num_w + 8, label_y), label, font=label_font, fill=LABEL_COLOR)
            x += num_w + label_w + 55
        frames.append(img)
    buf = io.BytesIO()
    frames[0].save(buf, format="GIF", save_all=True, append_images=frames[1:], loop=0, duration=1000)
    buf.seek(0)
    return buf

@app.route("/timer")
def timer():
    gif = generate_gif()
    return send_file(gif, mimetype="image/gif")

@app.route("/")
def home():
    return "Timer is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
