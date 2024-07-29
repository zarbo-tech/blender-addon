import os


class ZarboApiConfig:
    """ Пересчитывает путь до АПИ, чтобы хост можно было поменять в процессе работы аддона """

    @property
    def host(self):
        return os.environ.get('ZARBO_API_HOST', 'https://api.zarbo.tech/')

    @property
    def auth(self):
        return self.host + 'api/token/'

    @property
    def collections(self):
        return self.host + 'api/v1/collections/'

    @property
    def products(self):
        return self.host + 'api/v1/products/'

    @property
    def models(self):
        return self.host + 'api/v1/models/'

    @property
    def widgets(self):
        return self.host + 'api/v1/widgets/'

    @property
    def render(self):
        return self.widgets + 'render/'