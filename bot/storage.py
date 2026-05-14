import json
import uuid
import requests
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, parse_qs

from config import YOUTUBE_API_KEY


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

def get_youtube_video_id(url):
    parsed_url = urlparse(url)

    if parsed_url.netloc in ["www.youtube.com", "youtube.com", "m.youtube.com"]:
        query = parse_qs(parsed_url.query)
        return query.get("v", [None])[0]

    if parsed_url.netloc in ["youtu.be", "www.youtu.be"]:
        return parsed_url.path.strip("/")

    if "youtube.com/shorts/" in url:
        return parsed_url.path.split("/shorts/")[1].split("/")[0]

    return None

def get_youtube_metadata(url):
    video_id = get_youtube_video_id(url)

    if not video_id:
        return None

    if not YOUTUBE_API_KEY:
        print("YOUTUBE_API_KEY не найден в .env")
        return None

    api_url = "https://www.googleapis.com/youtube/v3/videos"

    params = {
        "part": "snippet,contentDetails",
        "id": video_id,
        "key": YOUTUBE_API_KEY,
    }

    try:
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        items = data.get("items", [])

        if not items:
            return None

        item = items[0]
        snippet = item.get("snippet", {})
        content_details = item.get("contentDetails", {})

        thumbnails = snippet.get("thumbnails", {})
        thumbnail_url = (
            thumbnails.get("maxres", {}).get("url")
            or thumbnails.get("high", {}).get("url")
            or thumbnails.get("medium", {}).get("url")
            or thumbnails.get("default", {}).get("url")
            or get_thumbnail_url(url)
        )

        return {
            "title": snippet.get("title") or "YouTube video",
            "description": snippet.get("description") or "Описание отсутствует.",
            "thumbnailUrl": thumbnail_url,
            "duration": content_details.get("duration"),
            "uploader": snippet.get("channelTitle"),
        }

    except Exception as error:
        print("Ошибка YouTube API:", error)
        return None

def get_video_metadata(url):
    if "youtube.com" in url or "youtu.be" in url:
        metadata = get_youtube_metadata(url)

        if metadata:
            return metadata

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
    youtube_id = get_youtube_video_id(url)

    if youtube_id:
        return f"https://www.youtube.com/embed/{youtube_id}"

    if "rutube.ru/video/" in url:
        video_id = url.split("rutube.ru/video/")[1].split("/")[0]
        return f"https://rutube.ru/play/embed/{video_id}"

    return url


def get_thumbnail_url(url):
    youtube_id = get_youtube_video_id(url)

    if youtube_id:
        return f"https://img.youtube.com/vi/{youtube_id}/hqdefault.jpg"

    return "/images/no-placeholder.jpg"
