import logging
import sys
import ssl

from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.types import FSInputFile
from asyncio import run
from config import settings_bot, web_hook_settings, start_settings
from handlerss import base_handler
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

bot = Bot(
    token=settings_bot.bot_token,
    parse_mode="HTML"
)


async def main():
    dp = Dispatcher()
    dp.include_routers(
        base_handler.router
    )
    if start_settings.is_webhook:
        main_web_hook(
            dp=dp
        )
    else:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(
            bot
        )


async def on_startup(bot_: Bot) -> None:
    if start_settings.is_webhook and start_settings.is_ssl:
        await bot.set_webhook(
            f"{web_hook_settings.base_webhook_url}{web_hook_settings.webhook_path}",
            certificate=FSInputFile(web_hook_settings.webhook_ssl_cert),
            secret_token=web_hook_settings.webhook_secret,
        )
    else:
        await bot_.set_webhook(url=f"{web_hook_settings.base_webhook_url}{web_hook_settings.webhook_path}",
                               secret_token=web_hook_settings.webhook_secret)


def main_web_hook(dp: Dispatcher) -> None:
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=web_hook_settings.webhook_secret,
    )
    webhook_requests_handler.register(app, path=web_hook_settings.webhook_path)

    setup_application(app,
                      dp,
                      bot=bot)

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(web_hook_settings.webhook_ssl_cert,
                            web_hook_settings.webhook_ssl_priv)

    web.run_app(app, host=web_hook_settings.web_server_host,
                port=web_hook_settings.web_server_port,
                ssl_context=context)


if __name__ == "__main__":
    run(main=main())
