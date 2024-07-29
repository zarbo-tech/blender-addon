from .preferences import AddonPreferences
from .data_group import DataContainer
from .general_panel import ZarboPanel
from .auth import AuthOperator
from .file_sender import SendFileOperator
# from .file_loader import FileLoaderOperator
from .api_key import ResetApiKeyOperator
from .collection import CreateCollectionOperator, CreateCollectionPopupOperator, UpdateCollectionsOperator
from .preview import LoadZarboImage, UpdateImageOperator
from .product import CreateProductOperator, CreateProductPopupOperator, UpdateProductsOperator
from .models import UpdateModelsOperator, CreateModelsOperator, CreateModelPopupOperator, UpdateModelOperator, UpdateModelPopupOperator

registered_operators = [
    AddonPreferences,
    DataContainer,
    ZarboPanel,
    # FileLoaderOperator,
    AuthOperator,
    ResetApiKeyOperator,
    SendFileOperator,
    UpdateCollectionsOperator,
    UpdateProductsOperator,
    CreateCollectionOperator,
    CreateCollectionPopupOperator,
    CreateProductPopupOperator,
    CreateProductOperator,
    UpdateModelsOperator, CreateModelsOperator, CreateModelPopupOperator,UpdateModelOperator, UpdateModelPopupOperator,
    LoadZarboImage, UpdateImageOperator,
]

registered_props = [

]
