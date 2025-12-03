import os
import json
import random


STATS_DIR = "game_stats"
STATS_FILE = os.path.join(STATS_DIR, "stats.json")

def initialize_stats_file():
   
    if not os.path.exists(STATS_DIR):
        os.makedirs(STATS_DIR)
        print(f"Директория '{STATS_DIR}' создана.")
    
    if not os.path.exists(STATS_FILE):
        
        initial_stats = {"X_wins": 0, "O_wins": 0, "Draws": 0}
        with open(STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(initial_stats, f, indent=4)
        print(f"Файл статистики '{STATS_FILE}' создан.")

def load_stats():
    
    try:
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"X_wins": 0, "O_wins": 0, "Draws": 0}

def save_stats(stats):
   
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=4)

def update_stats(winner=None):
    
    stats = load_stats()
    if winner == "X":
        stats["X_wins"] += 1
    elif winner == "O":
        stats["O_wins"] += 1
    elif winner == "Draw":
        stats["Draws"] += 1
    save_stats(stats)

def display_stats():
    
    stats = load_stats()
    print("\n--- СТАТИСТИКА ИГР ---")
    print(f"Побед X: {stats['X_wins']}")
    print(f"Побед O: {stats['O_wins']}")
    print(f"Ничьих: {stats['Draws']}")
    print("----------------------\n")

def display_board(board, size):
   
   
    header = "   " + "  ".join(map(str, range(1, size + 1)))
    print(header)
    print("  " + "+--" * size + "+")

    for i in range(size):
        row_str = f"{i + 1} |"
        for j in range(size):
            index = i * size + j
            cell_content = board[index] if board[index] != " " else " "
            row_str += f" {cell_content} |"
        print(row_str)
        print("  " + "+--" * size + "+")

def check_win(board, player, size, win_length):
    
    def check_line(start_index, dx, dy):
        for k in range(win_length):
            idx = start_index + k * dx + k * dy * size
            if idx < 0 or idx >= len(board) or board[idx] != player:
                return False
        return True

    for i in range(size):
        for j in range(size):
            start = i * size + j
            if j <= size - win_length and check_line(start, 1, 0): return True
            if i <= size - win_length and check_line(start, 0, 1): return True
            if i <= size - win_length and j <= size - win_length and check_line(start, 1, 1): return True
            if i <= size - win_length and j >= win_length - 1 and check_line(start, -1, 1): return True
    return False

def check_draw(board):
    
    return " " not in board

def run_game_session(BOARD_SIZE, WIN_LENGTH):
    
    board = [" "] * (BOARD_SIZE * BOARD_SIZE)
    # Оценка 4: Случайный выбор первого игрока
    current_player = random.choice(["X", "O"])
    game_running = True

    print(f"\n--- Начало новой игры на поле {BOARD_SIZE}x{BOARD_SIZE} ---")
    print(f"Игрок '{current_player}' ходит первым (выбран случайно).")

    while game_running:
        display_board(board, BOARD_SIZE)
        move = None
        while move is None:
            try:
                user_input = input(f"Игрок '{current_player}', введите координаты хода (строка столбец): ")
                row_str, col_str = user_input.split()
                row = int(row_str) - 1
                col = int(col_str) - 1
                
                if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
                    print(f"Координаты вне диапазона. Введите числа от 1 до {BOARD_SIZE}.")
                    continue
                
                move = row * BOARD_SIZE + col

                if board[move] != " ":
                    print("Эта ячейка уже занята. Выберите другую.")
                    move = None
                    continue

            except ValueError:
                print("Некорректный ввод. Пожалуйста, введите две цифры, разделенные пробелом (например, '4 5').")
                continue
        
        board[move] = current_player
        
        if check_win(board, current_player, BOARD_SIZE, WIN_LENGTH):
            display_board(board, BOARD_SIZE)
            print(f"Игрок '{current_player}' победил! 🎉")
            update_stats(winner=current_player)
            game_running = False
        elif check_draw(board):
            display_board(board, BOARD_SIZE)
            print("Ничья! 🤝")
            update_stats(winner="Draw")
            game_running = False
        else:
            current_player = "O" if current_player == "X" else "X"

def main_menu():
    """Главное меню игры."""
    initialize_stats_file()
    
    
    while True:
        try:
            size_input = input("Введите размер игрового поля (например, 3 для 3x3, 9 для 9x9): ")
            BOARD_SIZE = int(size_input)
            if BOARD_SIZE < 3:
                print("Размер поля должен быть не менее 3.")
                continue

            win_length_input = input(f"Сколько символов нужно для победы? (Рекомендуется 3 для 3x3 или 5 для 9x9): ")
            WIN_LENGTH = int(win_length_input)
            if WIN_LENGTH > BOARD_SIZE or WIN_LENGTH < 3:
                 print(f"Длина победной серии должна быть от 3 до {BOARD_SIZE}.")
                 continue
            break
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите целое число.")
    
    
    while True:
        run_game_session(BOARD_SIZE, WIN_LENGTH)
        display_stats()
        
        play_again = input("Хотите сыграть еще раз? (да/нет): ").lower()
        if play_again != 'да' and play_again != 'yes' and play_again != 'д' and play_again != 'y':
            print("Спасибо за игру! До свидания.")
            break

if __name__ == "__main__":
    main_menu()
