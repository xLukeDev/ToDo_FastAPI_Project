from fastapi import FastAPI
from routers import tasks, auth, register, raport
app = FastAPI()

app.include_router(tasks.router)
app.include_router(register.router)
app.include_router(auth.router)
app.include_router(raport.router)
@app.get("/")
async def root():
    return {"message": "API WORKS!"}