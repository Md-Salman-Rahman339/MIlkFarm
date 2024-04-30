from django.urls import path
from .views import product_view, DetailsPost, buy_product,MyProductListView

urlpatterns = [
    path('product/', product_view, name='product_list'),
    path('myproduct/',MyProductListView.as_view(), name='my_product'),
    path('category/<slug:category_slug>/', product_view, name='category_wise_post'),
    path('details/<int:pk>/', DetailsPost.as_view(), name="details_view"),
    path('buy_product/<int:product_id>/', buy_product, name='buy_product'),
]
