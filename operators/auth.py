import bpy
from bpy.types import Operator
from ..managers.zarbo import ZarboManager


class AuthOperator(Operator):
    """ Оператор аутентификации """
    bl_idname = "object.authenticate"
    bl_label = "Войти"
    bl_description = "Проверка токена"

    def execute(self, context):
        bpy.context.scene['zarbo_access_token'] = 'Api-Key ' + bpy.context.scene['zarbo_user_pass']
        ZarboManager.validate_api_key()
        bpy.context.scene.show_api_key = False
        return {'FINISHED'}


