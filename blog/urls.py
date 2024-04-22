from django.urls import path

from .views import index_view, follow, like, profile_view, profile_settings_view, upload_view, search_view

urlpatterns = [
    path('', index_view),
    path('follow/', follow),
    path('like/', like),
    path('profile/', profile_view),
    path('settings/<int:pk>/', profile_settings_view),
    path('upload/', upload_view),
    path('search/', search_view)
]
