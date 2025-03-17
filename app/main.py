from fastapi import FastAPI
from exams.routes import router as exam_router
from auth.routes import router as user_router
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

app = FastAPI(
    title="Certification API",
    version="0.1",
    description="API for managing user authentication and exam certification.",
    docs_url=None,  # Disable default docs URL
    redoc_url=None  # Disable default redoc URL
)

app.include_router(exam_router)
app.include_router(user_router)


@app.get("/", tags=["Root"], summary="Welcome endpoint")
def read_root():
    """
    Root endpoint providing a welcome message.

    Returns:
        dict: Welcome message.
    """
    return {"message": "Welcome to the Certification API"}


@app.get("/docs", include_in_schema=False)
def custom_swagger_ui():
    """
    Serve the Swagger UI documentation at a custom URL.

    Returns:
        HTMLResponse: Swagger UI page.
    """
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Certification API Docs")


@app.get("/redoc", include_in_schema=False)
def custom_redoc():
    """
    Serve the ReDoc documentation at a custom URL.

    Returns:
        HTMLResponse: ReDoc page.
    """
    return get_redoc_html(openapi_url="/openapi.json", title="Certification API ReDoc")


@app.get("/health", tags=["Monitoring"], summary="Health check endpoint")
def health_check():
    """
    Health check endpoint to verify API status.

    Returns:
        dict: Status message.
    """
    return {"status": "ok", "uptime": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
