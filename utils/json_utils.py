import json
import os

def load_json(filepath):
    """
    Loads JSON data from a given filepath.

    Args:
        filepath (str): The path to the JSON file.

    Returns:
        dict: The loaded JSON data, or an empty dictionary if the file does not exist or an error occurs.
    """
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}. Returning empty dictionary.")
        return {}
    except IOError as e:
        print(f"Error: Could not read file {filepath}. {e}")
        return {}

def save_json(filepath, data):
    """
    Saves data to a JSON file at a given filepath.

    Args:
        filepath (str): The path to the JSON file.
        data (dict): The dictionary data to save.

    Returns:
        bool: True if the data was successfully saved, False otherwise.
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error: Could not write to file {filepath}. {e}")
        return False
