import bpy
from .operators.api_key import ResetApiKeyOperator
from .operators.auth import AuthOperator
from .operators.collection import UpdateCollectionsOperator
from .operators.file_loader import FileLoaderOperator
from .operators.file_sender import SendFileOperator
from .operators.general_panel import ZarboPanel
from .operators.product import UpdateProductsOperator


bl_info = {
    "name": "Zarbo Addon",
    "author": "Zarbo Tech",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Механизм быстрой загрузки моделей в сервис Zarbo",
    "warning": "Нужно обязательно обзавестись API-Key",
    "doc_url": "https://zarbo.tech/",
    "category": "Upload Scene",
}


def register():    
    bpy.types.Scene.zarbo_user_pass = bpy.props.StringProperty(name="Api-Key",
                                                               description="Его можно получить в личном кабинете"
                                                                           " https://zarbo.tech/")
    bpy.utils.register_class(ZarboPanel)
    bpy.utils.register_class(FileLoaderOperator)
    bpy.utils.register_class(AuthOperator)
    bpy.utils.register_class(ResetApiKeyOperator)
    bpy.utils.register_class(SendFileOperator)
    bpy.utils.register_class(UpdateCollectionsOperator)
    bpy.utils.register_class(UpdateProductsOperator)
    bpy.types.Scene.use_manage_menu = bpy.props.BoolProperty(name="Расширенные настройки", default=False,
                                                             description="Если вы знаете куда конкретно хотите положить"
                                                                         " модель, то воспользуйтесь этими настройками")
    bpy.types.Scene.widget_url = bpy.props.StringProperty(name="Ссылка", default="",
                                                          description="Откройте на вашем смартфоне")
    bpy.types.Scene.select_file = bpy.props.BoolProperty(name="Загрузить файл с диска", default=False,
                                                         description="Если не поставить галочку, то будут отправлены "
                                                                     "выделенные объекты сцены")
    bpy.types.Scene.show_api_key = bpy.props.BoolProperty(name="Button Pressed", default=True)
    bpy.types.Scene.collections_enum = bpy.props.EnumProperty(name="Коллекция", items=[],
                                                              description="Выберите коллекцию. "
                                                                          "Если не понимаете о чем речь, "
                                                                          "то просто уберите галочку "
                                                                          "Расширенные настройки")
    bpy.types.Scene.products_enum = bpy.props.EnumProperty(name="Продукт", items=[],
                                                           description="Выберите продукт. "
                                                                       "Если не понимаете о чем речь, "
                                                                       "то просто уберите галочку "
                                                                       "Расширенные настройки")


def unregister():
    bpy.utils.unregister_class(ZarboPanel)
    bpy.utils.unregister_class(FileLoaderOperator)
    bpy.utils.unregister_class(AuthOperator)
    bpy.utils.unregister_class(ResetApiKeyOperator)
    bpy.utils.unregister_class(SendFileOperator)
    bpy.utils.unregister_class(UpdateCollectionsOperator)
    bpy.utils.unregister_class(UpdateProductsOperator)
    del bpy.types.Scene.use_manage_menu
    del bpy.types.Scene.widget_url
    del bpy.types.Scene.select_file
    del bpy.types.Scene.show_api_key
    del bpy.types.Scene.collections_enum
    del bpy.types.Scene.products_enum


if __name__ == "__main__":
    register()
