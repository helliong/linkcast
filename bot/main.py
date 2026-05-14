import asyncio
import re

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import BOT_TOKEN, ADMIN_IDS


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


def get_moderation_keyboard(video_url: str):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="✅ Одобрить",
        callback_data=f"approve|{video_url}",
    )

    builder.button(
        text="❌ Отклонить",
        callback_data=f"reject|{video_url}",
    )

    builder.button(
        text="🗑 Удалить",
        callback_data=f"delete|{video_url}",
    )

    builder.adjust(2, 1)

    return builder.as_markup()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


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
        "Поддерживаются ссылки:\n"
        "- YouTube\n"
        "- Rutube\n"
        "- VK Video"
    )


@dp.message(F.text)
async def handle_video_link(message: Message):
    text = message.text.strip()

    if not is_supported_video_url(text):
        await message.answer(
            "Это не похоже на поддерживаемую ссылку на видео.\n\n"
            "Отправь ссылку из YouTube, Rutube или VK Video."
        )
        return

    platform = get_platform(text)

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
            reply_markup=get_moderation_keyboard(text),
        )


@dp.callback_query(F.data.startswith("approve|"))
async def approve_video(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    video_url = callback.data.split("|", 1)[1]

    await callback.message.edit_text(
        "Видео одобрено ✅\n\n"
        f"Ссылка: {video_url}\n\n"
        "Позже оно будет добавляться на сайт автоматически."
    )

    await callback.answer("Видео одобрено")


@dp.callback_query(F.data.startswith("reject|"))
async def reject_video(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    video_url = callback.data.split("|", 1)[1]

    await callback.message.edit_text(
        "Видео отклонено ❌\n\n"
        f"Ссылка: {video_url}"
    )

    await callback.answer("Видео отклонено")


@dp.callback_query(F.data.startswith("delete|"))
async def delete_video(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    video_url = callback.data.split("|", 1)[1]

    await callback.message.edit_text(
        "Видео удалено 🗑\n\n"
        f"Ссылка: {video_url}"
    )

    await callback.answer("Видео удалено")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())