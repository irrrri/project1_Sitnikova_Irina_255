# labyrinth_game/utils.py

import math

from labyrinth_game.constants import ROOMS
from labyrinth_game.input_utils import get_input


def describe_current_room(game_state):
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]

    print(f"\n== {current_room_name.upper()} ==")

    print(room['description'])

    if room['items']:
        print("Заметные предметы:", ", ".join(room['items']))

    exits = room['exits']
    if exits:
        print("Выходы:", ", ".join(exits.keys()))

    if room['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]

    if not room['puzzle']:
        print("Загадок здесь нет.")
        return

    question, answer = room['puzzle']
    print(f"\nЗагадка: {question}")

    user_answer = get_input("Ваш ответ: ").strip().lower()

    correct_answers = {str(answer).strip().lower()}

    if str(answer) == '10':
        correct_answers.add('десять')

    if user_answer in correct_answers:
        print("Правильно! Вы успешно решили загадку.")

        room['puzzle'] = None

        # Награды зависят от комнаты
        rewards_by_room = {
            'hall': 'silver_coin',
            'library': 'gold_coin',
            'hidden_cave': 'crystal',
            'trap_room': None,        # ловушка — не награждаем
            'treasure_room': None,    # награда — сундук
        }

        reward = rewards_by_room.get(current_room_name)

        if reward:
            game_state['player_inventory'].append(reward)
            print(f"В награду вы получили: {reward}")
        else:
            print("Вы ничего не получили в награду.")

    else:
        print("Неверный ответ.")

        if current_room_name == 'trap_room':
            trigger_trap(game_state)
        else:
            print("Попробуйте снова.")


def attempt_open_treasure(game_state):
    """
    Логика открытия treasure_chest в комнате treasure_room.
    """
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]

    if 'treasure_chest' not in room.get('items', []):
        print("Сундук уже открыт или отсутствует.")
        return

    inventory = game_state['player_inventory']

    # Если есть ключ
    if 'treasure_key' in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return

    # Если ключа нет, предлагаем ввести код
    choice = get_input(
        "Сундук заперт. Попробовать ввести код? (да/нет): "
    ).strip().lower()
    if choice == 'да':
        if not room.get('puzzle'):
            print("Код неизвестен. Вы не можете открыть сундук.")
            return
        _, correct_code = room['puzzle']
        user_code = get_input("Введите код: ").strip()
        if user_code == str(correct_code):
            print("Код верный! Сундук открыт!")
            room['items'].remove('treasure_chest')
            print("В сундуке сокровище! Вы победили!")
            game_state['game_over'] = True
            # Убираем загадку, чтобы её нельзя было решить дважды
            room['puzzle'] = None
        else:
            print("Неверный код. Сундук остается закрытым.")
    else:
        print("Вы отступаете от сундука.")


def show_help(commands):
    print("\nДоступные команды:")
    for command, description in commands.items():
        print(f"{command:<16} {description}")


def pseudo_random(seed: int, modulo: int) -> int:
    if modulo <= 0:
        return 0

    x = math.sin(seed * 12.9898) * 43758.5453
    fractional = x - math.floor(x)
    return int(fractional * modulo)


def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state['player_inventory']

    # Если есть предметы — теряем один случайный
    if inventory:
        index = pseudo_random(game_state['steps_taken'], len(inventory))
        lost_item = inventory.pop(index)
        print(f"Вы потеряли предмет: {lost_item}")
        return

    # Если инвентарь пуст — риск смерти
    danger = pseudo_random(game_state['steps_taken'], 10)
    if danger < 3:
        print("Ловушка смертельна... Вы погибли.")
        game_state['game_over'] = True
    else:
        print("Вы чудом уцелели.")


def random_event(game_state):
    # Проверяем, произойдет ли событие
    event_chance = pseudo_random(game_state['steps_taken'], 10)
    if event_chance != 0:
        return

    event_type = pseudo_random(game_state['steps_taken'], 3)
    current_room = game_state['current_room']
    room = ROOMS[current_room]
    inventory = game_state['player_inventory']

    # Сценарий 1 — находка
    if event_type == 0:
        print("Вы заметили что-то на полу — это монетка!")
        room['items'].append('coin')

    # Сценарий 2 — испуг
    elif event_type == 1:
        print("Вы слышите зловещий шорох в темноте...")
        if 'sword' in inventory:
            print("Вы выхватываете меч, и существо убегает.")

    # Сценарий 3 — ловушка
    elif event_type == 2:
        if current_room == 'trap_room' and 'torch' not in inventory:
            print("В темноте вы не заметили опасность!")
            trigger_trap(game_state)