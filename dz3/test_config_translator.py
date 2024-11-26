import unittest
from config_translator import ConfigTranslator  # Убедитесь, что импортировали ConfigTranslator

class TestConfigTranslator(unittest.TestCase):

    def setUp(self):
        """Этот метод будет выполняться перед каждым тестом"""
        # Инициализация переводчика, путь к файлам (в реальной ситуации их можно подменить)
        self.translator = ConfigTranslator(input_file="input.json", output_file="output.txt")

    def test_graph_configuration(self):
        input_data = {
            "graph": {
                "nodes": 5,
                "edges": [
                    {"from": 1, "to": 2},
                    {"from": 2, "to": 3},
                    {"from": 3, "to": 4},
                    {"from": 4, "to": 5}
                ]
            }
        }
        expected_output = """
@{
    graph =     @{
        nodes = 5;
        edges =         @{
            0 =             @{
                from = 1;
                to = 2;
            };
            1 =             @{
                from = 2;
                to = 3;
            };
            2 =             @{
                from = 3;
                to = 4;
            };
            3 =             @{
                from = 4;
                to = 5;
            };
        };
    };
}
"""
        self.assertEqual(self.translator.translate(input_data).strip(), expected_output.strip())

    def test_physics_configuration(self):
        input_data = {
            "constants": {
                "pi": 3.14159,
                "gravity": 9.8,
                "mass": 5.0
            },
            "calculations": {
                "circumference": "|+ 2 pi mass|",
                "fall_time": "|+ sqrt((2 * mass) / gravity)|"
            }
        }
        expected_output = """
@{
    constants =     @{
        pi = 3.14159;
        gravity = 9.8;
        mass = 5.0;
    };
    calculations =     @{
        circumference = "|+ 2 pi mass|";
        fall_time = "|+ sqrt((2 * mass) / gravity)|";
    };
}
"""
        self.assertEqual(self.translator.translate(input_data).strip(), expected_output.strip())

if __name__ == '__main__':
    unittest.main()
