from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import json

# Create test app
app = FastAPI(title="Test")

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", '["http://localhost:3000", "http://127.0.0.1:3000"]')
if isinstance(cors_origins, str):
    cors_origins = json.loads(cors_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)