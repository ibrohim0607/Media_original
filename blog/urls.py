from django.urls import path
from .views import index_view, follow, like, unfollow, profile_view

urlpatterns = [
    path('', index_view),
    path('follow/', follow),
    path('unfollow/', unfollow),
    path('like/<int:pk>', like, name='like'),
    path('profile/', profile_view)
]
