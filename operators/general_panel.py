import bpy


class ZarboPanel(bpy.types.Panel):
    """ Панель управления экспортом файла в Zarbo """
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

            # row = layout.row(align=True)
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