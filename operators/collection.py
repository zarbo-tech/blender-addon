import bpy
from bpy.types import Operator
from ..managers.zarbo import ZarboManager


class UpdateCollectionsOperator(Operator):
    """ Оператор обновления содержимого """
    bl_idname = "object.update_collections"
    bl_label = "Обновить коллекции"
    bl_description = "Запрос к серверу для получения списка Коллекций вашего личного кабинета"

    def execute(self, context):
        access_token = bpy.context.scene['zarbo_access_token']
        collections = ZarboManager.get_collection_list()
        items = [
            (item.get('key'), item.get('name'), 'test') for item in collections
        ]
        bpy.types.Scene.collections_enum = bpy.props.EnumProperty(name="Коллекция", items=items)
        return {'FINISHED'}