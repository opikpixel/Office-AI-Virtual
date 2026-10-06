import os
import requests
from dotenv import load_dotenv

# Muat kunci dari .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Kunci API tidak ditemukan.")
    exit()

print("Mengambil daftar model resmi dari server Google...\n")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("--- DAFTAR MODEL YANG BISA KAMU PAKAI ---")
    for model in data.get('models', []):
        # Hanya tampilkan model pembuat teks (generateContent)
        if 'generateContent' in model.get('supportedGenerationMethods', []):
            print(f"- {model['name']}")
else:
    print(f"Gagal mengambil data. Status: {response.status_code}")
    print(response.text)