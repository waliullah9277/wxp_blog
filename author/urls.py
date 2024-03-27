from django.contrib import admin
from django.urls import path,include
from .import views
from wxp_programming.views import home
from posts.views import DetalisPostView
urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('login/', views.user_login, name = 'user_login'),
    # path('login/', views.UserLoginView.as_view(), name = 'user_login'),
    # path('logout/', views.user_logout, name = 'user_logout'),
    path('logout/', views.UserLogoutView.as_view(), name = 'user_logout'),
    path('profile/', views.profile, name = 'profile'),
    path('profile/edit_profile/', views.edit_profile, name = 'edit_profile'),
    path('profile/create-author-profile/', views.create_author_profile, name = 'create_author_profile'),
    path('profile/favorite_list/', views.view_favorites, name = 'favorite_list'),
    path('profile/edit/pass_change/', views.pass_change, name = 'pass_change'),
    path('category/<slug:category_slug>/',home, name='category_wise_post_profile'),
    path('details/<int:id>/', DetalisPostView.as_view(), name = 'details_post'),
    path("activate/<uid64>/<token>", views.activate, name = 'active'),
]