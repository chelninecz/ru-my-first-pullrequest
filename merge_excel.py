import pandas as pd
import glob
import os

# Конфигурация
NETWORK_PATH = r"\\10.16.130.100\WMFactory\QA_DPT"
OUTPUT_FILE = "merged_result.xlsx"
SHEET_NAME = 0  # Можно указать имя листа (например, 'Sheet1') или 0 для первого листа
FILE_PATTERN = "*.xlsx"  # Шаблон поиска файлов

def merge_excel_files(input_pattern, output_file, sheet_name=0):
    """
    Объединяет несколько Excel файлов в один.
    
    Параметры:
    - input_pattern: шаблон пути к файлам (например, '//server/share/*.xlsx')
    - output_file: имя выходного файла
    - sheet_name: имя или индекс листа для чтения
    """
    # Проверка доступности пути
    base_dir = os.path.dirname(input_pattern)
    if base_dir and not os.path.exists(base_dir):
        print(f"Ошибка: Путь '{base_dir}' недоступен.")
        print("Проверьте подключение к сети и права доступа.")
        return

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
            print(f"Прочитан файл: {os.path.basename(file)} ({len(df)} строк)")
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
    # Формируем полный путь к файлам на сетевом диске
    input_path = os.path.join(NETWORK_PATH, FILE_PATTERN)
    
    print(f"Поиск файлов по адресу: {input_path}")
    merge_excel_files(input_path, OUTPUT_FILE, sheet_name=SHEET_NAME)
