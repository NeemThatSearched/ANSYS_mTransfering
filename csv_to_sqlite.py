import os
import pandas as pd
import sqlite3

# Укажите путь к папке csv_exports
base_dir = 'csv_exports'
ex_dir = 'ex_db'

def make_unique(column_names):
    seen = {}
    result = []
    for name in column_names:
        if name in seen:
            seen[name] += 1
            new_name = f"{name}_{seen[name]}"
        else:
            seen[name] = 0
            new_name = name
        result.append(new_name)
    return result



# Проходим по каждой папке в csv_exports
for folder_name in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder_name)
    
    # Проверяем, является ли путь директорией
    if os.path.isdir(folder_path):
        # Создаем SQLite базу данных с названием папки
        db_path = os.path.join(ex_dir, f"{folder_name}.db")
        conn = sqlite3.connect(db_path)
        
        # Проходим по каждому CSV-файлу в папке
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.csv'):
                table_name = os.path.splitext(file_name)[0]
                csv_path = os.path.join(folder_path, file_name)

                print(f"Таблица {table_name} в бд {db_path}.")
                
                try:
                    df = pd.read_csv(csv_path, encoding='utf-8', low_memory=False)
                except UnicodeDecodeError:
                    # Если UTF-8 не работает, попробуйте другую кодировку
                    df = pd.read_csv(csv_path, encoding='ISO-8859-1', low_memory=False)

                df.columns = [col.lower() for col in df.columns]
                df.columns = make_unique(df.columns)
                df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        # Закрываем соединение с базой данных
        conn.close()

print("Все данные успешно добавлены в базы данных.")
