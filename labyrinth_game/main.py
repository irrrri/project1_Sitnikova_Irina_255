#!/usr/bin/env python3

from labyrinth_game.constants import COMMANDS, ROOMS
from labyrinth_game.input_utils import get_input
from labyrinth_game.player_actions import (
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(game_state, command):
    if not command:
        return

    parts = command.split(' ', 1)
    cmd = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else None

    match cmd:
        case 'north' | 'south' | 'east' | 'west':
            move_player(game_state, cmd)

        case 'look':
            describe_current_room(game_state)

        case 'inventory':
            show_inventory(game_state)

        case 'go':
            if arg:
                move_player(game_state, arg.lower())
            else:
                print("Укажите направление. Пример: go north")

        case 'take':
            if arg:
                if arg.lower() == 'treasure_chest':
                    print("Вы не можете поднять сундук, он слишком тяжелый.")
                else:
                    take_item(game_state, arg.lower())
            else:
                print("Укажите предмет, который хотите взять. Пример: take torch")

        case 'use':
            if arg:
                use_item(game_state, arg.lower())
            else:
                print("Укажите предмет для использования. Пример: use torch")

        case 'solve':
            # Проверяем, находимся ли в treasure_room с сундуком
            if (
                    game_state['current_room'] == 'treasure_room' and
                    'treasure_chest' in ROOMS['treasure_room']['items']
            ):
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)

        case 'quit' | 'exit':
            print("Выход из игры. До свидания!")
            game_state['game_over'] = True

        case 'help':
            show_help(COMMANDS)

        case _:
            print("Неизвестная команда. Введите 'help' для справки.")


def main():
    # Инициализация состояния игрока
    game_state = {
        'player_inventory': [],  # Инвентарь игрока
        'current_room': 'entrance',  # Текущая комната
        'game_over': False,  # Значения окончания игры
        'steps_taken': 0  # Количество шагов
    }

    print("Добро пожаловать в Лабиринт сокровищ!")

    describe_current_room(game_state)

    # Основной игровой цикл
    while not game_state['game_over']:
        print()
        command = get_input("Введите команду: ").strip()
        process_command(game_state, command)


if __name__ == "__main__":
    main()
