from django.urls import path

from . import views

app_name = 'orders'
urlpatterns = [
    path('<int:pk>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
    path('<int:pk>/update/', views.OrderUpdateView.as_view(), name='update'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='detail'),
    path('new/', views.OrderCreateView.as_view(), name='new_order'),
    path('', views.OrderListView.as_view(), name='index'),
]
