import json
import xml.etree.ElementTree as ET

def extract_materials(file_path: str)->list:
    """
    Важно сказать, что должен существовать путь ./projectName_files/dp0/SYS/ENGD/EngineeringData.xml
    :param file_path: Путь к папке с названием нужного проекта ансиса что то на подобии "./projectName_files"
    :return: Список всех материалов с их свойствами указанными в проекте
    """
    file_path = file_path.replace('\\', '/')
    xml_path = file_path + "dp0/SYS/ENGD/EngineeringData.xml" if file_path[-1] == '/' else file_path + "/dp0/SYS/ENGD/EngineeringData.xml"
    #MomentTest/MomentTest_files/dp0/SYS/ENGD/EngineeringData.xml
    
    with open(xml_path, 'r') as f:
        xml_content = f.read()

    root = ET.fromstring(xml_content)

    # Извлечение соответствий param_id и их имен
    param_name_map = {}
    for param in root.findall('.//Metadata/ParameterDetails'):
        param_id = param.get('id')
        param_name = param.find('Name').text
        param_name_map[param_id] = param_name

    # Извлечение соответствий property_id и их имен
    property_name_map = {}
    for prop in root.findall('.//Metadata/PropertyDetails'):
        property_id = prop.get('id')
        property_name = prop.find('Name').text
        property_name_map[property_id] = property_name

    materials = []
    for material in root.findall('.//Material'):
        bulk_details = material.find('BulkDetails')
        if bulk_details is not None:
            material_name = bulk_details.find('Name').text
            properties = extract_properties(bulk_details, property_name_map, param_name_map)
            materials.append({
                "name": material_name,
                "properties": properties
            })

    return materials

def extract_properties(bulk_details, property_name_map, param_name_map) -> dict:
    """
    :param bulk_details: Элемент в котором хранится весь материал от названия до свойств
    :param property_name_map: Словарь с РеАлЬнЫмИ названиями для каждого свойства
    :param param_name_map: Словарь с рЕаЛьНыМи названиями для каждого параметра у свойства
    :return: Список свойств для нужного материала
    """
    properties = {}
    for property_data in bulk_details.findall('PropertyData'):
        property_id = property_data.get('property')
        property_real_name = property_name_map.get(property_id, property_id)
        parameters = {}
        for parameter_value in property_data.findall('ParameterValue'):
            param_id = parameter_value.get('parameter')
            data_value = parameter_value.find('Data').text
            param_real_name = param_name_map.get(param_id, param_id)
            parameters[param_real_name] = data_value
        properties[property_real_name] = parameters
    return properties


def save_to_json(data, output_file):
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)