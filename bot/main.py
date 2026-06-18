"""Entrypoint for the Telegram bot."""

import logging
import os

from telegram import Update
from telegram.ext import Application, ApplicationBuilder

from bot.handlers import error_handler, register_handlers, set_bot_commands


logger = logging.getLogger(__name__)


def configure_logging(level_name: str) -> None:
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        format="%(asctime)s %(name)s [%(levelname)s] %(message)s",
        level=level,
    )


def build_application() -> Application:
    token = os.getenv("BOT_TOKEN")
    application = (
        ApplicationBuilder()
        .token(token)
        .post_init(set_bot_commands)
        .build()
    )
    register_handlers(application)
    application.add_error_handler(error_handler)
    return application


if __name__ == "__main__":
    configure_logging(os.getenv("LOG_LEVEL", "INFO"))
    app = build_application()
    print("Bot en marche...")
    app.run_polling()
