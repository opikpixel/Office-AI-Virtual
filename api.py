import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("GAGAL: Kunci API tidak terbaca.")
    exit()

print("Mencoba koneksi ke Google AI Studio dengan SDK baru...")

try:
    # Inisialisasi client baru
    client = genai.Client(api_key=api_key)

    # Tembak prompt sederhana ke model 1.5-flash
    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents="Balas pesan ini dengan kata 'KONEKSI BERHASIL' saja."
    )

    print("\n--- HASIL ---")
    print("Status: SUKSES")
    print("Respons AI:", response.text.strip())

except Exception as e:
    print("\n--- HASIL ---")
    print("Status: GAGAL TOTAL")
    print("Detail Error:", e)