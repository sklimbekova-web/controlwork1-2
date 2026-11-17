from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list_api_view),
    path('<int:id>/', views.post_detail_api_view),
    path('<int:id>/comments/', views.post_comments_api_view),
    path('comments/<int:id>/', views.comment_detail_api_view),
]