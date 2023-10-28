from telegram import TelegramBot

async def main():
    api_id = 23526290
    api_hash = '0af6fc05a7da3555e23722f44feb523f'
    phone = '+5511967211161'

    bot = TelegramBot(api_id, api_hash, phone)

    print("Iniciando robô...")
    print("Escolhendo grupo alvo")
    grupo_alvo = await bot.get_groups()
    membros = await bot.get_members_of_group(grupo_alvo)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
