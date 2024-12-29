import json
import re
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def save_glossary(glossary, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(glossary, f, ensure_ascii=False, indent=4)
    print(f"\nГлоссарий сохранен в файл {filename}.\n")

def load_glossary(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"\nФайл {filename} не найден.\n")
        return {}

def create_glossary():
    return {}

def add_term(glossary, term, definition):
    glossary[term] = definition
    print(f"\nТермин '{term}' добавлен.\n")

def remove_term(glossary, term):
    if term in glossary:
        del glossary[term]
        print(f"\nТермин '{term}' удален.\n")
    else:
        print(f"\nТермин '{term}' не найден.\n")

def find_term(glossary, term):
    definition = glossary.get(term)
    if definition:
        return definition
    else:
        print(f"\nТермин '{term}' не найден.\n")

def show_all_terms(glossary):
    if not glossary:
        print("\nГлоссарий пуст.\n")
    else:
        print("\nВсе термины и определения в глоссарии:")
        for index, (term, definition) in enumerate(glossary.items(), start=1):
            print(f"{index}. {term}: {definition}")
        print("")

def create_glossary_from_file(file_path):
    glossary = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split('. ', 1)
                if len(parts) == 2:
                    number = parts[0].strip()
                    definition = parts[1].strip()
                    glossary[number] = definition
    return glossary

def process_records(input_file_path, glossary, output_file_path):
    if not os.path.exists(input_file_path):
        print(f"\nФайл {input_file_path} не найден.\n")
        return
    if not glossary:
        print("\nГлоссарий не загружен или пуст.\n")
        return

    with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            line = line.strip()
            if line:
                name_match = re.match(r'^(.*?):', line)
                name = name_match.group(1) if name_match else None

                terms_matches = re.findall(r'п\. (\d+\.\d+\.\d+)', line)
                terms = terms_matches

                definitions = []
                missing_terms = []  # Список для отсутствующих терминов
                for term in terms:
                    if term in glossary:
                        definitions.append(glossary[term])
                    else:
                        missing_terms.append(term)

                result = f"{name} - " + "; ".join(definitions) + "."
                if missing_terms:
                    result += f" (Отсутствующие термины: {', '.join(missing_terms)})"
                outfile.write(result + "\n")

        print(f"\nРезультаты записаны в файл {output_file_path}\n")

def open_file_dialog(title="Выберите файл"):
    root = tk.Tk()
    root.withdraw()
    root.lift() 
    root.attributes("-topmost", True)
    file_path = filedialog.askopenfilename(title=title, filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    root.destroy()
    return file_path

def open_file_dialog_glossary(title="Выберите файл глоссария"):
    root = tk.Tk()
    root.withdraw()
    root.lift() 
    root.attributes("-topmost", True)  
    file_path = filedialog.askopenfilename(title=title, filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    root.destroy()
    return file_path

def save_file_dialog_result(title="Сохранить результат"):
    root = tk.Tk()
    root.withdraw() 
    root.lift() 
    root.attributes("-topmost", True) 
    file_path = filedialog.asksaveasfilename(title=title, defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    root.destroy()
    return file_path

def save_file_dialog_glossary(title="Сохранить глоссарий"):
    root = tk.Tk()
    root.withdraw() 
    root.lift() 
    root.attributes("-topmost", True) 
    file_path = filedialog.asksaveasfilename(title=title, defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    root.destroy()
    return file_path

def create_interface():
    root = tk.Tk()
    root.title("Глоссарий и Учителя")
    root.geometry("800x500")  # Увеличено для размещения элементов

    glossary = None
    input_file_path = None
    teachers_records = []
    current_record_index = -1

    def load_glossary_action():
        nonlocal glossary
        glossary_file_path = open_file_dialog_glossary("Выберите файл с глоссарием")
        if glossary_file_path:
            glossary = load_glossary(glossary_file_path)
            if glossary:
                glossary_text.delete(1.0, tk.END)  # Очищаем текстовое поле
                for term, definition in glossary.items():
                    glossary_text.insert(tk.END, f"{term}. {definition}\n")


    def save_glossary_action():
        nonlocal glossary
        glossary_file_path = save_file_dialog_glossary("Сохранить глоссарий как")
        if glossary_file_path:
            glossary_text_content = glossary_text.get(1.0, tk.END).strip()
            
            glossary_lines = glossary_text_content.splitlines()
            
            glossary = {}
            for line in glossary_lines:
                if ". " in line: 
                    term, definition = line.split(". ", 1)
                    glossary[term.strip()] = definition.strip()

            save_glossary(glossary_file_path, glossary)


    def load_teachers_file_action():
        nonlocal input_file_path, teachers_records, current_record_index
        input_file_path = open_file_dialog("Выберите файл с учителями")
        if input_file_path:
            with open(input_file_path, 'r', encoding='utf-8') as file:
                teachers_records = file.readlines()
                current_record_index = 0
                update_teacher_record_display()

    def update_teacher_record_display():
        if teachers_records:
            teacher_text.delete(1.0, tk.END)
            teacher_text.insert(tk.END, teachers_records[current_record_index].strip())
            show_glossary_definitions(teachers_records[current_record_index].strip())

    def show_glossary_definitions(record):
        definitions_text.delete(1.0, tk.END)
        if not glossary:
            messagebox.showerror("Ошибка", "Глоссарий не загружен.")
            return
        terms_matches = re.findall(r'п\. (\d+\.\d+\.\d+)', record)
        definitions = [glossary.get(term, f"Отсутствует: {term}") for term in terms_matches]
        definitions_text.insert(tk.END, "\n".join(definitions))


    def next_record():
        nonlocal current_record_index
        if teachers_records and current_record_index < len(teachers_records) - 1:
            current_record_index += 1
            update_teacher_record_display()

    def previous_record():
        nonlocal current_record_index
        if teachers_records and current_record_index > 0:
            current_record_index -= 1
            update_teacher_record_display()

    # Создание основного фрейма для размещения элементов
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Верхняя часть с кнопками
    button_frame = tk.Frame(main_frame)
    button_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    load_glossary_button = tk.Button(button_frame, text="Загрузить глоссарий", command=load_glossary_action)
    load_glossary_button.pack(side=tk.LEFT, padx=5)

    save_glossary_button = tk.Button(button_frame, text="Сохранить глоссарий", command=save_glossary_action)
    save_glossary_button.pack(side=tk.LEFT, padx=5)

    load_teachers_button = tk.Button(button_frame, text="Загрузить файл учителей", command=load_teachers_file_action)
    load_teachers_button.pack(side=tk.LEFT, padx=5)

    save_result_button = tk.Button(button_frame, text="Сохранить результат в файл", 
                               command=lambda: process_records(input_file_path, glossary, save_file_dialog_result("Сохранить результаты в файл")))
    save_result_button.pack(side=tk.LEFT, padx=5)

    # Левая часть для отображения глоссария
    left_frame = tk.Frame(main_frame)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    glossary_label = tk.Label(left_frame, text="Глоссарий")
    glossary_label.pack(anchor=tk.W)

    glossary_text = scrolledtext.ScrolledText(left_frame, width=40, height=20, wrap=tk.WORD)
    glossary_text.pack(fill=tk.BOTH, expand=True)

    # Правая часть с учителями и определениями
    right_frame = tk.Frame(main_frame)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    teacher_label = tk.Label(right_frame, text="Строка из файла учителей")
    teacher_label.pack(anchor=tk.W)

    teacher_text = tk.Text(right_frame, height=3, wrap=tk.WORD)
    teacher_text.pack(fill=tk.X)

    # Фрейм для кнопок
    navigation_frame = tk.Frame(right_frame)
    navigation_frame.pack(side=tk.TOP, pady=5)

    # Кнопка "Назад"
    prev_button = tk.Button(navigation_frame, text="Назад", command=previous_record)
    prev_button.pack(side=tk.LEFT, padx=5)

    # Кнопка "Вперед"
    next_button = tk.Button(navigation_frame, text="Вперед", command=next_record)
    next_button.pack(side=tk.LEFT, padx=5)

    definitions_label = tk.Label(right_frame, text="Определения из глоссария")
    definitions_label.pack(anchor=tk.W)

    definitions_text = scrolledtext.ScrolledText(right_frame, width=40, height=10, wrap=tk.WORD)
    definitions_text.pack(fill=tk.BOTH, expand=True)

    root.mainloop()


if __name__ == "__main__":
    create_interface()

# def main():
#     glossary = None
#     glossary_file_path = None  
#     input_file_path = None
#     output_file_path = None 
    
#     print("\nДобро пожаловать в приложение")

#     while True:
#         print("Меню приложения:\n1. Создать глоссарий из текстового файла\n2. Загрузить существующий глоссарий\n3. Сохранить глоссарий в файл\n4. Загрузить учителей\n5. Выполнить подстановку\n6. Выход")

#         try:
#             action = int(input("Выберите действие: "))
#         except ValueError:
#             print("Ошибка: введите число от 1 до 6.")
#             continue

#         if action == 1:
#             glossary_file_path = open_file_dialog("Выберите файл для создания глоссария")
#             if not os.path.exists(glossary_file_path):
#                 print(f"\nФайл {glossary_file_path} не найден.\n")
#             else:
#                 glossary = create_glossary_from_file(glossary_file_path)
#                 print("Глоссарий загружен")
        
#         elif action == 2:
#             glossary_file_path = open_file_dialog_glossary("Выберите файл с глоссарием")
#             if not os.path.exists(glossary_file_path):
#                 print(f"\nФайл {glossary_file_path} не найден.\n")
#             else:
#                 glossary = load_glossary(glossary_file_path)
            
#             if glossary:
#                 print(f"Глоссарий {glossary_file_path} загружен.")
#             else:
#                 print("Глоссарий не загружен")
        
#         elif action == 3:
#             if glossary is None:
#                 print("Ошибка: сначала создайте глоссарий или загрузите его.")
#             else:
#                 glossary_file_path = save_file_dialog_glossary("Сохранить глоссарий в файл")
#                 if glossary_file_path:
#                     save_glossary(glossary, glossary_file_path)
#                 else:
#                     print("Файл не был выбран для сохранения.")

#         elif action == 4:
#             input_file_path = open_file_dialog("Выберите файл с учителями")
#             if input_file_path:
#                 print("Файл успешно загружен.")
#             else:
#                 print("Файл не был выбран.")
        
#         elif action == 5:
#             if glossary is None or not glossary:
#                 print("Ошибка: глоссарий не загружен или пуст.")
#             elif input_file_path is None:
#                 print("Ошибка: файл с учителями не загружен.")
#             else:
#                 output_file_path = save_file_dialog_result("Сохранить результаты в файл")
#                 if output_file_path:
#                     process_records(input_file_path, glossary, output_file_path)
#                     glossary_file_path = None
#                     input_file_path = None
#                     output_file_path = None
#                     glossary = None
#                 else:
#                     print("Файл не был выбран для сохранения.")

#         elif action == 6:
#             print("Выход из программы.")
#             break
        
#         else:
#             print("Ошибка: выберите корректное действие (1-6).")







