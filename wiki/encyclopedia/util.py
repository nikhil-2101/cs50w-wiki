import re
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def list_entries():
    directory, file_list = default_storage.listdir("entries")
    markdown_files = [re.sub(r"\.md$", "", file) for file in file_list if file.endswith(".md")]
    return sorted(markdown_files)

def get_entry(entry_title):
    entry_path = f"entries/{entry_title}.md"
    try:
        with default_storage.open(entry_path) as entry_file:
            return entry_file.read().decode("utf-8")
    except FileNotFoundError:
        return None

def save_entry(entry_title, entry_content):
    entry_path = f"entries/{entry_title}.md"
    if default_storage.exists(entry_path):
        default_storage.delete(entry_path)
    content_file = ContentFile(entry_content.encode("utf-8"))
    default_storage.save(entry_path, content_file)
