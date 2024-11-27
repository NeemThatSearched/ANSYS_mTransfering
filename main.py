from module_ansys import extract_materials, save_to_json

def main():
    
    # Тут вводим путь к папОЧКе и куда все записываем
    # Потом мы все переделаем в гуишное приложение, пока делаем все консолькой, чтобы не заебываться
    file_path = "MomentTest/MomentTest_files"
    output_file = "materials.json"
    
    materials = extract_materials(file_path=file_path)
    save_to_json(materials, output_file)
    

if __name__ == "__main__":
    main()