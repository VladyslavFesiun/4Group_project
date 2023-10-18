import shutil
import sys
import re
from pathlib import Path

# Normalize

UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r",
               "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

TRANS = {}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()


def normalize(name):
   # Адаптуємо назву файлу, а саме заміняємо всі українські літери та символи != нижнє підкрелення
    new_name = name.translate(TRANS)
    new_name = re.sub("\W", "_", new_name)
    return new_name

#Scan

# Перелік списків файлів, який включає задані рохширення
images_files = list()
videos_files = list()
documents_files = list()
audio_files = list()
archives = list()

others = list()  # Файли без розширення та файли з невідомим розширенням
unknown = set()  # Список невідомих розширень, які ми зустріли при сортуванні
extentions = set()  # Список відомих розширень, які ми зустріли при сортуванні

EXTENSIONS_DICT = {
    'Images': ('.jpeg', '.png', '.jpg', '.svg', '.dng'),
    'Video': ('.avi', '.mp4', '.mov', '.mkv'),
    'Documents': ('.doc', '.docx', '.txt', '.xls', '.xlsx', '.djvu', '.rtf'),
    'Audio': ('.mp3', '.ogg', '.wav', '.amr'),
    'Archives': ('.zip', '.gz', '.tar'),
}

registred_extensions = {
    "Images": images_files,
    "Videos": videos_files,
    "Documents": documents_files,
    "Audio": audio_files,
    "Archives": archives,
}


def get_extensions(file_name):
    return Path(file_name).suffix


def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ("Images", "Videos", "Documets", "Audio", "Other"):
                scan(item)
            continue

        extention = get_extensions(file_name=item.name)
        list_name = None
        new_name = folder / item.name

        if not extention:
            others.append(new_name)
        else:
            for key, values in EXTENSIONS_DICT.items():
                if extention in values:
                    extentions.add(extention)
                    list_name = key

            try:
                container = registred_extensions[list_name]
                container.append(new_name)
            except KeyError:
                unknown.add(extention)
                others.append(new_name)


def handle_file(path, root_folder, dist):
    target_folder = root_folder/dist
    target_folder.mkdir(exist_ok = True)
    new_name = normalize(path.stem) + path.suffix
    path.replace(target_folder/new_name)


def handle_archive(path, root_folder, dist):
    target_folder = root_folder/dist
    target_folder.mkdir(exist_ok = True)

    normalized_name = normalize(path.stem)
    # print(normalized_name)
    new_name = normalize(path.stem) + path.suffix
    # print(new_name)

    archive_folder = root_folder/new_name

    try:
        shutil.unpack_archive(path, target_folder/normalized_name)
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def get_folder_objects(root_path):
    for folder in root_path.iterdir():
        if folder.is_dir():
            remove_empty_folders(folder)
            try:
                folder.rmdir()
            except OSError:
                pass


def sort_files():
    path = Path.cwd()
    print(f"Start in {path}")
    folder_path = Path.cwd()

    scan(folder_path)

    for file in images_files:
        handle_file(file, folder_path, "Images")

    for file in videos_files:
        handle_file(file, folder_path, "Videos")

    for file in documents_files:
        handle_file(file, folder_path, "Documents")

    for file in audio_files:
        handle_file(file, folder_path, "Audio")
    
    for file in others:
        handle_file(file, folder_path, "Others")
    
    for file in archives:
        handle_archive(file, folder_path, "Archives")

    get_folder_objects(folder_path)


if __name__ == '__main__':
    sort_files()

