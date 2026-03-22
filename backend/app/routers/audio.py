"""Audio file serving endpoint."""

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.config import settings

router = APIRouter()


@router.get("/audio/{audio_id}")
async def get_audio(audio_id: str):
    """Serve audio response file.
    
    Returns the generated voice response audio file.
    """
    # Construct file path
    file_path = Path(settings.upload_dir) / f"response_{audio_id}.wav"
    
    # Security: validate that the path is within upload_dir
    try:
        file_path = file_path.resolve()
        upload_dir = Path(settings.upload_dir).resolve()
        if not str(file_path).startswith(str(upload_dir)):
            raise HTTPException(status_code=403, detail="Access denied")
    except Exception:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Check if file exists
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        file_path,
        media_type="audio/wav",
        headers={"Content-Disposition": f"attachment; filename={file_path.name}"},
    )
