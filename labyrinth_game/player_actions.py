# labyrinth_game/player_actions.py

from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room


def show_inventory(game_state):
    inventory = game_state.get('player_inventory', [])

    if inventory:
        print("Ваш инвентарь содержит:")
        for item in inventory:
            print(f"- {item}")
    else:
        print("Ваш инвентарь пуст.")


def move_player(game_state, direction):
    current_room = game_state['current_room']
    exits = ROOMS[current_room]['exits']

    if direction in exits:
        # Обновляем текущую комнату
        game_state['current_room'] = exits[direction]
        # Увеличиваем счетчик шагов
        game_state['steps_taken'] += 1
        # Описание новой комнаты
        describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state, item_name):
    current_room = game_state['current_room']
    room_items = ROOMS[current_room]['items']

    if item_name in room_items:
        # Добавляем предмет в инвентарь
        game_state['player_inventory'].append(item_name)
        # Удаляем предмет из комнаты
        room_items.remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state, item_name):
    """
    Использует предмет из инвентаря игрока.
    Выполняет уникальные действия для каждого предмета.
    """
    inventory = game_state.get('player_inventory', [])

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    match item_name.lower():
        case 'torch':
            print("Вы зажгли факел. Стало светлее и легче ориентироваться.")
        case 'sword':
            print("Вы держите меч в руках. Чувствуете уверенность и силу.")
        case 'bronze_box' | 'bronze box':
            print("Вы открыли бронзовую шкатулку.")
            if 'rusty_key' not in inventory:
                inventory.append('rusty_key')
                print("Внутри вы нашли: rusty_key")
            else:
                print("Внутри ничего нового нет.")
        case _:
            print("Вы не знаете, как использовать этот предмет.")