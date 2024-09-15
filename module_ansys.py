import json
from ansys.dpf import core as dpf
from ansys.dpf.core import operators as ops

def extract_materials(file_path):
    # Создаем сервер DPF
    server = dpf.start_local_server()
    
    # Загружаем файл проекта ANSYS
    model = dpf.Model(file_path)
    
    # Получаем все материалы из модели
    materials = model.metadata.materials
    # Создаем список для хранения материалов и их свойств
    materials_list = []
    
    for material in materials:
        material_data = {
            "name": material.name,
            "properties": {}
        }
        
        # Получаем свойства материала
        for prop in material.properties:
            material_data["properties"][prop.name] = prop.value
        
        materials_list.append(material_data)
    
    return materials_list

def save_to_json(data, output_file):
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

# Из примеров документации 
# https://dpf.docs.pyansys.com/version/stable/index.html

from ansys.dpf.core import Model
from ansys.dpf.core import examples
def example():
    model = Model(examples.find_simple_bar())
    print(model)