<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-500 to-purple-600 flex flex-col items-center p-6">

    <!-- MENU -->
    <div class="flex gap-3 mb-6">
      <button
        v-for="menu in menus"
        :key="menu.key"
        @click="switchMenu(menu.key)"
        :class="[
          'px-4 py-2 rounded-full text-sm font-semibold transition-all',
          activeMenu === menu.key
            ? 'bg-white text-indigo-600 shadow-md'
            : 'border border-white/40 text-white hover:bg-white/20'
        ]"
      >
        {{ menu.label }}
      </button>
    </div>

    <!-- CARD -->
    <div class="w-full max-w-md rounded-2xl bg-white/10 backdrop-blur-xl shadow-2xl p-6 text-white">
      <h1 class="text-2xl font-bold text-center mb-3">
        Code Converter
      </h1>

      <!-- ALERT ESTETIK -->
      <div
        v-if="alertMessage"
        :class="[
          'mb-4 px-4 py-3 rounded-lg text-sm font-medium text-center transition-all',
          alertType === 'error'
            ? 'bg-red-500/20 text-red-200 border border-red-400/30'
            : 'bg-green-500/20 text-green-200 border border-green-400/30'
        ]"
      >
        {{ alertMessage }}
      </div>

      <!-- TEXT → QR -->
      <div v-if="activeMenu === 'text'">
        <input
          v-model="text"
          type="text"
          placeholder="Masukkan teks atau URL"
          class="w-full px-4 py-2 rounded-lg bg-white/20 placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-white mb-4"
        />

        <button
          @click="generateTextQR"
          class="w-full bg-indigo-600 hover:bg-indigo-700 py-2 rounded-lg font-semibold"
        >
          Generate QR
        </button>
      </div>

      <!-- JSON → QR -->
      <div v-if="activeMenu === 'json'">
        <textarea
          v-model="jsonText"
          rows="5"
          placeholder='{"name":"Yuds"}'
          class="w-full px-4 py-2 rounded-lg bg-white/20 placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-white mb-4"
        />

        <button
          @click="generateJsonQR"
          class="w-full bg-indigo-600 hover:bg-indigo-700 py-2 rounded-lg font-semibold"
        >
          Generate QR
        </button>
      </div>

      <!-- QR → TEXT -->
      <div v-if="activeMenu === 'decode'" class="space-y-4">
        <input
          type="file"
          accept="image/*"
          @change="onFileChange"
          class="w-full text-sm text-white file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-indigo-600 file:text-white hover:file:bg-indigo-700"
        />

        <button
          @click="decodeQR"
          class="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-2 rounded-lg"
        >
          Decode QR
        </button>

        <div v-if="decodedText" class="mt-4 p-3 rounded-lg bg-white/10">
          {{ decodedText }}
        </div>
      </div>

      <!-- HASIL QR -->
      <div v-if="qrImage" class="mt-6 text-center">
        <img
          :src="qrImage"
          class="mx-auto max-w-[280px] rounded-lg bg-white p-2 shadow-lg"
        />
        <a
          :href="qrImage"
          download="qr-code.png"
          class="inline-block mt-4 bg-white text-indigo-600 px-6 py-2 rounded-lg font-bold shadow hover:bg-gray-100 transition"
        >
          Download QR
        </a>
      </div>
    </div>

    <!-- FOOTER -->
    <footer class="mt-10 px-5 py-2 rounded-full bg-white/10 backdrop-blur-md text-white/70 text-xs shadow">
      © 2026 Code Converter · Team Yuds & Firlan
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeMenu = ref('text')

const menus = [
  { key: 'text', label: 'Text → QR' },
  { key: 'json', label: 'JSON → QR' },
  { key: 'decode', label: 'QR → Text' }
]

const text = ref('')
const jsonText = ref('')
const qrImage = ref(null)
const decodedText = ref('')
const selectedFile = ref(null)

/* ALERT */
const alertMessage = ref('')
const alertType = ref('error')

const showAlert = (msg, type = 'error') => {
  alertMessage.value = msg
  alertType.value = type
  setTimeout(() => (alertMessage.value = ''), 3000)
}

/* SWITCH MENU */
const switchMenu = (key) => {
  activeMenu.value = key
  qrImage.value = null
  decodedText.value = ''
  alertMessage.value = ''
}

/* TEXT → QR */
const generateTextQR = async () => {
  if (!text.value) {
    showAlert('Teks tidak boleh kosong')
    return
  }

  const res = await fetch('http://127.0.0.1:5000/generate-qr', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: text.value })
  })

  qrImage.value = URL.createObjectURL(await res.blob())
}

/* JSON → QR */
const generateJsonQR = async () => {
  if (!jsonText.value) {
    showAlert('JSON tidak boleh kosong')
    return
  }

  let parsed
  try {
    parsed = JSON.parse(jsonText.value)
  } catch {
    showAlert('Format JSON tidak valid')
    return
  }

  const res = await fetch('http://127.0.0.1:5000/generate-qr-from-json', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(parsed)
  })

  qrImage.value = URL.createObjectURL(await res.blob())
}

/* QR → TEXT */
const onFileChange = (e) => {
  selectedFile.value = e.target.files[0]
}

const decodeQR = async () => {
  if (!selectedFile.value) {
    showAlert('Pilih gambar QR terlebih dahulu')
    return
  }

  const formData = new FormData()
  formData.append('file', selectedFile.value)

  const res = await fetch('http://127.0.0.1:5000/decode-qr', {
    method: 'POST',
    body: formData
  })

  const data = await res.json()
  decodedText.value = data.text || 'QR tidak terbaca'
}
</script>
