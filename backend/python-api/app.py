import io
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from PIL import Image

app = Flask(__name__)
CORS(app)

@app.route('/generate-qr', methods=['POST'])
def generate_qr():
    text = request.json.get('text')
    if not text:
        return jsonify({'error': 'text is required'}), 400

    
    #BUAT QR (SCAN-FRIENDLY)
    
    qr = qrcode.QRCode(
        version=None,  # auto
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=6  # lebih lega = scan lebih cepat
    )
    qr.add_data(text)
    qr.make(fit=True)

    qr_img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(
            radius_ratio=0.5  # JANGAN full bulat
        ),
        fill_color="black",
        back_color="white"
    ).convert("RGB")

    
    try:
        logo = Image.open("logo.png").convert("RGBA")
    except:
        return jsonify({'error': 'logo.png not found'}), 400

    qr_w, qr_h = qr_img.size

    # logo maksimal 20%
    logo_size = qr_w // 5
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    # background putih supaya nyatu & kebaca
    logo_bg = Image.new("RGBA", logo.size, "WHITE")
    logo_bg.paste(logo, mask=logo)

    pos = ((qr_w - logo_size) // 2, (qr_h - logo_size) // 2)
    qr_img.paste(logo_bg, pos)

 
    buffer = io.BytesIO()
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(buffer, mimetype="image/png")


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5000, use_reloader=False)
