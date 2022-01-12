from django.urls import path

from . import views

app_name = 'orders'
urlpatterns = [
    path('<int:pk>/comment/', views.CommentCreateView.as_view(), name='create_comment'),
    path('<int:pk>/', views.OrderUpdateView.as_view(), name='update_order'),
    path('create/', views.OrderCreateView.as_view(), name='create_order'),
    path('', views.OrderListView.as_view(), name='list_order'),
]
