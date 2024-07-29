import bpy
from ..operators.data_group import DataContainer
import os

attrs = []

def get_addon_directory():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def update_selected_product(self, context):
    if context.scene.products_enum:
        bpy.ops.image.update_image()

def register_props():
    bpy.types.Scene.zarbo_data_container = bpy.props.CollectionProperty(type=DataContainer)
    attrs.append(bpy.types.Scene.zarbo_data_container)

    bpy.types.Scene.collections_enum = bpy.props.EnumProperty(name="Коллекция", items=[],
                                                              description="Выберите коллекцию. "
                                                                          "Если не понимаете о чем речь, "
                                                                          "то просто уберите галочку "
                                                                          "Расширенные настройки")
    attrs.append(bpy.types.Scene.collections_enum)

    bpy.types.Scene.use_manage_menu = bpy.props.BoolProperty(name="Расширенные настройки", default=False,
                                                             description="Если вы знаете куда конкретно хотите положить"
                                                                         " модель, то воспользуйтесь этими настройками")
    attrs.append(bpy.types.Scene.use_manage_menu)

    bpy.types.Scene.widget_url = bpy.props.StringProperty(name="Ссылка", default="",
                                                          description="Откройте на вашем смартфоне")
    attrs.append(bpy.types.Scene.widget_url)

    # bpy.types.Scene.select_file = bpy.props.BoolProperty(name="Загрузить файл с диска", default=False,
    #                                                      description="Если не поставить галочку, то будут отправлены "
    #                                                                  "выделенные объекты сцены")
    # attrs.append(bpy.types.Scene.select_file)

    bpy.types.Scene.show_api_key = bpy.props.BoolProperty(name="Button Pressed", default=True)
    attrs.append(bpy.types.Scene.show_api_key)

    bpy.types.Scene.products_enum = bpy.props.EnumProperty(name="Продукт", items=[],
                                                           description="Выберите продукт. "
                                                                       "Если не понимаете о чем речь, "
                                                                       "то просто уберите галочку "
                                                                       "Расширенные настройки",
                                                           update=update_selected_product)
    attrs.append(bpy.types.Scene.products_enum)

    bpy.types.Scene.zarbo_user_pass = bpy.props.StringProperty(name="Api-Key",
                                                               description="Его можно получить в личном кабинете"
                                                                           " https://zarbo.tech/")
    attrs.append(bpy.types.Scene.zarbo_user_pass)

    bpy.types.Scene.models_enum = bpy.props.EnumProperty(name="Модель", items=[],
                                                              description="Выберите модель. "
                                                                          "Если не понимаете о чем речь, "
                                                                          "то просто уберите галочку "
                                                                          "Расширенные настройки")
    attrs.append(bpy.types.Scene.models_enum)

    bpy.types.Scene.product_search = bpy.props.StringProperty(name="Поиск продукта",
                                                          description="Получение продуктов по элементу поиска",
                                                          default="")
    attrs.append(bpy.types.Scene.product_search)

    bpy.types.Scene.path_image = bpy.props.StringProperty(name="Путь до картинки",
                                                          description="Путь до превью, чтобы отобразить картинку",
                                                          default=os.path.join(get_addon_directory(), 'logo.png'))
    attrs.append(bpy.types.Scene.path_image)

    bpy.types.Scene.my_image = bpy.props.PointerProperty(type=bpy.types.Image)
    attrs.append(bpy.types.Scene.my_image)



def unregister_props():
    for attr in attrs:
        del attr

# class PropertiesCompositor:
#     def __init__(self):
#         bpy.types.Scene.zarbo_data_container = bpy.props.CollectionProperty(type=DataContainer)
#
#         bpy.types.Scene.collections_enum = bpy.props.EnumProperty(name="Коллекция", items=[],
#                                                                   description="Выберите коллекцию. "
#                                                                               "Если не понимаете о чем речь, "
#                                                                               "то просто уберите галочку "
#                                                                               "Расширенные настройки")
#
#         bpy.types.Scene.use_manage_menu = bpy.props.BoolProperty(name="Расширенные настройки", default=False,
#                                                                  description="Если вы знаете куда конкретно хотите положить"
#                                                                              " модель, то воспользуйтесь этими настройками")
#         bpy.types.Scene.widget_url = bpy.props.StringProperty(name="Ссылка", default="",
#                                                               description="Откройте на вашем смартфоне")
#         bpy.types.Scene.select_file = bpy.props.BoolProperty(name="Загрузить файл с диска", default=False,
#                                                              description="Если не поставить галочку, то будут отправлены "
#                                                                          "выделенные объекты сцены")
#         bpy.types.Scene.show_api_key = bpy.props.BoolProperty(name="Button Pressed", default=True)
#         bpy.types.Scene.products_enum = bpy.props.EnumProperty(name="Продукт", items=[],
#                                                                description="Выберите продукт. "
#                                                                            "Если не понимаете о чем речь, "
#                                                                            "то просто уберите галочку "
#                                                                            "Расширенные настройки")
#         bpy.types.Scene.zarbo_user_pass = bpy.props.StringProperty(name="Api-Key",
#                                                                    description="Его можно получить в личном кабинете"
#                                                                                " https://zarbo.tech/")
#
#
#     def register():
