import asyncio
import curses
from eth_account import Account
from utils.file_manager import load_yaml, load_txt
from utils.logger import logger
from data.const import menu_items
from pharos_client import PharosClient
from utils.menu import menu
from colorama import Fore, Style
import random
import os


settings = load_yaml('settings.yaml')
wallets = load_txt('data/wallets.txt')
proxies = load_txt('data/proxies.txt')

random.shuffle(wallets)

async def handle_account(private_key, action_name, proxy=None):
    pharos = PharosClient(private_key, proxy)
    wallet_address = Account.from_key(private_key).address
    try:
        await pharos.handle_wallet()
        action_func = getattr(pharos, action_name)
        await action_func()
    except KeyboardInterrupt:
        print(Fore.LIGHTYELLOW_EX + 'Script has finished' + Style.RESET_ALL)
    except Exception as e:
        logger.error(wallet_address, f'An error occurred while handling account: {e}')
    finally:
        await pharos.close_session()


async def main():
    if not wallets:
        print(Fore.RED + 'No wallets found' + Style.RESET_ALL)

    options = menu_items
    chosen_action = options[curses.wrapper(menu)]['func']
    os.system('cls' if os.name == 'nt' else 'clear')

    tasks = []

    if proxies:
        for w, p in zip(wallets, proxies):
            tasks.append(handle_account(private_key=w, proxy=p, action_name=chosen_action))
    else:
        for w in wallets:
            tasks.append(handle_account(private_key=w, action_name=chosen_action))

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())