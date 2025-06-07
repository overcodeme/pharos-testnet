import asyncio
import curses
from eth_account import Account
from utils.file_manager import load_yaml, load_txt
from utils.logger import logger
from data.const import menu_items
from pharos_client import PharosClient
from utils.menu import menu
from colorama import Fore, Style


settings = load_yaml('settings.yaml')
wallets = load_txt('data/wallets.txt')
proxies = load_txt('data/proxies.txt')

async def handle_account(private_key, proxy, action_name):
    pc = PharosClient(private_key, proxy)
    wallet_address = Account.from_key(private_key).address
    try:
        action_func = getattr(pc, action_name)
        await action_func()
    except Exception as e:
        logger.error(wallet_address, f'An error occurred: {e}')


async def main():
    if not wallets:
        print(Fore.RED + 'No wallets found' + Style.RESET_ALL)

    if not proxies:
        print(Fore.RED + 'No proxies found' + Style.RESET_ALL)

    options = menu_items
    chosen_action = options[curses.wrapper(menu)]['func']

    tasks = []
    for w, p in zip(wallets, proxies):
        tasks.append(await handle_account(w, p, chosen_action))

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())