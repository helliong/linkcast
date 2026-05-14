import asyncio
import re

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import BOT_TOKEN, ADMIN_IDS
from storage import (
    add_video,
    update_video_status,
    get_videos_by_status,
    get_video_by_id,
    get_videos_by_user,
)


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def is_supported_video_url(text: str) -> bool:
    pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be|rutube\.ru|vk\.com|vkvideo\.ru)/.+"
    return bool(re.match(pattern, text.strip()))


def get_platform(url: str) -> str:
    if "youtube.com" in url or "youtu.be" in url:
        return "YouTube"

    if "rutube.ru" in url:
        return "Rutube"

    if "vk.com" in url or "vkvideo.ru" in url:
        return "VK Video"

    return "Unknown"

def get_delete_keyboard(video_id: str):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="🗑 Удалить",
        callback_data=f"admin_delete|{video_id}",
    )

    return builder.as_markup()

def get_moderation_keyboard(video_id: str):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="✅ Одобрить",
        callback_data=f"approve|{video_id}",
    )

    builder.button(
        text="❌ Отклонить",
        callback_data=f"reject|{video_id}",
    )

    builder.button(
        text="🗑 Удалить",
        callback_data=f"delete|{video_id}",
    )

    builder.adjust(2, 1)

    return builder.as_markup()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

def get_status_label(status: str) -> str:
    labels = {
        "pending": "⏳ На модерации",
        "approved": "✅ Одобрено",
        "rejected": "❌ Отклонено",
        "deleted": "🗑 Удалено",
    }

    return labels.get(status, "Неизвестный статус")


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Привет! Я LinkCast Bot.\n\n"
        "Отправь мне ссылку на видео из YouTube, Rutube или VK Video, "
        "и я передам её на модерацию."
    )


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Как пользоваться ботом:\n\n"
        "1. Скопируй ссылку на видео\n"
        "2. Отправь её сюда\n"
        "3. Видео попадёт на модерацию\n"
        "4. После одобрения оно появится на сайте\n\n"
        "Команды:\n"
        "/start — запустить бота\n"
        "/help — помощь\n"
        "/my_videos — мои отправленные видео\n\n"
        "Поддерживаются ссылки:\n"
        "- YouTube\n"
        "- Rutube\n"
        "- VK Video"
    )
    
@dp.message(Command("admin_videos"))
async def admin_videos_command(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Нет доступа")
        return

    approved_videos = get_videos_by_status("approved")

    if not approved_videos:
        await message.answer("Одобренных видео пока нет.")
        return

    await message.answer(f"Найдено одобренных видео: {len(approved_videos)}")

    for index, video in enumerate(approved_videos, start=1):
        await message.answer(
            f"{index}. {video.get('title', 'Без названия')}\n\n"
            f"Платформа: {video.get('platform', 'unknown')}\n"
            f"Ссылка: {video.get('url')}\n"
            f"Дата: {video.get('createdAt')}\n\n"
            f"ID: {video.get('id')}",
            reply_markup=get_delete_keyboard(video["id"]),
        )

@dp.message(Command("myvideos"))
async def myvideos_command(message: Message):
    user_videos = get_videos_by_user(message.from_user.id)

    if not user_videos:
        await message.answer(
            "Ты пока не отправлял видео.\n\n"
            "Просто отправь мне ссылку на YouTube, Rutube или VK Video."
        )
        return

    await message.answer(f"Твои видео: {len(user_videos)}")

    for index, video in enumerate(user_videos, start=1):
        status = get_status_label(video.get("status"))

        await message.answer(
            f"{index}. {video.get('title', 'Без названия')}\n\n"
            f"Статус: {status}\n"
            f"Платформа: {video.get('platform', 'unknown')}\n"
            f"Ссылка: {video.get('url')}\n"
            f"Дата: {video.get('createdAt')}"
        )

@dp.message(F.text & ~F.text.startswith("/"))
async def handle_video_link(message: Message):
    text = message.text.strip()

    if not is_supported_video_url(text):
        await message.answer(
            "Это не похоже на поддерживаемую ссылку на видео.\n\n"
            "Отправь ссылку из YouTube, Rutube или VK Video."
        )
        return

    platform = get_platform(text)
    video = add_video(
    url=text,
    platform=platform,
    user_id=message.from_user.id,
    username=message.from_user.username,
)

    await message.answer(
        "Ссылка принята ✅\n\n"
        f"Платформа: {platform}\n"
        f"Ссылка: {text}\n\n"
        "Видео отправлено на модерацию."
    )

    for admin_id in ADMIN_IDS:
        await bot.send_message(
            chat_id=admin_id,
            text=(
                "Новое видео на модерацию 🎬\n\n"
                f"От пользователя: @{message.from_user.username}\n"
                f"Telegram ID: {message.from_user.id}\n"
                f"Платформа: {platform}\n"
                f"Ссылка: {text}\n\n"
                "Выбери действие:"
            ),
            reply_markup=get_moderation_keyboard(video["id"]),
        )
        

        
@dp.callback_query(F.data.startswith("admin_delete|"))
async def admin_delete_video(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    video_id = callback.data.split("|", 1)[1]

    video = get_video_by_id(video_id)

    if not video:
        await callback.answer("Видео не найдено", show_alert=True)
        return

    updated_video = update_video_status(video_id, "deleted")

    if not updated_video:
        await callback.answer("Не удалось удалить видео", show_alert=True)
        return

    await callback.message.edit_text(
        "Видео удалено 🗑\n\n"
        f"Название: {video.get('title', 'Без названия')}\n"
        f"Ссылка: {video.get('url')}\n\n"
        "Теперь оно не будет отображаться на сайте."
    )

    await callback.answer("Видео удалено")


@dp.callback_query(F.data.startswith("approve|"))
async def approve_video(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    video_id = callback.data.split("|", 1)[1]
    video = update_video_status(video_id, "approved")

    if not video:
        await callback.answer("Видео не найдено", show_alert=True)
        return

    await callback.message.edit_text(
        "Видео одобрено ✅\n\n"
        f"Название: {video['title']}\n"
        f"Ссылка: {video['url']}\n\n"
        "Теперь оно появится на сайте."
    )

    await callback.answer("Видео одобрено")


@dp.callback_query(F.data.startswith("reject|"))
async def reject_video(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    video_id = callback.data.split("|", 1)[1]
    video = update_video_status(video_id, "rejected")

    if not video:
        await callback.answer("Видео не найдено", show_alert=True)
        return

    await callback.message.edit_text(
        "Видео отклонено ❌\n\n"
        f"Ссылка: {video['url']}"
    )

    await callback.answer("Видео отклонено")
    
    


@dp.callback_query(F.data.startswith("delete|"))
async def delete_video(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    video_id = callback.data.split("|", 1)[1]
    video = update_video_status(video_id, "deleted")

    if not video:
        await callback.answer("Видео не найдено", show_alert=True)
        return

    await callback.message.edit_text(
        "Видео удалено 🗑\n\n"
        f"Ссылка: {video['url']}"
    )

    await callback.answer("Видео удалено")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())