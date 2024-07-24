import requests, bpy
from ..config.addon import addon_bl_idname


class RequestManager:

    @staticmethod
    def request(method, url, headers=None, **kwargs):
        api_key = "Api-Key " + bpy.context.preferences.addons['blender-addon'].preferences.api_key
        if not headers:
            headers = {}
        headers.update({'Authorization': api_key})
        return getattr(requests, method.lower())(url, headers=headers, **kwargs)
