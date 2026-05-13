import pandas as pd
import glob
import os

def merge_excel_files(input_pattern, output_file, sheet_name='Sheet1'):
    """
    Объединяет несколько Excel файлов в один.
    
    Параметры:
    - input_pattern: шаблон пути к файлам (например, 'data/*.xlsx' или 'file_*.xlsx')
    - output_file: имя выходного файла
    - sheet_name: имя листа для чтения (по умолчанию 'Sheet1')
    """
    # Получаем список файлов по шаблону
    files = glob.glob(input_pattern)
    
    if not files:
        print(f"Файлы по шаблону '{input_pattern}' не найдены.")
        return

    print(f"Найдено файлов: {len(files)}")
    
    # Читаем и объединяем данные
    dataframes = []
    for file in files:
        try:
            df = pd.read_excel(file, sheet_name=sheet_name)
            dataframes.append(df)
            print(f"Прочитан файл: {file} ({len(df)} строк)")
        except Exception as e:
            print(f"Ошибка при чтении {file}: {e}")
    
    if not dataframes:
        print("Не удалось прочитать ни одного файла.")
        return

    # Объединяем все таблицы
    merged_df = pd.concat(dataframes, ignore_index=True)
    
    # Сохраняем результат
    merged_df.to_excel(output_file, index=False, sheet_name='MergedData')
    print(f"Данные успешно сохранены в {output_file} (всего строк: {len(merged_df)})")

if __name__ == "__main__":
    # Пример использования:
    # 1. Положите исходные файлы в папку 'input_files'
    # 2. Запустите скрипт
    
    # Шаблон для поиска всех .xlsx файлов в папке input_files
    input_path = "input_files/*.xlsx"
    output_path = "merged_result.xlsx"
    
    # Создайте папку для примера, если её нет (опционально)
    if not os.path.exists("input_files"):
        os.makedirs("input_files")
        print("Папка 'input_files' создана. Поместите туда ваши Excel файлы.")
    
    merge_excel_files(input_path, output_path)
