from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerChannel, InputUser, InputPeerEmpty
from telethon.errors import PeerFloodError, ButtonUserPrivacyRestrictedError
import asyncio
import configparser

# Lê as configurações a partir do arquivo Config_ini.txt:
config = configparser.ConfigParser()
config.read('Config_ini.txt')

class TelegramBot:
    def __init__(self):
        # Obtém as informações de configuração do arquivo de configuração (o txt):
        self.api_id = int(config.get('telegram', 'api_id'))
        self.api_hash = config.get('telegram', 'api_hash')
        self.phone = config.get('telegram', 'phone')
        self.session_file = "my_session"
        self.client = TelegramClient(self.session_file, self.api_id, self.api_hash)

    async def connect(self):
        # Inicia a sessão e autentica o usuário, se necessário:
        await self.client.start(self.phone)
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone)
            await self.client.sign_in(self.phone, input('Digite o código:'))

    async def get_groups(self):
        # Conecta e obtém informações sobre os grupos disponíveis:
        await self.connect()
        groups = {}
        chats = await self.client.get_dialogs()

        for chat in chats:
            # Verifica se o chat é um grupo (megagroup):
            if hasattr(chat.entity, 'megagroup') and chat.entity.megagroup:
                groups[chat.entity.title] = chat.entity

        return groups

    async def get_user_by_phone(self, phone):
        # Encontra um usuário com base no número de telefone:
        user = await self.client.get_entity(phone)
        return user if user else None

    async def add_member_to_group(self, phone, group_name):
        # Adicionar um usuário a um grupo com base no número de telefone:
        user = await self.get_user_by_phone(phone)
        if user:
            groups = await self.get_groups()
            group = groups.get(group_name)
            if group:
                try:
                    # Informações necessárias para adicionar o usuário ao grupo:
                    target_group_entity = InputPeerChannel(group.id, group.access_hash)
                    # Solicitação de adição do usuário ao grupo:
                    await self.client(InviteToChannelRequest(target_group_entity, [InputUser(user.id)]))
                    print(f'Usuário com número de telefone {phone} adicionado ao grupo {group_name}.')
                except PeerFloodError:
                    print('Erro de flood. Dormindo por 1h.')
                    await asyncio.sleep(3600)
                except ButtonUserPrivacyRestrictedError:
                    print('Usuário não permite ser adicionado no grupo')
                except Exception as e:
                    print(str(e))
            else:
                print(f"Grupo com nome '{group_name}' não encontrado.")
        else:
            print(f"Usuário com número de telefone '{phone}' não encontrado.")

if __name__ == '__main__':
    bot = TelegramBot()
    bot.client.start()
    
    # Número de telefone e nome do grupo desejados:
    target_phone = 'xxxxxxxxxxx'
    target_group_name = 'xxxxxxxx'
    
    # Adicionar o usuário ao grupo usando o número de telefone:
    asyncio.get_event_loop().run_until_complete(bot.add_member_to_group(target_phone, target_group_name))
