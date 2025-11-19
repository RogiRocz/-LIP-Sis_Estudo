from fastapi import FastAPI

app = FastAPI(title="LIP - Sis_Estudo API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Study System API"}
