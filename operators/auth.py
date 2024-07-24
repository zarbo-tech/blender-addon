import bpy
from bpy.types import Operator
from ..managers.api import APIManager
from ..config.addon import addon_bl_idname


class AuthOperator(Operator):
    """ Оператор аутентификации """
    bl_idname = "object.authenticate"
    bl_label = "Войти"
    bl_description = "Проверка токена"

    def execute(self, context):
        bpy.context.preferences.addons[addon_bl_idname].preferences.api_key = 'Api-Key ' + bpy.context.scene['zarbo_user_pass']
        APIManager.validate_api_key()
        bpy.context.scene.show_api_key = False
        del bpy.context.scene['zarbo_user_pass']  # TODO избавиться от хранения в сцене, передавая напрямую в prefs
        return {'FINISHED'}


