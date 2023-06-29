import bpy
from bpy.types import Operator
from ..managers.zarbo import ZarboManager


class UpdateProductsOperator(Operator):
    """ Оператор обновления содержимого """
    bl_idname = "object.update_products"
    bl_label = "Обновить продукты"
    bl_description = "Запрос к серверу для получения списка Продуктов вашего личного кабинета"

    def execute(self, context):
        # access_token = bpy.context.scene['zarbo_access_token']
        products = ZarboManager.get_product_list(context.scene.collections_enum)
        items = [
            (str(item.get('id')), item.get('name'), 'test') for item in products
        ]
        bpy.types.Scene.products_enum = bpy.props.EnumProperty(name="Продукт", items=items)
        return {'FINISHED'}