import asyncio
import os

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot

from bot.loader import registrar_comandos, registrar_query_handlers, remover_mensagens_expiradas

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = AsyncTeleBot(TOKEN)


async def main() -> None:
    print("O Bot está funcionando")

    await registrar_comandos(bot)
    await registrar_query_handlers(bot)
    print("Os comandos e handlers foram registrados")

    asyncio.create_task(remover_mensagens_expiradas())

    # Não responde comandos mandados enquanto ele estava offline
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.infinity_polling()


if __name__ == "__main__":
    asyncio.run(main())
