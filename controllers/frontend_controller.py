from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["frontend"])

@router.get("/", response_class=HTMLResponse)
async def read_root():
    """
    Serve frontend application
    """
    try:
        with open("frontend/dist/index.html", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Frontend not found. Please run build.</h1>"
