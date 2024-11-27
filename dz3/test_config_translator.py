import json
import re

class ConfigTranslator:
    def __init__(self, input_file=None, output_file=None):
        self.input_file = input_file
        self.output_file = output_file

    def translate(self, input_data):
        if isinstance(input_data, str):
            try:
                input_data = json.loads(input_data)
            except json.JSONDecodeError as e:
                raise ValueError("Invalid JSON string") from e

        constants = input_data.get("constants", {})

        def evaluate_expression(expr):
            """Evaluates expressions like |+ a b| using constants."""
            match = re.match(r"\|([+\-*/])\s+(\w+)\s+(\w+)\|", expr)
            if match:
                operator, left, right = match.groups()
                if left in constants and right in constants:
                    left_val = constants[left]
                    right_val = constants[right]
                    if operator == '+':
                        return left_val + right_val
                    elif operator == '-':
                        return left_val - right_val
                    elif operator == '*':
                        return left_val * right_val
                    elif operator == '/':
                        if right_val == 0:
                            raise ValueError("Division by zero")
                        return left_val / right_val
            return expr  # Return unchanged if not an expression

        def process_dict(d, indent):
            """Recursively processes the dictionary to translate into config format."""
            indent_str = " " * indent
            result = f"{indent_str}@{{\n"
            for key, value in d.items():
                result += f"{indent_str}    {key} = "
                if isinstance(value, dict):
                    result += process_dict(value, indent + 4) #.strip() + ";\n"
                elif isinstance(value, list):
                    result += f"        @{{\n"
                    for i, item in enumerate(value):
                        result += f"{' ' * (indent + 8)}{i} =             {process_dict(item, indent + 8).strip()}\n"
                    result += f"{indent_str}    }};\n"
                elif isinstance(value, (int, float)):
                    result += f"{value};\n" 
                elif isinstance(value, str):
                    result += f"{evaluate_expression(value)};\n" 
                else:
                    result += "null;\n"
            result += f"{indent_str}}};\n"
            return result

        output = process_dict(input_data, 0).strip()
        if self.output_file:
            with open(self.output_file, "w") as f:
                f.write(output)
        return output


# Тесты
import unittest

class TestConfigTranslator(unittest.TestCase):

    def setUp(self):
        self.translator = ConfigTranslator()

    def test_translate_json_string(self):
        input_json = '{"graph": {"nodes": 3, "edges": [{"from": 1, "to": 2}, {"from": 2, "to": 3}]}}'
        expected_output = """
@{
    graph =     @{
        nodes = 3;
        edges =         @{
            0 =             @{
                from = 1;
                to = 2;
            };
            1 =             @{
                from = 2;
                to = 3;
            };
        };
    };
};
"""
        self.assertEqual(self.translator.translate(input_json).strip(), expected_output.strip())

    def test_translate_with_constants_and_expressions(self):
        input_data = '{"constants": {"a": 5, "b": 10}, "result": "|+ a b|"}'
        expected_output = """
@{
    constants =     @{
        a = 5;
        b = 10;
    };
    result = 15;
};
"""
        self.assertEqual(self.translator.translate(input_data).strip(), expected_output.strip())

    def test_invalid_json(self):
        with self.assertRaises(ValueError):
            self.translator.translate("invalid json")

    def test_division_by_zero(self):
        input_data = '{"constants": {"a": 5, "b": 0}, "result": "|/ a b|"}'
        with self.assertRaises(ValueError):
            self.translator.translate(input_data)

if __name__ == "__main__":
    unittest.main()
