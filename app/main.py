from fastapi import FastAPI
from exams.routes import router as exam_router
from auth.routes import router as user_router

app = FastAPI(title="Certification API", version="0.1")

app.include_router(exam_router, prefix="/exams", tags=["exams"])
app.include_router(user_router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Certification API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)