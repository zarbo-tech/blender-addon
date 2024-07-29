import bpy

from .operators.data_group import DataContainer
# from .operators.preferences import AddonPreferences
from .operators.api_key import ResetApiKeyOperator
from .operators.auth import AuthOperator
from .operators.collection import UpdateCollectionsOperator, CreateCollectionOperator, CreateCollectionPopupOperator
from .operators.file_loader import FileLoaderOperator
from .operators.file_sender import SendFileOperator
from .operators.general_panel import ZarboPanel
from .operators.product import UpdateProductsOperator


bl_info = {
    "name": "Zarbo Addon",
    "author": "Zarbo Tech",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Механизм быстрой загрузки моделей в сервис Zarbo",
    "warning": "Нужно обязательно обзавестись API-Key",
    "doc_url": "https://zarbo.tech/",
    "category": "Upload Scene",
}


# class AddonPreferences(bpy.types.AddonPreferences):
#     bl_idname = __name__
#
#     api_key: bpy.props.StringProperty(
#         name="API Key",
#         description="Yours API key for access to service",
#         default="<KEY>"
#     )
#
#     def draw(self, context):
#         layout = self.layout
#         layout.prop(self, "api_key")

#
#
# class OBJECT_OT_my_custom_operator(bpy.types.Operator):
#     bl_idname = "object.my_custom_operator"
#     bl_label = "My Custom Operator"
#
#     def execute(self, context):
#         prefs = bpy.context.preferences.addons[__name__].preferences
#         self.report({'INFO'}, f"Custom String: {prefs.api_key}")
#         return {'FINISHED'}
#
# def menu_func(self, context):
#     self.layout.operator(OBJECT_OT_my_custom_operator.bl_idname)


def old_register():
    bpy.utils.register_class(AddonPreferences)
    # bpy.utils.register_class(OBJECT_OT_my_custom_operator)
    # bpy.types.VIEW3D_MT_object.append(menu_func)

    bpy.types.Scene.zarbo_user_pass = bpy.props.StringProperty(name="Api-Key",
                                                               description="Его можно получить в личном кабинете"
                                                                           " https://zarbo.tech/")
    # bpy.types.Scene.zarbo_collection_name = bpy.props.StringProperty(name="Название", description="Окно создание коллекции")
    bpy.types.Scene.zarbo_product_name = bpy.props.StringProperty(name="Название", description="Окно создание продукта")
    bpy.types.Scene.collections_enum = bpy.props.EnumProperty(name="Коллекция", items=[],
                                                              description="Выберите коллекцию. "
                                                                          "Если не понимаете о чем речь, "
                                                                          "то просто уберите галочку "
                                                                          "Расширенные настройки")

    bpy.utils.register_class(DataContainer)
    bpy.types.Scene.zarbo_data_container = bpy.props.CollectionProperty(type=DataContainer)
    bpy.utils.register_class(ZarboPanel)
    bpy.utils.register_class(FileLoaderOperator)
    bpy.utils.register_class(AuthOperator)
    bpy.utils.register_class(ResetApiKeyOperator)
    bpy.utils.register_class(SendFileOperator)
    bpy.utils.register_class(UpdateCollectionsOperator)
    bpy.utils.register_class(UpdateProductsOperator)
    bpy.utils.register_class(CreateCollectionOperator)
    bpy.utils.register_class(CreateCollectionPopupOperator)
    bpy.types.Scene.use_manage_menu = bpy.props.BoolProperty(name="Расширенные настройки", default=False,
                                                             description="Если вы знаете куда конкретно хотите положить"
                                                                         " модель, то воспользуйтесь этими настройками")
    bpy.types.Scene.widget_url = bpy.props.StringProperty(name="Ссылка", default="",
                                                          description="Откройте на вашем смартфоне")
    # bpy.types.Scene.select_file = bpy.props.BoolProperty(name="Загрузить файл с диска", default=False,
    #                                                      description="Если не поставить галочку, то будут отправлены "
    #                                                                  "выделенные объекты сцены")
    bpy.types.Scene.show_api_key = bpy.props.BoolProperty(name="Button Pressed", default=True)
    bpy.types.Scene.products_enum = bpy.props.EnumProperty(name="Продукт", items=[],
                                                           description="Выберите продукт. "
                                                                       "Если не понимаете о чем речь, "
                                                                       "то просто уберите галочку "
                                                                       "Расширенные настройки")


def old_unregister():
    # bpy.utils.unregister_class(AddonPreferences)
    # bpy.utils.unregister_class(OBJECT_OT_my_custom_operator)
    # bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(DataContainer)
    bpy.utils.unregister_class(ZarboPanel)
    bpy.utils.unregister_class(FileLoaderOperator)
    bpy.utils.unregister_class(AuthOperator)
    bpy.utils.unregister_class(ResetApiKeyOperator)
    bpy.utils.unregister_class(SendFileOperator)
    bpy.utils.unregister_class(UpdateCollectionsOperator)
    bpy.utils.unregister_class(UpdateProductsOperator)
    bpy.utils.unregister_class(CreateCollectionOperator)
    bpy.utils.unregister_class(CreateCollectionPopupOperator)
    del bpy.types.Scene.use_manage_menu
    del bpy.types.Scene.widget_url
    # del bpy.types.Scene.select_file
    del bpy.types.Scene.show_api_key
    del bpy.types.Scene.collections_enum
    del bpy.types.Scene.products_enum


from .operators import registered_operators
from .properties import register_props, unregister_props

def register():
    [bpy.utils.register_class(cl) for cl in registered_operators]
    register_props()

def unregister():
    [bpy.utils.unregister_class(cl) for cl in registered_operators]
    unregister_props()


if __name__ == "__main__":
    register()
