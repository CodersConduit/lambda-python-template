import datetime
import json
import os
import shutil
import unittest
import zipfile

CCBUILD_CONFIG_PATH = "config/build_config.json"
CCBUILD_DIR = "ccbuild"


def ccbuild():
    try:
        config = parse_build_config(CCBUILD_CONFIG_PATH)
        print("Config parsed successfully:", config)

        test_root = config["ccbuild"].get("test-root")
        if test_root:
            run_tests(test_root)
            print("Tests ran successfully..")

        create_zip(config["lambda"]["name"], config["ccbuild"]["sources-root"], config["ccbuild"]["dependencies-root"])
        print("Zip file created successfully.")
    except Exception as e:
        print("Error:", e)


# Run unit tests in the test directory
def run_tests(test_dir: str):
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    if not result.wasSuccessful():
        raise Exception("Some unit tests failed.")


def reset_build_dir():
    if os.path.exists(CCBUILD_DIR):
        try:
            shutil.rmtree(CCBUILD_DIR)
        except OSError as e:
            print(f"Error: {e.strerror}")

    try:
        os.makedirs(CCBUILD_DIR)
    except OSError as e:
        print(f"Error: Unable to create directory '{CCBUILD_DIR}': {e.strerror}")


# Create zip file
def create_zip(lambda_name: str, source_root: str, dependencies_root: str):
    reset_build_dir()

    timestamp = datetime.datetime.now().strftime("%Y%h%d_%H%M_%Ss")
    with zipfile.ZipFile(f'{CCBUILD_DIR}/{lambda_name}{timestamp}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add package dependencies
        venv_site_packages = os.path.join(*dependencies_root.split('/'))
        print(venv_site_packages)
        for root, dirs, files in os.walk(venv_site_packages):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=os.path.relpath(file_path, venv_site_packages))

        # Add files from src directory
        for root, dirs, files in os.walk(source_root):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=os.path.relpath(file_path, start=source_root))


def parse_build_config(file_path: str):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"File is not a valid JSON: {file_path}")

    required_fields = ["lambda.name", "lambda.handler", "ccbuild.sources-root", "ccbuild.dependencies-root"]
    for field in required_fields:
        keys = field.split('.')
        if not is_key_present(data, keys):
            raise ValueError(f"Required field '{field}' is missing in the JSON file.")

    return data


def is_key_present(data, keys):
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return False
    return True


# Main execution
if __name__ == '__main__':
    ccbuild()
