import zipfile
import os
import shutil
import bpy


def zip_directory(source_dir, output_filename):
    """Создает ZIP-архив из директории."""
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, relative_path)


def copy_addon(zip_path):
    """Копирует ZIP-архив аддона в папку аддонов Blender."""
    addon_dir = bpy.utils.script_paths(subdir="addons")[0]
    destination = os.path.join(addon_dir, os.path.basename(zip_path))
    shutil.copy(zip_path, destination)
    print(f"Добавлен в папку аддонов: {destination}")


def activate_addon(module_name):
    """Активирует аддон в Blender."""
    if not bpy.ops.wm.addon_enable.poll():
        print("Не удалось активировать аддон.")
        return
    bpy.ops.wm.addon_enable(module=module_name)
    print(f"Аддон '{module_name}' активирован.")


def save_api_key(api_key):
    """Сохраняет API-ключ в настройках Blender."""
    bpy.context.scene.api_key = api_key


def main():
    # Путь к директории с аддоном
    addon_dir = "/home/istomin-vs/projects/blender-addon"

    # Путь к выходному ZIP-файлу
    zip_path = "/home/istomin-vs/projects/blender-addon.zip"

    # Сохранение API-ключа (замените на ваш ключ)
    api_key = "your_api_key_here"

    # Создание ZIP-архива
    zip_directory(addon_dir, zip_path)

    # Копирование ZIP-архива в папку аддонов
    copy_addon(zip_path)

    # Активирование аддона
    module_name = "your_addon_module_name"  # Замените на имя модуля вашего аддона
    activate_addon(module_name)

    # Сохранение API-ключа в Blender
    save_api_key(api_key)

    print("Процесс завершен.")


if __name__ == "__main__":
    main()