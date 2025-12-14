# labyrinth_game/utils.py

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
    correct_answer = str(answer).strip().lower()

    if user_answer == correct_answer:
        print("Правильно! Вы успешно решили загадку.")
        # Убираем загадку, чтобы её нельзя было решить дважды
        room['puzzle'] = None

        # Пример награды: добавляем предмет в инвентарь
        reward_item = "gold_coin"
        game_state['player_inventory'].append(reward_item)
        print(f"В награду вы получили: {reward_item}")
    else:
        print("Неверно. Попробуйте снова.")


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


def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")