import unittest
from unittest.mock import patch, MagicMock
import os
import xml.etree.ElementTree as ET
import argparse
from subprocess import PIPE
from graph import (
    parse_arguments,
    find_pom,
    fetch_dependencies,
    generate_dot_code,
    save_dot_file,
    visualize_graph
)

class TestDependencyVisualizer(unittest.TestCase):

    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_arguments(self, mock_args):
        mock_args.return_value = argparse.Namespace(
            visualizer="dot",
            package="com.example:myapp",
            output="graph.png",
            repo="/path/to/repo"
        )
        args = parse_arguments()
        self.assertEqual(args.visualizer, "dot")
        self.assertEqual(args.package, "com.example:myapp")
        self.assertEqual(args.output, "graph.png")
        self.assertEqual(args.repo, "/path/to/repo")

    def test_find_pom(self):
        with patch('os.path.exists', return_value=True):
            pom_path = find_pom("/path/to/repo", "com.example", "myapp", "1.0.0")
            expected_path = "/path/to/repo/com/example/myapp/1.0.0/myapp-1.0.0.pom"
            self.assertEqual(pom_path, expected_path)

    def test_find_pom_not_found(self):
        with patch('os.path.exists', return_value=False):
            with self.assertRaises(FileNotFoundError):
                find_pom("/path/to/repo", "com.example", "myapp", "1.0.0")


    def test_generate_dot_code(self):
        dependencies = {
            "myapp": {
                "lib1": {},
                "lib2": {"lib3": {}}
            }
        }
        dot_code = generate_dot_code("myapp", dependencies)
        self.assertIn('"myapp"', dot_code)
        self.assertIn('"myapp" -> "lib1"', dot_code)
        self.assertIn('"lib2" -> "lib3"', dot_code)

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save_dot_file(self, mock_open):
        dot_code = "digraph dependencies { \"node1\" -> \"node2\"; }"
        output_path = "graph.png"
        dot_file = save_dot_file(dot_code, output_path)
        self.assertEqual(dot_file, "graph.dot")
        mock_open.assert_called_once_with("graph.dot", "w", encoding="utf-8")
        mock_open().write.assert_called_once_with(dot_code)

    @patch('subprocess.run')
    def test_visualize_graph_failure(self, mock_run):
        # Mocks subprocess.run to simulate an error
        mock_run.return_value = MagicMock(returncode=1, stderr=b"Visualization failed due to an error.")

        # Check that the exception is raised
        with self.assertRaises(RuntimeError) as context:
            visualize_graph("dot", "graph.dot", "graph.png")

        # Assert that the exception message contains expected content
        self.assertIn("Visualization failed", str(context.exception))
        self.assertIn("due to an error", str(context.exception))


if __name__ == "__main__":
    unittest.main()
