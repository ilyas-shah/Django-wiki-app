import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from markdown2 import Markdown


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")

    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title, convert = True):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.

    convert: If true, returns the md_to_html converted file data
    else
    """
    markdown_to_html = Markdown()
    try:
        f = default_storage.open(f"entries/{title}.md")
        file_data = f.read().decode("utf-8")

        if convert:
            return markdown_to_html.convert(file_data)
        return file_data
    except FileNotFoundError:
        return None
def search_entries(query):
    """
    Retrieves an encyclopedia entries which match the query by characters. If no entries found, the function returns None.
    """
    entries = list_entries()
    matched_entries = []
    for entry in entries:
        if query.lower() in entry.lower():
            matched_entries.append(entry)
    return matched_entries
