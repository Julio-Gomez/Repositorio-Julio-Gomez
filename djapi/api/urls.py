from django.urls import path
from api.apiviews import ProductoList, ProductoDatalle, CategoriaSave, SubcategoriaSave, CategoriaList, SubcategoriaList, CategoriaDetalle, SubcategoriaAdd, ProductoViewSet
from api.apiviews import UserCreate, LoginView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

router = DefaultRouter()
router.register('v2/productos', ProductoViewSet, base_name='productos')
urlpatterns = [
    path('v1/productos/', ProductoList.as_view(), name='producto_list'),
    path('v1/productos/<int:pk>', ProductoDatalle.as_view(), name='producto_detalle'),
    path('v1/categorias/', CategoriaList.as_view(), name='categoria_save'),
    path('v1/categorias/<int:pk>', CategoriaDetalle.as_view(), name='categoria_detalle'),
    path('v1/categorias/<int:pk>/subcategorias/', SubcategoriaList.as_view(), name = 'subcategoria_save'),
    path('v1/categorias/<int:cat_pk>/addsubcategorias/', SubcategoriaAdd.as_view(), name='subcategoria_apiview'),
    path('v3/usuarios/', UserCreate.as_view(), name= 'creacion_de_usuario'),
    path("v4/login/", LoginView.as_view(), name='login'),
    path("v4/login-drf/", views.obtain_auth_token, name='login_drf')
]

urlpatterns += router.urls