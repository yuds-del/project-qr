# Import Flask untuk membuat API
from flask import Flask, request, jsonify, send_file

from flask_cors import CORS

# Library untuk membuat QR Code
import qrcode

# Library untuk menyimpan gambar di memori (tanpa simpan ke file)
import io

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# IZINKAN SEMUA ORIGIN (DEV MODE)
CORS(app, resources={r"/*": {"origins": "*"}})

# Endpoint API untuk generate QR Code
@app.route('/generate-qr', methods=['POST'])
def generate_qr():
    # Mengambil data JSON dari request
    data = request.json

    # Mengambil nilai 'text' dari JSON
    text = data.get('text')

    # Validasi jika text kosong
    if not text:
        return jsonify({"error": "text is required"}), 400

    # Membuat QR Code dari text
    qr = qrcode.make(text)

    # Membuat buffer memory untuk menyimpan gambar QR
    buffer = io.BytesIO()

    # Menyimpan QR Code ke buffer dalam format PNG
    qr.save(buffer, format='PNG')

    # Mengembalikan pointer buffer ke awal
    buffer.seek(0)

    # Mengirim file QR Code sebagai response API
    return send_file(
        buffer,
        mimetype='image/png'
    )

# Menjalankan server Flask
if __name__ == '__main__':
    app.run(debug=True)
