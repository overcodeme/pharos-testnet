import asyncio
import curses
from utils.file_manager import load_yaml, load_txt
from data.const import menu_items
from utils.menu import menu


settings = load_yaml('settings.yaml')
wallets = load_txt('data/wallets.txt')

async def main():
    options = menu_items
    chosen_action = options[curses.wrapper(menu)]



if __name__ == '__main__':
    asyncio.run(main())