import io
import json
import os
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from pyzbar.pyzbar import decode
from PIL import Image

app = Flask(__name__)
CORS(app)

# Path absolut agar logo pasti ditemukan oleh sistem
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "logo.png")

def generate_qr(data: str):
    # Error Correction H wajib agar QR tetap bisa di-scan meski ditutup logo
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,  # Resolusi tinggi agar detail logo terjaga
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Buat dasar QR
    qr_img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(radius_ratio=0.1),
        fill_color="black",
        back_color="white"
    ).convert("RGB")

    try:
        # Load Logo
        if not os.path.exists(LOGO_PATH):
            print(f"File {LOGO_PATH} tidak ditemukan!")
            return qr_img

        logo = Image.open(LOGO_PATH).convert("RGBA")
        qr_w, qr_h = qr_img.size

        # Ukuran logo: 22% dari ukuran QR (Ideal)
        logo_size = qr_w // 4.5
        logo = logo.resize((int(logo_size), int(logo_size)), Image.LANCZOS)

        #AREA PUTIH (DIPERTEBAL): Kunci agar logo terlihat di JSON padat
        padding = 35 
        clear_bg = Image.new("RGB", (int(logo_size + padding), int(logo_size + padding)), "white")
        
        # Tempel kotak putih di tengah
        bg_pos = ((qr_w - clear_bg.size[0]) // 2, (qr_h - clear_bg.size[1]) // 2)
        qr_img.paste(clear_bg, bg_pos)

        # Tempel logo di tengah kotak putih
        logo_pos = ((qr_w - logo.size[0]) // 2, (qr_h - logo.size[1]) // 2)
        qr_img.paste(logo, logo_pos, logo)
        
        print("Berhasil generate QR dengan logo")
    except Exception as e:
        print(f"Gagal menempel logo: {e}")

    return qr_img

@app.route('/generate-qr', methods=['POST'])
def generate_text_qr():
    text = request.json.get('text')
    if not text: return jsonify({'error': 'text required'}), 400
    img = generate_qr(text)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return send_file(buffer, mimetype="image/png")

@app.route('/generate-qr-from-json', methods=['POST'])
def generate_json_qr():
    data = request.json
    if not data: return jsonify({'error': 'JSON required'}), 400
    # Kompres JSON agar tidak terlalu padat
    json_text = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    img = generate_qr(json_text)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return send_file(buffer, mimetype="image/png")

@app.route('/decode-qr', methods=['POST'])
def decode_qr():
    if 'file' not in request.files: return jsonify({'error': 'no file'}), 400
    try:
        img = Image.open(request.files['file'].stream).convert("RGB")
        decoded = decode(img)
        return jsonify({'text': decoded[0].data.decode('utf-8')}) if decoded else ({'error': 'not found'}, 400)
    except: return jsonify({'error': 'invalid'}), 400

if __name__ == '__main__':
<<<<<<< HEAD
    app.run(host='0.0.0.0',debug=True, port=5000, use_reloader=False)
=======
    app.run(debug=True, port=5000)
>>>>>>> ec3ad21 (update qr to text (done), json to qr (done))
