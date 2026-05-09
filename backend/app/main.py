from fastapi import FastAPI

app = FastAPI(
    title="PhishGuard API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "PhishGuard API Running"
    }