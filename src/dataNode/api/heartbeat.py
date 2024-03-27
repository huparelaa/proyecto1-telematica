from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.post("/heartbeat")
def heartbeat():
    # Lógica para manejar el heartbeat aquí
    return {"status": "alive"}
