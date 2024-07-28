import bpy
import requests
import tempfile
import os

from ..managers.api import APIManager


def download_file(url):
    temp_dir = os.path.join(tempfile.gettempdir(), 'fixed_temp_dir')
    os.makedirs(temp_dir, exist_ok=True)

    # Определяем путь для файла с фиксированным именем
    local_filename = os.path.join(temp_dir, 'preview_product')

    # Скачиваем файл
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    # Выводим путь к скачанному файлу
    return local_filename

class LoadZarboImage(bpy.types.Operator):
    """ Оператор для загрузки изображения """
    bl_idname = "image.load_zarbo_image"
    bl_label = "Открыть превью продукта"

    def execute(self, context):
        # Загружаем изображение
        img_path = None
        if context.scene.products_enum:
            product, _ = APIManager.get_product(context.scene.products_enum)
            if product["preview"]:
                img_path = download_file(product["preview"])
        if img_path is None:
            img_path = context.scene.path_image
        if os.path.exists(img_path):
            img = bpy.data.images.load(img_path)
            context.scene.my_image = img
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, f"Image not found: {img_path}")
            return {'CANCELLED'}

class UpdateImageOperator(bpy.types.Operator):
    """ Оператор для обновления изображения по выбранному продукту """
    bl_idname = "image.update_image"
    bl_label = "Update Image"

    def execute(self, context):
        img_path = None
        product, _ = APIManager.get_product(context.scene.products_enum)
        if product["preview"]:
            img_path = download_file(product["preview"])
        if img_path is None:
            img_path = context.scene.path_image
        if os.path.exists(img_path):
            img = bpy.data.images.load(img_path)
            context.scene.my_image = img
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, f"Image not found: {img_path}")
            return {'CANCELLED'}