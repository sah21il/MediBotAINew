from fastapi import FastAPI, HTTPException
from utils.message_schema import ObservationMessage
from nats.aio.client import Client as NATS
import asyncio
import json

app = FastAPI(title="Ingest Agent")

@app.on_event("startup")
async def startup_event():
    app.state.nc = NATS()
    await app.state.nc.connect("127.0.0.1:4222")  # NATS server

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.nc.close()

@app.post("/ingest")
async def ingest_data(message: ObservationMessage):
    try:
        data = message.dict()
        await app.state.nc.publish("observations", json.dumps(data).encode())
        return {"status": "success", "message_id": message.message_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
