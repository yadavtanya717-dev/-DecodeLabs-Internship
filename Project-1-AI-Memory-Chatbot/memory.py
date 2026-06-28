import json
import os

MEMORY_FILE = "memory.json"


def load_memory():
    """
    Load conversation memory from JSON file.
    Returns an empty list if the file doesn't exist,
    is empty, or contains invalid JSON.
    """
    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            # Ensure memory is always a list
            if isinstance(data, list):
                return data
            else:
                return []

    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_memory(memory):
    """
    Save conversation memory safely.
    """
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4, ensure_ascii=False)


def add_message(role, content):
    """
    Add a new message to memory.
    """
    memory = load_memory()

    memory.append({
        "role": role,
        "content": content
    })

    save_memory(memory)


def get_memory():
    """
    Return the entire conversation history.
    """
    return load_memory()


def clear_memory():
    """
    Clear all saved conversation history.
    """
    save_memory([])