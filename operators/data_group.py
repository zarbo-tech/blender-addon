import bpy


class DataContainer(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Для чего нужен")
    collection_id: bpy.props.IntProperty(name="ID коллекции")
    collection_key: bpy.props.StringProperty(name="Key коллекции")
    product_id: bpy.props.IntProperty(name="ID продукта")
    model_id: bpy.props.IntProperty(name="ID модели")


def get_data_container(name):
    def oops(self, context):
        self.layout.label(text=name)
    bpy.context.window_manager.popup_menu(oops, title="Error", icon='ERROR')

    for container in bpy.context.scene.zarbo_data_container:
        if container.name == name:
            def oops(self, context):
                self.layout.label(text=name)

            bpy.context.window_manager.popup_menu(oops, title="Найден", icon='ERROR')
            break
    else:
        def oops(self, context):
            self.layout.label(text=name)

        bpy.context.window_manager.popup_menu(oops, title="Создан", icon='ERROR')
        container = bpy.context.scene.zarbo_data_container.add()
        container.name = name
    return container
