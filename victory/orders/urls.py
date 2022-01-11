from django.urls import path

from . import views

app_name = 'orders'
urlpatterns = [
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('new/', views.NewOrderView.as_view(), name='new_order'),
    path('', views.IndexView.as_view(), name='index'),
]
