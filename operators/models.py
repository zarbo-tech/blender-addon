import uuid
from datetime import datetime

import bpy, os
from bpy.types import Operator

from .data_group import get_data_container
from ..managers.api import APIManager
from .file_loader import FileLoaderOperator
from ..managers.temp import TempManager


def update_visibility(self, context):
    if self.export_param == 'visible':
        bpy.ops.object.select_all(action='DESELECT')
        for obj in context.visible_objects:
            obj.select_set(True)
    elif self.export_param == 'selected':
        ...
    else:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in context.scene.objects:
            obj.select_set(True)


class UpdateModelsOperator(Operator):
    """ Оператор обновления содержимого """
    bl_idname = "object.update_models"
    bl_label = "Получить модели"
    bl_description = "Запрос к серверу для получения списка Моделей вашего личного кабинета"

    def execute(self, context):
        models, errors = APIManager.get_models(context.scene.products_enum)
        if errors:
            self.report({"ERROR"}, errors)
        items = [
            (str(item.get('id')), item.get('name'), 'test') for item in models
        ]
        bpy.types.Scene.models_enum = bpy.props.EnumProperty(name="Модель", items=items)
        return {'FINISHED'}


class CreateModelsOperator(Operator):
    """ Кнопка открытия попапа """
    bl_idname = "object.create_model"
    bl_label = "Создать модель"
    bl_description = "Запрос к серверу для создания Модели вашего личного кабинета"

    def execute(self, context):
        # layout = self.layout
        # layout.operator("wm.create_collection_popup")
        bpy.ops.wm.create_model_popup('INVOKE_DEFAULT')
        return {'FINISHED'}


class CreateModelPopupOperator(Operator):
    """ Всплывающее окно """
    bl_idname = "wm.create_model_popup"
    bl_label = "Создание новой модели"
    bl_options = {'REGISTER', 'UNDO'}
    zarbo_model_name: bpy.props.StringProperty(name="Название",
                                               description="Окно создание модели",
                                               default="Создано из Blender")
    export_param: bpy.props.EnumProperty(name="Параметры экспорта",
                                         description="Обновление модели",
                                         items=(('selected', 'Выделенные', ''),
                                                ('visible', 'Видимые', ''),
                                                ('all', 'Все', '')),
                                         update=update_visibility)

    # filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def update_enum(self, context, selected_object):
        models, errors = APIManager.get_models(context.scene.products_enum)
        items = [
            (str(item.get('id')), item.get('name'), 'test') for item in models
        ]
        bpy.types.Scene.models_enum = bpy.props.EnumProperty(name="Модель",
                                                             items=items,
                                                             default=selected_object)

    def execute(self, context):
        temp_manager = TempManager()
        filepath = os.path.join(temp_manager.get_dirname(), f'{uuid.uuid4()}.glb')
        bpy.context.scene['zarbo_file_name'] = filepath
        use_selection = False if self.export_param == 'all' else True
        bpy.ops.export_scene.gltf(export_format='GLB', filepath=filepath, use_selection=use_selection)
        with open(filepath, 'rb') as f:
            model, _ = APIManager.create_model(
                context.scene.products_enum,
                f.read(),
                f'{self.zarbo_model_name} {datetime.now().strftime("%d.%m %H:%M")}'
            )
        temp_manager.cleanup()

        self.update_enum(context, str(model['id']))
        return {'FINISHED'}

    def cancel(self, context):
        self.report({'INFO'}, "Окно закрыто без сохранения")
        self.zarbo_model_name = None
        return {'CANCELLED'}

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.prop(self, 'zarbo_model_name')
        box.prop(self, 'export_param')
        # box.prop(self, 'filepath')
        # row = box.row(align=True)
        # row.operator("object.file_loader")
        # box.operator("object.file_loader")


class UpdateModelOperator(Operator):
    """ Кнопка открытия попапа """
    bl_idname = "object.update_model"
    bl_label = "Обновить модель"
    bl_description = "Запрос к серверу для замены Модели вашего личного кабинета"

    def execute(self, context):
        # layout = self.layout
        # layout.operator("wm.create_collection_popup")
        bpy.ops.wm.update_model_popup('INVOKE_DEFAULT')
        return {'FINISHED'}


class UpdateModelPopupOperator(Operator):
    """ Всплывающее окно """
    bl_idname = "wm.update_model_popup"
    bl_label = "Обновление существующей модели"
    bl_options = {'REGISTER', 'UNDO'}
    export_param: bpy.props.EnumProperty(name="Параметры экспорта",
                                         description="Обновление модели",
                                         items=(('selected', 'Выделенные', ''),
                                                ('visible', 'Видимые', ''),
                                                ('all', 'Все', '')),
                                         update=update_visibility)

    # filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        temp_manager = TempManager()
        filename = f'{uuid.uuid4()}.glb'
        filepath = os.path.join(temp_manager.get_dirname(), filename)
        bpy.context.scene['zarbo_file_name'] = filepath
        use_selection = False if self.export_param == 'all' else True
        bpy.ops.export_scene.gltf(export_format='GLB', filepath=filepath, use_selection=use_selection)
        with open(filepath, 'rb') as f:
            model, errors = APIManager.update_model(context.scene.models_enum, f.read(), filename)
        temp_manager.cleanup()
        if errors:
            self.report({'ERROR'}, errors)

        # self.update_enum(context, str(model['id']))
        return {'FINISHED'}

    def cancel(self, context):
        self.report({'INFO'}, "Окно закрыто без сохранения")
        self.export_param = None
        return {'CANCELLED'}

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.prop(self, 'export_param')
        # box.prop(self, 'filepath')
        # row = box.row(align=True)
        # row.operator("object.file_loader")
        # box.operator("object.file_loader")
