# Project QR
Sistem QR Code Generator berbasis microservice menggunakan Python (Flask) untuk generate QR dan Golang sebagai backend utama, dengan dukungan Frontend (Tailwind CSS) dan Telegram Bot.

## Fitur
- Generate QR Code dari teks / URL
- API berbasis REST (POST)
- Output berupa gambar PNG
- Backend utama menggunakan Golang
- Python khusus sebagai service QR Code
- Bisa diakses via Website & Telegram Bot

Mudah dikembangkan (microservice)
## Struktur Project
```text
project-qr/
├── backend/
│   ├── go-api/                 # Backend utama (Golang)
│   │   
│   │   
│   │   
│   │   
│   │   
│   │       
│   │
│   └── python-api/             # Service QR Code (Flask)
│       ├── app.py
│       ├── requirements.txt
│       └── test_api.py
│          
│
├── frontend/                   # Website (Tailwind CSS)
│   
│   
│   
│   
│
│
│   
│  
│
│
│   
│
├── README.md

```

## Instalasi (Python API)

Pastikan Python sudah terinstall.

```bash
cd backend/python-api
pip install -r requirements.txt
```
## Menjalankan Server API
```bash
python app.py
```
Server akan berjalan di:
```bash
http://127.0.0.1:5000
```

## REndpoint API (Python)
POST /generate-qr
Request (JSON)
```bash
{
  "text": "https://example.com"
}
```
## Response
- Status: 200 OK
- Tipe: image/png
- Isi: Gambar QR Code

## Menggunakan Python
File test_api.py:
```bash
python test_api.py
```
