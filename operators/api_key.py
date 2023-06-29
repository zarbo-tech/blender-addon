import bpy
from bpy.types import Operator


class ResetApiKeyOperator(Operator):
    """ Оператор сброса API-Key """
    bl_idname = "object.reset_api_key"
    bl_label = "Сбросить токен"
    bl_description = "Удалить токен из окружения, показать окно для ввода нового токена"

    def execute(self, context):
        bpy.context.scene['zarbo_access_token'] = None
        bpy.context.scene.show_api_key = True
        return {'FINISHED'}