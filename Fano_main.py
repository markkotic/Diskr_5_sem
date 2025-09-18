
##############################################################################################
# def generate_test_file(file_name, text_length):
#     """Генерирует тестовый файл с случайным текстом."""
#     with open(file_name, 'w', encoding='utf-8') as f:
#         text = ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=text_length))
#         f.write(text)

# def create_test_files():
#     """Создает 5 тестовых файлов с разной длиной текста."""
#     test_files = []
#     for i in range(5):
#         file_name = f'test_file_{i + 1}.txt'
#         text_length = random.randint(50, 200) 
#         generate_test_file(file_name, text_length)
#         test_files.append(file_name)
#     print("Сгенерированы следующие тестовые файлы:")
#     for file in test_files:
#         print(file)
#     return test_files
##############################################################
import os
import random
import string
from collections import defaultdict
def display_file_selection(files):
    """Отображает меню выбора файла."""
    print("\nВыберите файл для кодирования:")
    for idx, file in enumerate(files):
        print(f"{idx + 1}: {file}")
    print("0: Выход")

def read_file(file_name):
    """Читает текст из файла."""
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.read()

def calculate_frequencies(text):
    """Подсчитывает частоту символов в тексте."""
    frequency = defaultdict(int)
    for char in text:
        frequency[char] += 1
    return frequency
#############################
def build_fano_code(frequency):
    """Строит код по алгоритму Фано."""
    sorted_chars = sorted(frequency.items(), key=lambda item: item[1], reverse=True)
    codes = {char: '' for char, _ in sorted_chars}  # Инициализация кодов пустыми строками

    def fano_recursive(chars):
        nonlocal codes
        if len(chars) <= 1:
            return
        
        total_freq = sum(freq for _, freq in chars)
        half = total_freq / 2
        cumulative = 0
        split_index = 0

        # оптимальное разделение
        for i, (char, freq) in enumerate(chars):
            cumulative += freq
            if cumulative >= half:
                # Проверяем какое разделение лучше
                if abs(cumulative - half) < abs((cumulative - freq) - half):
                    split_index = i + 1
                else:
                    split_index = i
                break

        left = chars[:split_index]
        right = chars[split_index:]

       
        for char, _ in left:  # Добавляем '0' и '1' к кодам левой и правой части
            codes[char] += '0'
        
        for char, _ in right: 
            codes[char] += '1'

        
        fano_recursive(left)
        fano_recursive(right)

    fano_recursive(sorted_chars)
    return codes

def encode_with_fano(text, codes):
    """Кодирует текст с использованием кода Фано."""
    return ''.join(codes[char] for char in text)

def main():
    # Используем существующие файлы
    test_files = ['test_file_1.txt', 'test_file_2.txt', 'test_file_3.txt', 'test_file_4.txt']
    
    # Проверяем, какие файлы действительно существуют
    existing_files = [f for f in test_files if os.path.exists(f)]
    
    if not existing_files:
        print("Не найдено ни одного из файлов test_file_1.txt, test_file_2.txt, test_file_3.txt, test_file_4.txt")
        return
    
    print("Доступные файлы для кодирования:")
    for file in existing_files:
        print(file)
    
    while True:
        display_file_selection(existing_files)
        choice = input("Введите номер файла (1-4) или 0 для выхода: ")
        
        if choice == '0':
            print("Выход из программы.")
            break
        
        if choice.isdigit() and 1 <= int(choice) <= len(test_files):
            selected_file = test_files[int(choice) - 1]
            print(f"Выбранный файл: {selected_file}")
            
            text_to_encode = read_file(selected_file)
            print(f"Текст для кодирования:\n{text_to_encode}\n")
            
            frequency = calculate_frequencies(text_to_encode)
            print("Частота символов:")
            for char, freq in frequency.items():
                print(f"'{char}': {freq}")
            
            fano_codes = build_fano_code(frequency)
            print("\nКод Фано:")
            for char, code in fano_codes.items():
                print(f"'{char}': {code}")
            
            encoded_text = encode_with_fano(text_to_encode, fano_codes)
            print(f"\nЗакодированный текст:\n{encoded_text}\n")
            
        else:
            print("Некорректный ввод. Пожалуйста, выберите номер файла от 1 до 4.")

if __name__ == "__main__":
    main()