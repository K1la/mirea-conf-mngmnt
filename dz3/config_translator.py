import argparse
import json
import re

class ConfigTranslator:
    def __init__(self, input_file=None, output_file=None):
        self.input_file = input_file
        self.output_file = output_file
        self.constants = {}
    
    def read_json(self, input_data=None):
        if isinstance(input_data, str):
            data = json.loads(input_data)
            self.constants = data.get("constants", {})
        elif self.input_file != None:
            try:
                with open(self.input_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.constants = data.get("constants", {})
            except json.JSONDecodeError as e:
                raise ValueError(f"Ошибка в JSON: {e}")
            except FileNotFoundError:
                raise ValueError(f"Файл {self.input_file} не найден.")
        else:
            raise ValueError(f'некорректный ввод файла/строки')
        return data # type = dict()
        

    def translate(self, data, indent_level=0):
        """Переводит данные в формат УКЯ с учетом уровня отступов."""
        if isinstance(data, dict):
            return self._translate_dict(data, indent_level)
        elif isinstance(data, list):
            return self._translate_list(data, indent_level)
        elif isinstance(data, int) or isinstance(data, float):
            return str(data)
        elif isinstance(data, str):
            return self._handle_expression(data) # |+ a b|
        else:
            raise ValueError(f"Некорректный тип данных: {type(data)}")

    def _handle_expression(self, value):
        """Обрабатывает строковые выражения (например, |+ a b|, |max() a b|, |mod() a b| )."""
        match = re.match(r"\|(\+|max\(\)|mod\(\))\s+(\w+)\s+(\w+)\|", value)
        if match == None:
            raise ValueError(f'Некорректный оператор в: {value}')
        operator, left, right = match.groups()
        if left in self.constants and right in self.constants:
            left_val = self.constants[left]
            right_val = self.constants[right]
            if operator == '+':
                return left_val + right_val
            elif operator == 'max()':
                return max(left_val, right_val)
            elif operator == 'mod()':
                return left_val % right_val
        

    def _translate_dict(self, dictionary, indent_level):
        """Преобразование словаря в формат УКЯ с учетом уровня отступов."""
        indent = " " * (4 * indent_level)
        nested_indent = " " * (4 * (indent_level + 1))
        result = [f"{indent}@{{"]
        for key, value in dictionary.items():
            if not re.match(r"^[_a-z]+$", key):
                raise ValueError(f"Некорректное имя: {key}")
            translated_value = self.translate(value, indent_level + 1)
            result.append(f"{nested_indent}{key} = {translated_value};")
        result.append(f"{indent}}}")
        return "\n".join(result)

    def _translate_list(self, data_list, indent_level):
        """Преобразование списка в формат УКЯ с учетом уровня отступов."""
        indent = " " * (4 * indent_level)
        nested_indent = " " * (4 * (indent_level + 1))
        result = [f"{indent}@{{"]
        for i, value in enumerate(data_list):
            translated_value = self.translate(value, indent_level + 1)
            result.append(f"{nested_indent}{i} = {translated_value};")
        result.append(f"{indent}}}")
        return "\n".join(result)

    def write_config(self, config_text):
        """Записывает конфигурацию в файл."""
        with open(self.output_file, 'w', encoding='utf-8') as file:
            file.write(config_text)

    def run(self):
        """Читает JSON, преобразует его в УКЯ и записывает результат."""
        json_data = self.read_json() # type = dict
        config_text = self.translate(json_data)
        self.write_config(config_text)


def parse_arguments():
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(description="Конвертер JSON в учебный конфигурационный язык.")
    parser.add_argument("-i", "--input", required=True, help="Путь к входному JSON-файлу.")
    parser.add_argument("-o", "--output", required=True, help="Путь к выходному файлу.")
    return parser.parse_args()

def main():
    args = parse_arguments()
    translator = ConfigTranslator(args.input, args.output)
    try:
        translator.run()
        print("Файл успешно преобразован.")
    except ValueError as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
