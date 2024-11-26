import subprocess
import os
import argparse
import xml.etree.ElementTree as ET
from subprocess import run, PIPE

def parse_arguments():
    parser = argparse.ArgumentParser(description="Visualize Maven package dependencies as a graph.")
    parser.add_argument("-v", "--visualizer", required=True, help="Path to the graph visualization program (e.g., dot).")
    parser.add_argument("-p", "--package", required=True, help="Name of the Maven package (artifactId).")
    parser.add_argument("-o", "--output", required=True, help="Path to save the output graph image (PNG format).")
    parser.add_argument("-r", "--repo", required=True, help="Path to the local Maven repository.")
    return parser.parse_args()

def resolve_version(group_id, artifact_id, version="1.0.0"):
    """Resolve version for dependencies (e.g., handle ${version} variables)."""
    return version  # Hardcoded version or use a default if required.

def find_pom(repo_path, group_id, artifact_id, version):
    """Find the POM file in the Maven repository."""
    group_path = os.path.join(repo_path, *group_id.split('.'))
    artifact_path = os.path.join(group_path, artifact_id, version)
    pom_file = f"{artifact_id}-{version}.pom"
    pom_path = os.path.join(artifact_path, pom_file)

    if not os.path.exists(pom_path):
        raise FileNotFoundError(f"POM file not found at {pom_path}")
    
    return pom_path

def fetch_dependencies(repo_path, group_id, artifact_id, version):
    """Fetch Maven dependencies by parsing the POM file."""
    try:
        # Resolve version if necessary
        version = resolve_version(group_id, artifact_id, version)
        pom_path = find_pom(repo_path, group_id, artifact_id, version)
        
        tree = ET.parse(pom_path)
        root = tree.getroot()
        namespace = {"mvn": "http://maven.apache.org/POM/4.0.0"}

        dependencies_element = root.find("mvn:dependencies", namespace)
        if dependencies_element is None:
            return {}

        dependencies = {}
        for dependency in dependencies_element.findall("mvn:dependency", namespace):
            dep_group_id = dependency.find("mvn:groupId", namespace)
            dep_artifact_id = dependency.find("mvn:artifactId", namespace)
            dep_version = dependency.find("mvn:version", namespace)

            if dep_group_id is None or dep_artifact_id is None or dep_version is None:
                continue

            # Recursively fetch transitive dependencies
            dependencies[dep_artifact_id.text] = fetch_dependencies(repo_path, dep_group_id.text, dep_artifact_id.text, dep_version.text)

        return dependencies
    except Exception as e:
        print(f"Error fetching dependencies for {group_id}:{artifact_id} ({version}): {e}")
        return {}

def generate_dot_code(root_package, dependencies):
    """Generate Graphviz DOT code."""
    nodes = set()
    edges = set()

    def traverse(package_name, deps):
        nodes.add(f'"{package_name}"')
        for dep_name in deps:
            edges.add(f'"{package_name}" -> "{dep_name}"')
            traverse(dep_name, deps[dep_name])

    traverse(root_package, dependencies)

    dot_code = "digraph dependencies {\n"
    dot_code += "  " + ";\n  ".join(nodes) + ";\n"
    dot_code += "  " + ";\n  ".join(edges) + ";\n"
    dot_code += "}"
    return dot_code

def save_dot_file(dot_code, output_path):
    """Save DOT code to a file."""
    dot_file = output_path.replace(".png", ".dot")
    with open(dot_file, "w", encoding="utf-8") as file:
        file.write(dot_code)
    return dot_file

def visualize_graph(visualizer: str, dot_file: str, output_file: str):
    try:
        result = subprocess.run(
            [visualizer, '-Tpng', dot_file, '-o', output_file],
            stdout=PIPE, stderr=PIPE, check=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"Visualization failed: {result.stderr.decode()}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Visualization failed: {e.stderr.decode()}")


def main():
    args = parse_arguments()

    print(f"Analyzing Maven dependencies for package: {args.package}")

    try:
        # Разделяем groupId и artifactId, если указано в формате groupId:artifactId
        if ":" in args.package:
            group_id, artifact_id = args.package.split(":")
        else:
            raise ValueError("Package name must be in the format groupId:artifactId")

        # Задаём версию пакета (можно уточнить или извлечь из другого источника)
        version = "3.12.0"

        dependencies = fetch_dependencies(args.repo, group_id, artifact_id, version)
        dot_code = generate_dot_code(args.package, dependencies)

        dot_file = save_dot_file(dot_code, args.output)
        print(f"DOT file generated: {dot_file}")

        visualize_graph(args.visualizer, dot_file, args.output)
        print("Visualization completed successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
