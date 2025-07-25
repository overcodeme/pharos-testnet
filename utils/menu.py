import curses
from data.const import menu_items, badges


def menu(stdscr: curses.window):
    stdscr.clear()
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    options = menu_items
    badges_menu = [b for b in badges.keys()]
    badges_menu.append('Back')
    current_row = 0

    while True:
        for idx, action in enumerate(options):
            if idx == current_row:
                stdscr.addstr(idx, 0, f'-> {action["name"]}', curses.color_pair(1))

                stdscr.move(len(options), 0)
                stdscr.clrtoeol()

                stdscr.addstr(len(options), 0, f'{action["description"]}', curses.color_pair(2))
            else:
                stdscr.addstr(idx, 0, f'   {action["name"]}')

        stdscr.refresh()
        key = stdscr.getch()
        
        if key == curses.KEY_UP:
            if current_row > 0:
                current_row -= 1
            else:
                current_row = len(options) - 1
        elif key == curses.KEY_DOWN:
            if current_row < len(options) - 1:
                current_row += 1
            else:
                current_row = 0
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if options[current_row]['name'] == 'Mint Badge':
                current_row_badge = 0
                while True:
                    stdscr.clear()
                    for i, badge_menu_item in enumerate(badges_menu):
                        if i == current_row_badge:
                            stdscr.addstr(i, 0, f'-> {badge_menu_item}', curses.color_pair(1))
                        else:
                            stdscr.addstr(i, 0, f'   {badge_menu_item}')

                    stdscr.refresh()
                    key_badge = stdscr.getch()

                    if key_badge == curses.KEY_UP:
                        if current_row_badge > 0:
                            current_row_badge -= 1
                        else:
                            current_row_badge = len(badges_menu) - 1
                    elif key_badge == curses.KEY_DOWN:
                        if current_row_badge < len(badges_menu) - 1:
                            current_row_badge += 1
                        else:
                            current_row_badge = 0
                    elif key_badge == curses.KEY_ENTER or key in [10, 13]:
                        if current_row_badge == len(badges_menu) - 1:
                            break
                        return ['mint_badge', badges[badges_menu[current_row_badge]]]
            else:
                return options[current_row]['func']