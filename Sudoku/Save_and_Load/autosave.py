import os
import pickle

def autosave_game(save_dir, board_data, last_saved_filename=None):
    """Автоматически сохраняет игру."""
    if last_saved_filename:
        file_path = os.path.join(save_dir, last_saved_filename + ".sudoku")
    else:
        autosave_number = get_next_autosave_number(save_dir)
        filename = f"autosave_{autosave_number}"
        file_path = os.path.join(save_dir, filename + ".sudoku")
        last_saved_filename = filename  # Сохраняем имя последнего файла
    try:
        with open(file_path, "wb") as f:
            pickle.dump(board_data, f)
        print(f"Game saved to {file_path}")
    except Exception as e:
        print(f"Error saving game: {e}")

    delete_oldest_autosave(save_dir, 10)  # Поддерживаем не более 10 файлов автосохранения
    return last_saved_filename

def get_next_autosave_number(save_dir):
    """Получает следующий номер для автосохранения."""
    existing_autosaves = [f for f in os.listdir(save_dir) if f.startswith("autosave_") and f.endswith(".sudoku")]
    numbers = [int(f[9:-7]) for f in existing_autosaves if f[9:-7].isdigit()]
    if not numbers:
        return 1
    else:
        return max(numbers) + 1

def delete_oldest_autosave(save_dir, max_saves):
    """Удаляет старые автосохранения, если их больше max_saves."""
    existing_autosaves = [f for f in os.listdir(save_dir) if f.startswith("autosave_") and f.endswith(".sudoku")]
    if len(existing_autosaves) > max_saves:
        saves = [(int(f[9:-7]), f) for f in existing_autosaves if f[9:-7].isdigit()]
        saves.sort()

        oldest_file = os.path.join(save_dir, saves[0][1])
        try:
            os.remove(oldest_file)
            print(f"Deleted oldest autosave: {oldest_file}")
        except FileNotFoundError:
            print("No autosave found!")