import asyncio
import os
from fastapi import FastAPI, WebSocket
from crewai import Agent, Crew, Process, Task
from crewai.llm import LLM
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Gunakan model preview yang terbukti berhasil menembus blokade 503 di log-mu sebelumnya
gemini_llm = LLM(model="gemini/gemini-1.5-flash", api_key=os.getenv("GEMINI_API_KEY"))

@app.websocket("/ws/kantor")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"agen": "Sistem", "status": "idle", "pesan": "Kantor AI siap. Menunggu perintah..."})
    
    try:
        while True:
            # Menunggu tombol ditekan dari antarmuka web
            tugas_masuk = await websocket.receive_text()
            await websocket.send_json({"agen": "Sistem", "status": "sibuk", "pesan": f"Tugas diterima: {tugas_masuk}"})

            # Inisialisasi agen
            coder = Agent(
                role="Python Developer", 
                goal="Tulis skrip Python fungsional", 
                backstory="Programmer senior yang benci kode berantakan.", 
                llm=gemini_llm
            )
            reviewer = Agent(
                role="Code Reviewer", 
                goal="Cek dan optimalkan kode", 
                backstory="QA ketat yang selalu menemukan celah.", 
                llm=gemini_llm
            )
            
            tugas1 = Task(description=tugas_masuk, expected_output="Blok kode Python mentah", agent=coder)
            tugas2 = Task(description="Review dan refaktor kode dari tugas sebelumnya", expected_output="Kode final yang dioptimalkan", agent=reviewer)
            
            kru = Crew(agents=[coder, reviewer], tasks=[tugas1, tugas2], process=Process.sequential)

            # Pancarkan sinyal visual bahwa agen sedang lembur
            await websocket.send_json({"agen": "Coder", "status": "lembur", "pesan": "Mengetik algoritma..."})
            
            # Eksekusi CrewAI di thread terpisah agar tidak membekukan peladen WebSocket
            hasil = await asyncio.to_thread(kru.kickoff)
            
            # Pancarkan sinyal bahwa tugas bergeser ke reviewer, lalu selesai
            await websocket.send_json({"agen": "Reviewer", "status": "lembur", "pesan": "Mengevaluasi logika..."})
            await asyncio.sleep(2) # Jeda visual buatan
            await websocket.send_json({"agen": "Semua", "status": "selesai", "pesan": str(hasil)})

    except Exception as e:
        print(f"Koneksi antarmuka terputus: {e}")