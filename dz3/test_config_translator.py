from config_translator import ConfigTranslator 
import unittest

class TestConfigTranslator(unittest.TestCase):
    def setUp(self):
        self.translator = ConfigTranslator()

    def test_translate_json_string(self):
        input_data = '{"graph": {"nodes": 3, "edges": [{"from": 1, "to": 2}, {"from": 2, "to": 3}]}}'
        data_json = self.translator.read_json(input_data)
        translate_data = self.translator.translate(data_json)
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
}
"""
        self.assertEqual(translate_data.strip(), expected_output.strip())
    
    def test_translate_constants(self):
        input_data = '{"constants": {"a": 5, "b": 10}, "result_plus": "|+ a b|", "result_max": "|max() a b|", "result_mod": "|mod() a b|"}'
        data_json = self.translator.read_json(input_data)
        translate_data = self.translator.translate(data_json)
        expected_output = """
@{
    constants =     @{
        a = 5;
        b = 10;
    };
    result_plus = 15;
    result_max = 10;
    result_mod = 5;
}
"""
        self.assertEqual(translate_data.strip(), expected_output.strip())

    def test_invalid_constants_operator(self):
        input_data = '{"constants": {"a": 5, "b": 0}, "result": "|/ a b|"}'
        data_json = self.translator.read_json(input_data)
        
        with self.assertRaises(ValueError):
            self.translator.translate(data_json)
    
    def test_invalid_constants_json(self):
        with self.assertRaises(ValueError):
            self.translator.translate("invalid json")
    
    def test_invalid_translate(self):
        with self.assertRaises(ValueError):
            self.translator.translate(set([1,2,3,4,4]))
    
    def test_invalid_name_dict(self):
        input_data = '{"Constants": {"a": 5, "b": 0}}'
        data_json = self.translator.read_json(input_data)

        with self.assertRaises(ValueError):
            self.translator.translate(data_json)
    
    def test_invalid_json(self):
        input_data = set([1,2,3])
        with self.assertRaises(ValueError):
            self.translator.read_json(input_data)

if __name__ == "__main__":
    unittest.main()