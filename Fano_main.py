import os
from collections import defaultdict, deque


def display_file_selection(files):
    print("\nВыберите файл для кодирования:")
    for idx, file in enumerate(files):
        print(f"{idx + 1}: {file}")
    print("0: Выход")

def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.read()

def calculate_frequencies(text):
    frequency = defaultdict(int)
    for char in text:
        frequency[char] += 1
    return frequency

def build_fano_code(frequency):
    sorted_chars = sorted(frequency.items(), key=lambda item: item[1], reverse=True)
    codes = {char: '' for char, _ in sorted_chars}
    stack = deque([(sorted_chars, '')])
    
    while stack:
        chars, prefix = stack.popleft()
        if len(chars) <= 1:
            continue
        
        total_freq = sum(freq for _, freq in chars)
        half = total_freq / 2
        cumulative = 0
        split_index = 0

        for i, (char, freq) in enumerate(chars):
            cumulative += freq
            if cumulative >= half:
                if abs(cumulative - half) < abs((cumulative - freq) - half):
                    split_index = i + 1
                else:
                    split_index = i
                break

        left = chars[:split_index]
        right = chars[split_index:]

        for char, _ in left:
            codes[char] += prefix + '0'
        
        for char, _ in right:
            codes[char] += prefix + '1'

        stack.append((left, prefix + '0'))
        stack.append((right, prefix + '1'))
    
    return codes

def encode_with_fano(text, codes):
    return ''.join(codes[char] for char in text)

def ascii(text: str) -> str:
    return ' '.join(str(ord(char)) if ord(char) < 128 else '?' for char in text)

def main():
    test_files = ['test_file_1.txt', 'test_file_2.txt', 'test_file_3.txt', 'test_file_4.txt']
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
            forAscii = text_to_encode
            print(f"Текст для кодирования:\n{text_to_encode}\n")

            out_text = ascii(forAscii)
            print(f"Текст ASCII:\n{out_text}\n")

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
