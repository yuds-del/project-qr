# Project QR


## Fitur
- Generate QR Code dari teks / URL
- API berbasis REST (POST)
- Output berupa gambar PNG
- Mudah diintegrasikan dengan frontend atau aplikasi lain

## Struktur Project
```text
project-qr/
├── app.py
├── requirements.txt
├── test_api.py
├── README.md
```

## Instalasi

Pastikan Python sudah terinstall.

```bash
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

## Response

- Status: 200 OK
- Tipe: image/png
- Isi: Gambar QR Code

## Menggunakan Python
File test_api.py:
```bash
python test_api.py
```
