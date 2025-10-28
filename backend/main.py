from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from telesat_sim import run_simulation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/simulate")
def simulate():
    data = run_simulation()
    return {"simulation": data}
