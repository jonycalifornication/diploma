import asyncio
import logging

from src.decorators import bot_mode


@bot_mode
async def main():
    """Основная функция запуска."""
    pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
