import json
import uuid
# import yt_dlp
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
VIDEOS_FILE = BASE_DIR / "public" / "data" / "videos.json"

print("VIDEOS_FILE:", VIDEOS_FILE)


def read_videos():
    if not VIDEOS_FILE.exists():
        VIDEOS_FILE.parent.mkdir(parents=True, exist_ok=True)
        VIDEOS_FILE.write_text("[]", encoding="utf-8")

    text = VIDEOS_FILE.read_text(encoding="utf-8")

    if not text.strip():
        return []

    return json.loads(text)


def write_videos(videos):
    VIDEOS_FILE.parent.mkdir(parents=True, exist_ok=True)

    VIDEOS_FILE.write_text(
        json.dumps(videos, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def get_video_metadata(url):
    if "youtube.com" in url or "youtu.be" in url:
        return {
            "title": "YouTube video",
            "description": "Видео было добавлено через Telegram-бота.",
            "thumbnailUrl": get_thumbnail_url(url),
            "duration": None,
            "uploader": None,
        }

    if "rutube.ru" in url:
        return {
            "title": "Rutube video",
            "description": "Видео было добавлено через Telegram-бота.",
            "thumbnailUrl": get_thumbnail_url(url),
            "duration": None,
            "uploader": None,
        }

    if "vk.com" in url or "vkvideo.ru" in url:
        return {
            "title": "VK Video",
            "description": "Видео было добавлено через Telegram-бота.",
            "thumbnailUrl": get_thumbnail_url(url),
            "duration": None,
            "uploader": None,
        }

    return {
        "title": "Видео",
        "description": "Видео было добавлено через Telegram-бота.",
        "thumbnailUrl": get_thumbnail_url(url),
        "duration": None,
        "uploader": None,
    }


def add_video(url, platform, user_id, username):
    videos = read_videos()
    metadata = get_video_metadata(url)

    video = {
        "id": str(uuid.uuid4()),
        "title": metadata["title"],
        "description": metadata["description"],
        "url": url,
        "embedUrl": get_embed_url(url),
        "thumbnailUrl": metadata["thumbnailUrl"],
        "platform": platform.lower(),
        "category": "Video",
        "status": "pending",
        "duration": metadata["duration"],
        "uploader": metadata["uploader"],
        "addedByTelegramId": user_id,
        "addedByUsername": username,
        "createdAt": datetime.now().strftime("%Y-%m-%d"),
    }

    videos.append(video)
    write_videos(videos)

    return video

def get_videos_by_user(user_id):
    videos = read_videos()

    return [
        video
        for video in videos
        if video.get("addedByTelegramId") == user_id
    ]


def get_videos_by_status(status):
    videos = read_videos()
    return [video for video in videos if video.get("status") == status]


def get_video_by_id(video_id):
    videos = read_videos()

    for video in videos:
        if video.get("id") == video_id:
            return video

    return None


def update_video_status(video_id, status):
    videos = read_videos()

    for video in videos:
        if video.get("id") == video_id:
            video["status"] = status
            write_videos(videos)
            return video

    return None


def get_embed_url(url):
    if "youtube.com/watch?v=" in url:
        video_id = url.split("watch?v=")[1].split("&")[0]
        return f"https://www.youtube.com/embed/{video_id}"

    if "youtu.be/" in url:
        video_id = url.split("youtu.be/")[1].split("?")[0]
        return f"https://www.youtube.com/embed/{video_id}"

    if "rutube.ru/video/" in url:
        video_id = url.split("rutube.ru/video/")[1].split("/")[0]
        return f"https://rutube.ru/play/embed/{video_id}"

    return url


def get_thumbnail_url(url):
    if "youtube.com/watch?v=" in url:
        video_id = url.split("watch?v=")[1].split("&")[0]
        return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

    if "youtu.be/" in url:
        video_id = url.split("youtu.be/")[1].split("?")[0]
        return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

    return "/images/no-placeholder.jpg"
