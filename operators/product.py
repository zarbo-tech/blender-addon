import uuid
import bpy
from bpy.types import Operator

from ..properties import update_selected_product
from .data_group import get_data_container
from ..managers.api import APIManager

class UpdateProductsOperator(Operator):
    """ Оператор обновления содержимого """
    bl_idname = "object.update_products"
    bl_label = "Получить продукты"
    bl_description = "Запрос к серверу для получения списка Продуктов вашего личного кабинета"

    def execute(self, context):
        # access_token = bpy.context.scene['zarbo_access_token']
        # container = get_data_container('upload')
        # key = container.collection_key = container.collection_key or context.scene.collections_enum
        products, errors = APIManager.get_product_list(
            collection_id=context.scene.collections_enum,
            blender_q=context.scene.product_search
        )
        items = [
            (str(item.get('id')), item.get('name'), 'test') for item in products
        ]
        bpy.types.Scene.products_enum = bpy.props.EnumProperty(name="Продукт", items=items,
                                                               description="Выберите продукт. "
                                                                           "Если не понимаете о чем речь, "
                                                                           "то просто уберите галочку "
                                                                           "Расширенные настройки",
                                                               update=update_selected_product)
        bpy.ops.image.update_image()
        return {'FINISHED'}

class CreateProductOperator(Operator):
    """ Кнопка открытия попапа """
    bl_idname = "object.create_product"
    bl_label = "Создать продукт"
    bl_description = "Запрос к серверу для создания Продукта"

    def execute(self, context):
        # layout = self.layout
        # layout.operator("wm.create_collection_popup")
        bpy.ops.wm.create_product_popup('INVOKE_DEFAULT')
        return {'FINISHED'}

def get_uuid():
    return str(uuid.uuid4())

class CreateProductPopupOperator(Operator):
    """Всплывающее окно с простым сообщением"""
    bl_idname = "wm.create_product_popup"
    bl_label = "Создание нового продукта"
    bl_options = {'REGISTER', 'UNDO'}
    zarbo_product_name: bpy.props.StringProperty(name="Название",
                                                 description="Окно создание коллекции",
                                                 default="Создано из Blender")
    zarbo_product_guid: bpy.props.StringProperty(name="Артикул",
                                                 description="Окно создание коллекции",
                                                 default=str(uuid.uuid4()))

    def update_enum(self, context, selected_object):
        # container = get_data_container('upload')
        # container.collection_key = context.scene.collections_enum[0]
        products, error = APIManager.get_product_list(collection_id=context.scene.collections_enum)
        if error:
            self.report({'ERROR'}, error)
        items = [
            (str(item.get('id')), item.get('name'), 'test') for item in products
        ]

        bpy.types.Scene.products_enum = bpy.props.EnumProperty(name="Продукт", items=items,
                                                               description="Выберите продукт. "
                                                                           "Если не понимаете о чем речь, "
                                                                           "то просто уберите галочку "
                                                                           "Расширенные настройки",
                                                               default=selected_object,
                                                               update=update_selected_product)

    def execute(self, context):
        # container = get_data_container('upload')
        if context.scene.collections_enum:
            collection_id = context.scene.collections_enum
        else:
            collection_id, _ = APIManager.get_collections()
        product, error = APIManager.create_product(collection_id,
                                                   name=self.zarbo_product_name,
                                                   guid=self.zarbo_product_guid
                                                   )
        # product, error = APIManager.create_product(container.collection_id)
        if error:
            self.report({'ERROR'}, error + f"\ncollection_id: {context.scene.collections_enum}")
            return {'CANCELLED'}
        # container.product_id = product['id']
        self.update_enum(context, str(product['id']))
        # return context.window_manager.invoke_props_dialog(self)
        return {'FINISHED'}

    def cancel(self, context):
        self.report({'INFO'}, "Окно закрыто без сохранения")
        context.scene.zarbo_product_name = None
        return {'CANCELLED'}

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.prop(self, 'zarbo_product_name')
        box.prop(self, 'zarbo_product_guid')

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
