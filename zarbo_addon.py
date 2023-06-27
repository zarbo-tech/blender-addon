import bpy, requests, os, tempfile, uuid, subprocess
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper


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


ZARBO_API_HOST = 'https://api.zarbo.tech/'
ZARBO_API_AUTH = ZARBO_API_HOST + 'api/token/'
ZARBO_API_COLLECTIONS = ZARBO_API_HOST + 'api/v1/collections/'
ZARBO_API_PRODUCTS = ZARBO_API_HOST + 'api/v1/products/'
ZARBO_API_MODELS = ZARBO_API_HOST + 'api/v1/models/'
ZARBO_API_WIDGETS = ZARBO_API_HOST + 'api/v1/widgets/'
ZARBO_API_RENDER = ZARBO_API_WIDGETS + 'render/'

bpy.types.Scene.collections_enum = bpy.props.EnumProperty(name="Коллекция", items=[])
bpy.types.Scene.products_enum = bpy.props.EnumProperty(name="Продукт", items=[])


class ZarboManager:
    @staticmethod
    def create_model(product_id=None, file=None):
        product_id = product_id if product_id else bpy.context.scene.products_enum
        file = file if file else bpy.context.scene['zarbo_file_content']
        
        filepath = bpy.context.scene['zarbo_file_name']
        data = {'file': 'test', 'product_id': product_id,}
        _, ext = os.path.splitext(filepath)
        if ext == '.usdz':
            additional_data = 'ar_ios'
        else:
            additional_data = '3d ar_android ar_ios'
        data.update({'additional_data': additional_data})
        
        ZarboManager.reset_all_models_additional_data(product_id)

        filename = os.path.basename(bpy.context.scene['zarbo_file_name'])
        
        response = requests.post(ZARBO_API_MODELS, 
                    data=data, 
                    headers={"Authorization": bpy.context.scene['zarbo_access_token']}, 
                    files={'file': (filename, file)})
        assert response.status_code == 201, f"Ошибка: %s" % response.json().get('detail')
        
        return response.json()
    
    @staticmethod
    def get_model_list(product_id):
        response = requests.get(ZARBO_API_MODELS + '?product=' + str(product_id),
                        headers={"Authorization": bpy.context.scene['zarbo_access_token']})
        assert response.status_code == 200, f"Ошибка: %s" % response.json().get('detail')
        return response.json()['results']
    
    @staticmethod
    def reset_all_models_additional_data(product_id):
        models = ZarboManager.get_model_list(product_id)
        for model in models:
            response = requests.patch(ZARBO_API_MODELS + str(model['id']) + '/',
                        data={'additional_data': ''},
                        headers={"Authorization": bpy.context.scene['zarbo_access_token']})
            assert response.status_code == 200, f"Ошибка: %s" % response.json().get('detail')
            return response.json()


    @staticmethod
    def create_collection():
        response = requests.post(ZARBO_API_COLLECTIONS, 
                        data={'name': 'Создано из Blender'},
                        headers={"Authorization": bpy.context.scene['zarbo_access_token']})
        assert response.status_code == 201, f"Ошибка: %s" % response.json().get('detail')
        return response.json()

    @staticmethod
    def get_collection():
        response = requests.get(ZARBO_API_COLLECTIONS, 
                        headers={"Authorization": bpy.context.scene['zarbo_access_token']})
        assert response.status_code == 200, f"Ошибка: %s" % response.json().get('detail')
        return response.json()

    @staticmethod
    def create_product(collection_id):
        random_name = str(uuid.uuid4())
        response = requests.post(
                    ZARBO_API_PRODUCTS,
                    data={
                            'collection_id': collection_id, 
                            'guid': random_name,
                            'name': random_name
                        },
                    headers={
                        "Authorization": bpy.context.scene['zarbo_access_token']
                    })
        assert response.status_code == 201, f"Ошибка: %s" % response.json().get('detail')
        return response.json()

    @staticmethod
    def get_product_list(collection_key):
        url = ZARBO_API_PRODUCTS + '?limit=9999999&offset=0'
        url += '&collections=%s' % collection_key
        response = requests.get(url, headers={"Authorization": bpy.context.scene['zarbo_access_token']})
        assert response.status_code == 200, f"Ошибка: %s" % response.json().get('detail')
        return response.json().get('results')

    @staticmethod
    def get_collection_list():
        response = requests.get(ZARBO_API_COLLECTIONS, 
                            headers={"Authorization": bpy.context.scene['zarbo_access_token']})
        assert response.status_code == 200, f"Ошибка: %s" % response.json().get('detail')
        return response.json()
    
    @staticmethod
    def create_widget(product_id):
        data = {'product_id': product_id}
        data.update({'loading_type': 'auto', 'ar': True, 'ar_scale': True, 'ar_mode': 'webxr quick-look scene-viewer',
                    'camera_controls': True, 'disable_zoom': False, 'change_material': True})
        response = requests.post(ZARBO_API_WIDGETS,
                    data=data,
                    headers={"Authorization": bpy.context.scene['zarbo_access_token']})
        assert response.status_code == 201, f"Ошибка: %s" % response.json().get('detail')
        return response.json()
    
    @staticmethod
    def get_render_url(widget_id):
        return ZARBO_API_RENDER + str(widget_id)
    
    @staticmethod
    def get_widget(product_id):
        response = requests.get(ZARBO_API_WIDGETS + "?product=%s" % product_id)
        widget = response.json()
        if response.status_code != 200:
            self.report({'ERROR'}, f"Ошибка: %s" % response.json().get('detail'))
        if widget.get('results'):
            return widget.get('results')[0]
        return None
    
    @staticmethod
    def get_or_create_widget(product_id):
        widget = ZarboManager.get_widget(product_id)
        if widget:
            return widget
        return ZarboManager.create_widget(product_id)
    
    @staticmethod
    def validate_api_key():
        ZarboManager.get_collection_list()
        
    
    
class TempManager:
    dirmaker_class = tempfile.TemporaryDirectory
    dirmaker_instance = None
    _instances = {}
    
    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(TempManager, cls).__new__(cls)
        return cls._instances[cls]
    
    def __init__(self, *args, **kwargs):
        self.dirmaker_instance = self.dirmaker_class()
    
    def get_dirname(self):
        return self.dirmaker_instance.name

    def cleanup(self):
        return self.dirmaker_instance.cleanup()
    
        
# Оператор импорта файла
class FileLoaderOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "object.file_loader"
    bl_label = "Выбрать файл"

    # Определение свойств оператора
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        # Чтение содержимого выбранного файла
        with open(self.filepath, 'rb') as file:
            file_name = os.path.basename(self.filepath)
            file_content = file.read()

        # Сохранение содержимого в переменную
#        bpy.context.scene['zarbo_file_content'] = (
#            file_name, file_content
#        )
        bpy.context.scene['zarbo_file_content'] = file_content
        bpy.context.scene['zarbo_file_name'] = file_name

        return {'FINISHED'}
    
# Оператор аутентификации
class AuthOperator(Operator):
    bl_idname = "object.authenticate"
    bl_label = "Войти"

    def execute(self, context):
        bpy.context.scene['zarbo_access_token'] = 'Api-Key ' + bpy.context.scene['zarbo_user_pass']
        ZarboManager.validate_api_key()
        bpy.context.scene.show_api_key = False
        return {'FINISHED'}

# Оператор сброса API-Key
class ResetApiKeyOperator(Operator):
    bl_idname = "object.reset_api_key"
    bl_label = "Сбросить токен"

    def execute(self, context):
        bpy.context.scene['zarbo_access_token'] = None
        bpy.context.scene.show_api_key = True
        return {'FINISHED'}


# Оператор обновления содержимого
class UpdateCollectionsOperator(Operator):
    bl_idname = "object.update_collections"
    bl_label = "Обновить коллекции"

    def execute(self, context):
        access_token = bpy.context.scene['zarbo_access_token']
        collections = ZarboManager.get_collection_list()
        items = [ 
            (item.get('key'), item.get('name'), 'test') for item in collections 
        ]
        bpy.types.Scene.collections_enum = bpy.props.EnumProperty(name="Коллекция", items=items)
        return {'FINISHED'}
    
    
# Оператор обновления содержимого
class UpdateProductsOperator(Operator):
    bl_idname = "object.update_products"
    bl_label = "Обновить продукты"

    def execute(self, context):
        access_token = bpy.context.scene['zarbo_access_token']
        products = ZarboManager.get_product_list(context.scene.collections_enum)
        items = [ 
            (str(item.get('id')), item.get('name'), 'test') for item in products 
        ]
        bpy.types.Scene.products_enum = bpy.props.EnumProperty(name="Продукт", items=items)
        return {'FINISHED'}
    


# Оператор отправки файла
class SendFileOperator(Operator):
    bl_idname = "object.send_file"
    bl_label = "Отправить файл"

    def execute(self, context):
        if context.scene.select_file:
#            send_by_path = bool(bpy.context.scene.get('zarbo_file_content'))
            send_by_path = True
        else:
            send_by_path = False
                
        if not context.scene.use_manage_menu:
            collections_list = ZarboManager.get_collection()
            if collections_list:
                collection = collections_list[0]
            else:
                collection = ZarboManager.create_collection()
            product_id = ZarboManager.create_product(collection['id'])['id']
            
        else:
            product_id = bpy.context.scene.products_enum
        
        if send_by_path:
            model = ZarboManager.create_model(product_id=product_id, 
                                            file=bpy.context.scene['zarbo_file_content'])
        else:
            temp_manager = TempManager()
            filepath = os.path.join(temp_manager.get_dirname(), 'test.glb')
            bpy.context.scene['zarbo_file_name'] = filepath
            bpy.ops.export_scene.gltf(export_format='GLB', filepath=filepath)
            with open(filepath, 'rb') as f:
                model = ZarboManager.create_model(product_id, f.read())
            temp_manager.cleanup()
        assert model
        widget = ZarboManager.get_or_create_widget(product_id)
        context.scene.widget_url = ZarboManager.get_render_url(widget['id'])
        
        return {'FINISHED'}
    

# Панель управления экспортом файла в Zarbo
class LayoutDemoPanel(bpy.types.Panel):
    """ """
    bl_label = "Загрузка в Zarbo"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        
        if scene.show_api_key:
            layout.prop(context.scene, 'zarbo_user_pass')
            row = layout.row(align=True)
            row.operator("object.authenticate")
        else:
            row = layout.row(align=True)
            row.operator("object.reset_api_key")

        layout.prop(context.scene, 'select_file')
        
        if scene.select_file:
            box = layout.box()
            box.label(text="Будет отправлен загруженный файл", icon="INFO")
            box = layout.box()
            col = box.column()
            row = col.row()
            row.label(text="Файл для загрузки:")
            row.label(text=bpy.context.scene.get('zarbo_file_name'))
            row = box.row(align=True)
            row.operator("object.file_loader")
        else:
            box = layout.box()
            box.label(text="Будут отправлены выделенные объекты сцены", icon="INFO")
        
        
        
        layout.prop(context.scene, 'use_manage_menu')
        if context.scene.use_manage_menu == True:
            
            box = layout.box()
            box.label(text="Выберите коллекцию и продукт:")
            
            #row = layout.row(align=True)
            box.prop(context.scene, 'collections_enum')
            
            row = box.row(align=True)
            row.operator('object.update_collections')
            
            box.prop(context.scene, 'products_enum')
            
            row = box.row(align=True)
            row.operator('object.update_products')
            
            
        else:
            box = layout.box()
            pie = box.menu_pie()
            pie.label(text='Система сама определит новую или использует', icon="INFO")
            pie.label(text="существующую коллекцию, в которой будет ")
            pie.label(text="создан продукт")
        
        layout.separator()
        row = layout.row(align=True)
        row.operator("object.send_file")
        row.scale_y = 1.7
        
        if hasattr(scene, 'widget_url'):
            layout.prop(context.scene, 'widget_url')


def register():    
    bpy.types.Scene.zarbo_user_pass = bpy.props.StringProperty(name="Api-Key")
    bpy.utils.register_class(LayoutDemoPanel)
    bpy.utils.register_class(FileLoaderOperator)
    bpy.utils.register_class(AuthOperator)
    bpy.utils.register_class(ResetApiKeyOperator)
    bpy.utils.register_class(SendFileOperator)
    bpy.utils.register_class(UpdateCollectionsOperator)
    bpy.utils.register_class(UpdateProductsOperator)
    bpy.types.Scene.use_manage_menu = bpy.props.BoolProperty(name="Расширенные настройки", default=False)
    bpy.types.Scene.widget_url = bpy.props.StringProperty(name="Ссылка", default="")
    bpy.types.Scene.select_file = bpy.props.BoolProperty(name="Загрузить файл с диска", default=False)
    bpy.types.Scene.show_api_key = bpy.props.BoolProperty(name="Button Pressed", default=True)



def unregister():
    bpy.utils.unregister_class(LayoutDemoPanel)
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



if __name__ == "__main__":
    register()
