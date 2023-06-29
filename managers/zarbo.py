import bpy, os, requests, uuid
from ..config import api_config


class ZarboManager:
    """ Набор методов взаимодействия с АПИ """
    @staticmethod
    def create_model(product_id=None, file=None):
        product_id = product_id if product_id else bpy.context.scene.products_enum
        file = file if file else bpy.context.scene['zarbo_file_content']

        filepath = bpy.context.scene['zarbo_file_name']
        data = {'file': 'test', 'product_id': product_id, }
        _, ext = os.path.splitext(filepath)
        if ext == '.usdz':
            additional_data = 'ar_ios'
        else:
            additional_data = '3d ar_android ar_ios'
        data.update({'additional_data': additional_data})

        ZarboManager.reset_all_models_additional_data(product_id)

        filename = os.path.basename(bpy.context.scene['zarbo_file_name'])

        response = requests.post(api_config.models,
                                 data=data,
                                 headers={"Authorization": bpy.context.scene['zarbo_access_token']},
                                 files={'file': (filename, file)})
        assert response.status_code == 201, f"Ошибка: %s" % response.json().get('detail')

        return response.json()

    @staticmethod
    def get_model_list(product_id):
        response = requests.get(api_config.models + '?product=' + str(product_id),
                                headers={"Authorization": bpy.context.scene['zarbo_access_token']})
        assert response.status_code == 200, f"Ошибка: %s" % response.json().get('detail')
        return response.json()['results']

    @staticmethod
    def reset_all_models_additional_data(product_id):
        models = ZarboManager.get_model_list(product_id)
        for model in models:
            response = requests.patch(api_config.models + str(model['id']) + '/',
                                      data={'additional_data': ''},
                                      headers={"Authorization": bpy.context.scene['zarbo_access_token']})
            assert response.status_code == 200, f"Ошибка: %s" % response.json().get('detail')
            return response.json()

    @staticmethod
    def create_collection():
        response = requests.post(api_config.collections,
                                 data={'name': 'Создано из Blender'},
                                 headers={"Authorization": bpy.context.scene['zarbo_access_token']})
        assert response.status_code == 201, f"Ошибка: %s" % response.json().get('detail')
        return response.json()

    @staticmethod
    def get_collection():
        response = requests.get(api_config.collections,
                                headers={"Authorization": bpy.context.scene['zarbo_access_token']})
        assert response.status_code == 200, f"Ошибка: %s" % response.json().get('detail')
        return response.json()

    @staticmethod
    def create_product(collection_id):
        random_name = str(uuid.uuid4())
        response = requests.post(
            api_config.products,
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
        url = api_config.products + '?limit=9999999&offset=0'
        url += '&collections=%s' % collection_key
        response = requests.get(url, headers={"Authorization": bpy.context.scene['zarbo_access_token']})
        assert response.status_code == 200, f"Ошибка: %s" % response.json().get('detail')
        return response.json().get('results')

    @staticmethod
    def get_collection_list():
        response = requests.get(api_config.collections,
                                headers={"Authorization": bpy.context.scene['zarbo_access_token']})
        assert response.status_code == 200, f"Ошибка: %s" % response.json().get('detail')
        return response.json()

    @staticmethod
    def create_widget(product_id):
        data = {'product_id': product_id}
        data.update({'loading_type': 'auto', 'ar': True, 'ar_scale': True, 'ar_mode': 'webxr quick-look scene-viewer',
                     'camera_controls': True, 'disable_zoom': False, 'change_material': True})
        response = requests.post(api_config.widgets,
                                 data=data,
                                 headers={"Authorization": bpy.context.scene['zarbo_access_token']})
        assert response.status_code == 201, f"Ошибка: %s" % response.json().get('detail')
        return response.json()

    @staticmethod
    def get_render_url(widget_id):
        return api_config.render + str(widget_id)

    @staticmethod
    def get_widget(product_id):
        response = requests.get(api_config.widgets + "?product=%s" % product_id)
        widget = response.json()
        assert response.status_code == 200, f"Ошибка: %s" % response.json().get('detail')
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

