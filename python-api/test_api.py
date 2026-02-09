import requests

url = "http://localhost:5000/generate-qr"
data = {"text": "hello world"}

res = requests.post(url, json=data)

with open("hasil_qr.png", "wb") as f:
    f.write(res.content)

print("QR berhasil dibuat")
