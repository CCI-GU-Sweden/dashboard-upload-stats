from django.urls import path
from . import views

urlpatterns = [
    path('uploads/', views.uploads, name='uploads'),
    path('api/uploads/summary', views.uploads_summary, name='uploads_summary'),
    path('api/uploads/scopes', views.upload_scopes, name='upload_scopes'),
]
