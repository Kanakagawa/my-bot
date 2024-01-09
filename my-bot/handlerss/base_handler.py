from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import html


router = Router()


@router.message(Command("start"))
async def start_command(message: Message):
    await message.reply(
        text=f"Hello {html.bold(html.quote(message.from_user.full_name))}"
    )
