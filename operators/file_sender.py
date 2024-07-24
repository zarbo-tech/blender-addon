import bpy, os
from bpy.types import Operator
from ..managers.api import APIManager
from ..managers.temp import TempManager


class SendFileOperator(Operator):
    """ Оператор отправки файла """
    bl_idname = "object.send_file"
    bl_label = "Получить ссылку"
    bl_description = "Отправить файл в личный кабинет и получить ссылку"

    def execute_old(self, context):
        if context.scene.select_file:
            #            send_by_path = bool(bpy.context.scene.get('zarbo_file_content'))
            send_by_path = True
        else:
            send_by_path = False

        if not context.scene.use_manage_menu:
            collections_list = APIManager.get_collection()
            if collections_list:
                collection = collections_list[0]
            else:
                collection = APIManager.create_collection()
            product_id = APIManager.create_product(collection['id'])['id']

        else:
            product_id = bpy.context.scene.products_enum

        if send_by_path:
            model = APIManager.create_model(product_id=product_id,
                                              file=bpy.context.scene['zarbo_file_content'])
        else:
            temp_manager = TempManager()
            filepath = os.path.join(temp_manager.get_dirname(), 'test.glb')
            bpy.context.scene['zarbo_file_name'] = filepath
            bpy.ops.export_scene.gltf(export_format='GLB', filepath=filepath)
            with open(filepath, 'rb') as f:
                model = APIManager.create_model(product_id, f.read())
            temp_manager.cleanup()
        assert model
        widget = APIManager.get_or_create_widget(product_id)
        context.scene.widget_url = APIManager.get_render_url(widget['id'])

        return {'FINISHED'}

    def execute(self, context):
        widget, _ = APIManager.get_or_create_widget(context.scene.products_enum)
        self.report({'ERROR'}, str(widget))
        context.scene.widget_url = APIManager.get_render_url(widget['id'])
