import bpy
from bpy.types import Operator
from ..config.addon import addon_bl_idname


class ResetApiKeyOperator(Operator):
    """ Оператор сброса API-Key """
    bl_idname = "object.reset_api_key"
    bl_label = "Сбросить токен"
    bl_description = "Удалить токен из окружения, показать окно для ввода нового токена"

    def execute(self, context):
        # bpy.context.scene['zarbo_access_token'] = None
        bpy.context.preferences.addons[addon_bl_idname].preferences.api_key = None
        bpy.context.scene.show_api_key = True
        return {'FINISHED'}