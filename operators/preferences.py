import bpy
from ..config.addon import addon_bl_idname


class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = 'blender-addon'

    api_key: bpy.props.StringProperty(
        name="API Key",
        description="Yours API key for access to service",
        default="<API-Key>"
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "api_key")