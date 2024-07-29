import bpy
from bpy.types import Operator

from .data_group import get_data_container
from ..managers.api import APIManager


class UpdateCollectionsOperator(Operator):
    """ Оператор обновления содержимого """
    bl_idname = "object.update_collections"
    bl_label = "Получить коллекции"
    bl_description = "Запрос к серверу для получения списка Коллекций вашего личного кабинета"

    def execute(self, context):
        collections, errors = APIManager.get_collection_list()
        if errors:
            self.report({"ERROR"}, errors)
        items = [
            (str(item.get('id')), item.get('name'), 'test') for item in collections
        ]
        bpy.types.Scene.collections_enum = bpy.props.EnumProperty(name="Коллекция", items=items)
        return {'FINISHED'}


class CreateCollectionOperator(Operator):
    """ Кнопка открытия попапа """
    bl_idname = "object.create_collection"
    bl_label = "Создать коллекцию"
    bl_description = "Запрос к серверу для создания Коллекции вашего личного кабинета"

    def execute(self, context):
        # layout = self.layout
        # layout.operator("wm.create_collection_popup")
        bpy.ops.wm.create_collection_popup('INVOKE_DEFAULT')
        return {'FINISHED'}


class CreateCollectionPopupOperator(Operator):
    """ Всплывающее окно """
    bl_idname = "wm.create_collection_popup"
    bl_label = "Создание новой коллекции"
    bl_options = {'REGISTER', 'UNDO'}
    zarbo_collection_name: bpy.props.StringProperty(name="Название",
                                                    description="Окно создание коллекции")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def update_enum(self, context, selected_object: str):
        collections = APIManager.get_collection_list()
        items = [
            (str(item['id']), item['name'], 'test') for item in collections[0]
        ]
        bpy.types.Scene.collections_enum = bpy.props.EnumProperty(name="Коллекция",
                                                                  items=items,
                                                                  default=selected_object)

    def execute(self, context):
        collection = APIManager.create_collection(self.zarbo_collection_name)
        # Извлечение ID выбранного объекта и преобразование его в строку
        if isinstance(collection, tuple):
            selected_id = collection[0]['id']
        elif isinstance(collection, dict):
            selected_id = collection['id']
        else:
            raise Exception(f"Не смогли получить идентификатор коллекции. Результат: {collection}")
        self.update_enum(context, str(selected_id))
        return {'FINISHED'}

    def cancel(self, context):
        self.report({'INFO'}, "Окно закрыто без сохранения")
        self.zarbo_collection_name = None
        return {'CANCELLED'}

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.prop(self, 'zarbo_collection_name')
