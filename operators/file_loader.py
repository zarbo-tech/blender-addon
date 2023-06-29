import bpy, os
from bpy_extras.io_utils import ImportHelper


class FileLoaderOperator(bpy.types.Operator, ImportHelper):
    """ Оператор импорта файла """
    bl_idname = "object.file_loader"
    bl_label = "Выбрать файл"
    bl_description = "Выбрать файл с диска для последующей отправки в личный кабинет"

    # Определение свойств оператора
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        # Чтение содержимого выбранного файла
        with open(self.filepath, 'rb') as file:
            file_name = os.path.basename(self.filepath)
            file_content = file.read()

        # Сохранение содержимого в переменную
#        bpy.context.scene['zarbo_file_content'] = (
#            file_name, file_content
#        )
        bpy.context.scene['zarbo_file_content'] = file_content
        bpy.context.scene['zarbo_file_name'] = file_name

        return {'FINISHED'}