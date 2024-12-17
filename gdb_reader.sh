#!/bin/bash

# Укажите базовый путь, где находятся папки
BASE_DIR="/Users/neem/Downloads/Granta EduPack/2024 R1/Database"

# Создайте основную директорию для CSV-файлов, если она не существует
OUTPUT_BASE_DIR="csv_exports"
mkdir -p "$OUTPUT_BASE_DIR"

# Функция для экспорта всех таблиц из data.gdb
export_tables() {
    local gdb_path="$1"
    local output_dir="$2"

    # Получение списка всех таблиц
    TABLES=$(mdb-tables -1 "$gdb_path")

    while IFS= read -r TABLE; do
        # Замените пробелы в имени файла на подчеркивания
        OUTPUT_FILE="$output_dir/${TABLE// /_}.csv"
        # Вывод команды
        echo "Выполнение команды: mdb-export \"$gdb_path\" \"$TABLE\" > \"$OUTPUT_FILE\""
        # Выполнение команды
        mdb-export "$gdb_path" "$TABLE" > "$OUTPUT_FILE"
        if [ $? -ne 0 ]; then
            echo "Ошибка: Не удалось экспортировать таблицу $TABLE."
            rm -f "$OUTPUT_FILE"
        else
            echo "Таблица $TABLE успешно экспортирована."
        fi
    done <<< "$TABLES"
}

# Рекурсивный поиск папок и проверка наличия data.gdb
find "$BASE_DIR" -type d | while read -r dir; do
    GDB_FILE="$dir/data.gdb"
    if [ -f "$GDB_FILE" ]; then
        # Извлечение имени папки
        FOLDER_NAME=$(basename "$dir")
        # Создание директории для экспорта CSV
        OUTPUT_DIR="$OUTPUT_BASE_DIR/$FOLDER_NAME"
        mkdir -p "$OUTPUT_DIR"
        # Экспорт таблиц
        export_tables "$GDB_FILE" "$OUTPUT_DIR"
    else
        echo "Файл data.gdb не найден в $dir, пропуск."
    fi
done

echo "Экспорт завершен."
