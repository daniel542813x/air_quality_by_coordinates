from fastapi import FastAPI
from routes import air_quality

app = FastAPI()
app.include_router(air_quality.router)


@app.get("/")
async def root():
 return {
        "message": "Welcome to the Air Quality API"
 }