import os
from crewai import Agent, Crew, Process, Task
from crewai.llm import LLM
from dotenv import load_dotenv

# Muat variabel dari file .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Konfigurasi LLM menggunakan model Gemini via CrewAI LLM wrapper
# Pastikan menggunakan model yang didukung, contoh: gemini-1.5-pro atau gemini-2.5-flash
gemini_llm = LLM(model="gemini/gemini-3-flash-preview", api_key=api_key)

# 1. Definisikan Agen Pertama (Spesialis Pemrograman)
coder_agent = Agent(
    role="Python Developer",
    goal="Menulis skrip Python yang bersih dan fungsional berdasarkan instruksi.",
    backstory=(
        "Kamu adalah seorang *software engineer* berpengalaman yang "
        "fokus menulis kode modular, efisien, dan bebas bug."
    ),
    verbose=True,
    llm=gemini_llm,
)

# 2. Definisikan Agen Kedua (Spesialis Peninjau/Reviewer)
reviewer_agent = Agent(
    role="Code Reviewer",
    goal=(
        "Meninjau kode yang ditulis oleh Coder, mencari celah error, dan"
        " memberikan versi perbaikan."
    ),
    backstory=(
        "Kamu adalah pengawas kualitas kode yang teliti, kritis, dan "
        "memastikan tidak ada kesalahan logika sebelum kode digunakan."
    ),
    verbose=True,
    llm=gemini_llm,
)

# 3. Definisikan Tugas (Tasks)
task_coding = Task(
    description=(
        "Buat skrip Python sederhana untuk sistem lampu lalu lintas otomatis"
        " menggunakan logika kondisional."
    ),
    expected_output=(
        "Blok kode Python yang berfungsi lengkap beserta penjelasan singkat."
    ),
    agent=coder_agent,
)

task_review = Task(
    description=(
        "Periksa kode Python yang telah dibuat oleh Coder. Berikan catatan"
        " perbaikan atau pastikan kode sudah optimal."
    ),
    expected_output="Laporan hasil tinjauan dan kode final yang sudah disempurnakan.",
    agent=reviewer_agent,
)

# 4. Gabungkan ke dalam Crew (Orkestrasi Alur Kerja)
office_crew = Crew(
    agents=[coder_agent, reviewer_agent],
    tasks=[task_coding, task_review],
    process=Process.sequential,  # Tugas dikerjakan berurutan (dari Coder ke Reviewer)
    verbose=True,
)

# 5. Jalankan Sistem
if __name__ == "__main__":
    print("## Memulai Simulasi Kantor AI di Terminal ##")
    result = office_crew.kickoff()
    print("\n\n########################")
    print("## Hasil Akhir Pekerjaan ##")
    print("########################\n")
    print(result)