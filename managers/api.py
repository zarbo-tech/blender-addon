import bpy, os, uuid
from ..config import api_config
from ..managers.request import RequestManager
from datetime import datetime

class APIManager:
    """ Набор методов взаимодействия с АПИ """
    @staticmethod
    def check_errors(response):
        errors = extra_data = None
        if response.status_code not in [200, 201]:
            data = response.json()
            if isinstance(data, dict):
                errors = data.get('detail')
                extra_data = data.get('extra_data')
            elif isinstance(data, list):
                errors = data[0].get('detail')
                extra_data = data[0].get('extra_data')
            else:
                raise Exception(data)

        if not errors:
            return None
        if errors:
            def oops(self, context):
                self.layout.label(text=errors + '\n' + str(extra_data) + '\n' + str(response.request))
            bpy.context.window_manager.popup_menu(oops, title="Error", icon='ERROR')
        return errors + '\n' + str(extra_data)


    @staticmethod
    def create_model(product_id=None, file=None, name=None):
        name = name or f'Без названия {datetime.now().strftime("%d.%m %H:%M")}'
        product_id = product_id if product_id else bpy.context.scene.products_enum
        file = file if file else bpy.context.scene['zarbo_file_content']
        filepath = bpy.context.scene['zarbo_file_name']
        filename = os.path.basename(bpy.context.scene['zarbo_file_name'])
        data = {'file': filename, 'product_id': product_id, 'name': name}
        _, ext = os.path.splitext(filepath)
        if ext == '.usdz':
            additional_data = 'ar_ios'
        else:
            additional_data = '3d ar_android ar_ios'
        data.update({'additional_data': additional_data})

        APIManager.reset_all_models_additional_data(product_id)

        response = RequestManager.request('POST', api_config.models, data=data, files={'file': (filename, file)})
        # assert response.status_code == 201, f"Ошибка: %s" % response.json().get('detail')
        errors = APIManager.check_errors(response)
        return response.json(), errors

    @staticmethod
    def get_model_list(product_id):
        response = RequestManager.request('GET', api_config.models + '?product=' + str(product_id))
        # assert response.status_code == 200, f"Ошибка: %s" % response.json().get('detail')
        errors = APIManager.check_errors(response)
        result_response = response.json()
        if isinstance(result_response, dict):
            return response.json().get('results', []), errors
        else:
            return response.json(), errors


    @staticmethod
    def reset_all_models_additional_data(product_id):
        models, _ = APIManager.get_model_list(product_id)
        for model in models:
            response = RequestManager.request('PATCH', api_config.models + str(model['id']) + '/',
                                              data={'additional_data': ''})
            # assert response.status_code == 200, f"Ошибка: %s" % response.json().get('detail')
            errors = APIManager.check_errors(response)
            return response.json(), errors

    @staticmethod
    def create_collection(name=None):
        response = RequestManager.request('POST', api_config.collections,
                                          data={'name': name or 'Создано из Blender'})
        # assert response.status_code == 201, f"Ошибка: %s" % response.json().get('detail')
        errors = APIManager.check_errors(response)
        return response.json(), errors

    @staticmethod
    def get_collection(pk=None):
        response = RequestManager.request('GET', api_config.collections + str(pk))
        # assert response.status_code == 200, f"Ошибка: %s" % response.json().get('detail')
        # return response.json()
        errors = APIManager.check_errors(response)
        return response.json(), errors

    @staticmethod
    def create_product(collection_id, name=None, guid=None):
        if name is None:
            name = "Создано из BLender: " + str(uuid.uuid4())
        if guid is None:
            guid = str(uuid.uuid4())
        response = RequestManager.request('POST', api_config.products,
                                          data={
                                              'collection_id': collection_id,
                                              'guid': guid,
                                              'name': name
                                          })
        # assert response.status_code == 201, f"Ошибка: %s" % response.json().get('detail')
        # return response.json()
        errors = APIManager.check_errors(response)
        return response.json(), errors

    @staticmethod
    def get_product(product_id: int):
        response = RequestManager.request('GET', api_config.products + "%s/" % product_id)
        errors = APIManager.check_errors(response)
        return response.json(), errors


    @staticmethod
    def get_collections():
        response = RequestManager.request('GET', api_config.collections)
        errors = APIManager.check_errors(response)
        data = response.json()
        if data[0]:
            return data[0]['id'], errors
        raise Exception(f"Отсутствуют коллекции у пользователя")


    @staticmethod
    def get_product_list(collection_key=None, collection_id=None, blender_q=None):
        if collection_id:
            response, _ = APIManager.get_collection(collection_id)
            collection_key = response['key']
        url = api_config.products + '?limit=9999999&offset=0'
        if collection_key:
            url += '&collections=%s' % collection_key
        if blender_q:
            url += '&blender_q=%s' % blender_q
        response = RequestManager.request('GET', url)
        # assert response.status_code == 200, f"Ошибка: %s" % response.json().get('detail')
        # return response.json().get('results')
        errors = APIManager.check_errors(response)
        result_response = response.json()
        if isinstance(result_response, dict):
            return response.json().get('results', []), errors
        else:
            return response.json(), errors

    @staticmethod
    def get_collection_list():
        response = RequestManager.request('GET', api_config.collections)
        # assert response.status_code == 200, f"Ошибка: %s" % response.json().get('detail')
        # return response.json()
        errors = APIManager.check_errors(response)
        return response.json(), errors

    @staticmethod
    def create_widget(product_id):
        data = {'product_id': product_id}
        data.update({'loading_type': 'auto', 'ar': True, 'ar_scale': True, 'ar_mode': 'webxr quick-look scene-viewer',
                     'camera_controls': True, 'disable_zoom': False, 'change_material': True})
        response = RequestManager.request('POST', api_config.widgets, data=data)
        # assert response.status_code == 201, f"Ошибка: %s" % response.json().get('detail')
        # return response.json()
        errors = APIManager.check_errors(response)
        return response.json(), errors

    @staticmethod
    def get_render_url(widget_id):
        return api_config.render + str(widget_id)

    @staticmethod
    def get_widget(product_id):
        response = RequestManager.request('GET', api_config.widgets + "?product=%s" % product_id)
        # widget = response.json()
        # assert response.status_code == 200, f"Ошибка: %s" % response.json().get('detail')
        errors = APIManager.check_errors(response)
        response = response.json()
        res = None
        if response.get('results'):
            res = response.get('results')[0]

        return res, errors
        # if widget.get('results'):
        #     return widget.get('results')[0]

    @staticmethod
    def get_or_create_widget(product_id):
        widget, error = APIManager.get_widget(product_id)
        if widget:
            return widget, error
        return APIManager.create_widget(product_id)

    @staticmethod
    def validate_api_key():
        APIManager.get_collection_list()


    @staticmethod
    def get_models(product_id):
        response = RequestManager.request('GET', api_config.models + "?product=%s" % product_id)
        errors = APIManager.check_errors(response)
        return response.json()['results'], errors

    @staticmethod
    def get_model(model_id):
        response = RequestManager.request('GET', api_config.models + "%s/" % model_id)
        errors = APIManager.check_errors(response)
        return response.json(), errors

    @staticmethod
    def update_model(model_id, file, name="test.glb"):
        model, _ = APIManager.get_model(model_id)
        if model and model.get("product_id"):
            APIManager.reset_all_models_additional_data(model.get("product_id"))
            response = RequestManager.request('PATCH',
                  api_config.models + str(model_id) + '/',
                  data={'file': name, "additional_data": "3d ar_android ar_ios"},
                  # headers=http_headers,
                  files={'file': (name, file)})
            errors = APIManager.check_errors(response)
            if errors:
                def oops(self, context):
                    self.layout.label(text=str(response.__dict__))

                bpy.context.window_manager.popup_menu(oops, title="Error", icon='ERROR')
            return response.json(), errors