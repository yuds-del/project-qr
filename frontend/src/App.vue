<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-xl w-full max-w-md p-6">
      <h1 class="text-2xl font-bold text-center text-gray-800 mb-4">
        QR Code Generator
      </h1>

      <input
        v-model="text"
        type="text"
        placeholder="Masukkan teks atau URL"
        class="w-full px-4 py-2 border rounded-lg mb-4"
      />

      <button
        @click="generateQR"
        class="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-2 rounded-lg"
      >
        Generate QR
      </button>

      <div v-if="qrImage" class="mt-6 text-center">
        <img :src="qrImage" class="mx-auto w-48 h-48" />
        <a
    :href="qrImage"
    download="qr-code.png"
    class="inline-block mt-4 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg"
  >
    Download QR
  </a>
</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const text = ref('')
const qrImage = ref(null)

const generateQR = async () => {
  if (!text.value) {
    alert('Text tidak boleh kosong')
    return
  }

  try {
    const response = await fetch('http://127.0.0.1:5000/generate-qr', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: text.value })
    })

    if (!response.ok) throw new Error('Gagal generate')

    const blob = await response.blob()
    qrImage.value = URL.createObjectURL(blob)
  } catch (err) {
    console.error(err)
    alert('QR gagal dibuat')
  }
}
</script>
