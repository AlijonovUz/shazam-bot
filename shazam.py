import os
import uuid
import asyncio
from shazamio import Shazam

_shazam = Shazam()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _recognize_sync(file_path: str) -> dict | None:
    try:
        return asyncio.run(_shazam.recognize(file_path))
    except Exception:
        return None


def recognize(bot, message) -> dict | None:
    if message.content_type == "voice":
        file_id = message.voice.file_id
        ext = "ogg"
    elif message.content_type == "audio":
        file_id = message.audio.file_id
        ext = "mp3"
    elif message.content_type == "video_note":
        file_id = message.video_note.file_id
        ext = "mp4"
    elif message.content_type == "video":
        file_id = message.video.file_id
        ext = "mp4"
    else:
        return None

    file_info = bot.get_file(file_id)
    data = bot.download_file(file_info.file_path)

    file_name = f"{uuid.uuid4()}.{ext}"
    path = os.path.join(UPLOAD_DIR, file_name)

    with open(path, "wb") as file:
        file.write(data)

    result = _recognize_sync(path)

    try:
        os.remove(path)
    except OSError:
        pass

    return result