from flask import Flask, send_file
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

DEADLINE = datetime(2026, 4, 15, 21, 0, 0, tzinfo=timezone(timedelta(hours=5)))

BG_COLOR = (217, 217, 219)
NUMBER_COLOR = (255, 0, 21)
LABEL_COLOR = (0, 0, 0)
WIDTH, HEIGHT = 700, 160

def generate_gif():
    frames = []
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

    for s in range(seconds, seconds - 2, -1):
        sec = max(s, 0)
        img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
        draw = ImageDraw.Draw(img)

        try:
            number_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 85)
            label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        except:
            number_font = ImageFont.load_default()
            label_font = ImageFont.load_default()

        sections = [
            (f"{days:02d}", "Days"),
            (f"{hours:02d}", "Hrs"),
            (f"{minutes:02d}", "Mins"),
            (f"{sec:02d}", "Secs"),
        ]

        col_width = WIDTH // 4
        for i, (num, label) in enumerate(sections):
            x_center = col_width * i + col_width // 2

            num_bbox = draw.textbbox((0, 0), num, font=number_font)
            num_w = num_bbox[2] - num_bbox[0]
            num_h = num_bbox[3] - num_bbox[1]
            draw.text((x_center - num_w // 2, 15), num, font=number_font, fill=NUMBER_COLOR)

            label_bbox = draw.textbbox((0, 0), label, font=label_font)
            label_w = label_bbox[2] - label_bbox[0]
            draw.text((x_center - label_w // 2, 15 + num_h + 8), label, font=label_font, fill=LABEL_COLOR)

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
