#!/usr/bin/env python3
"""
Servidor proxy para receber dados do formulário da lista de espera
e gravar na planilha do Google Sheets via gws CLI.
"""
import json
import subprocess
import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# Permitir CORS de qualquer origem (o formulário vem de brilliant.ia.br)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

SPREADSHEET_ID = "1795DSX-xT6BLyIO5v6swx7_AAIDC4mKzE4AjY5_h2tY"

@app.post("/submit")
async def submit_form(request: Request):
    try:
        body = await request.json()
        nome = body.get("nome", "").strip()
        email = body.get("email", "").strip()
        whatsapp = body.get("whatsapp", "").strip()
        turma = body.get("turma", "").strip()

        if not nome or not email or not whatsapp:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Campos obrigatórios faltando"}
            )

        # Gerar timestamp
        now = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

        # Gravar na planilha via gws CLI
        json_values = json.dumps([[now, nome, email, whatsapp, turma]])
        result = subprocess.run(
            [
                "gws", "sheets", "+append",
                "--spreadsheet", SPREADSHEET_ID,
                "--json-values", json_values
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print(f"gws error: {result.stderr}")
            return JSONResponse(
                status_code=500,
                content={"status": "error", "message": "Erro ao gravar na planilha"}
            )

        return JSONResponse(
            status_code=200,
            content={"status": "success", "message": "Inscrição realizada com sucesso!"}
        )

    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)
