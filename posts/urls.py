from django.urls import path
from .views import home, create_job, login_user, register, about, contact, logout_user, jobs_page, profile_view

urlpatterns = [
    path('', home),
    path('create/', create_job),
    path('login/', login_user, name='login'),
    path('register/', register),

    path('about/', about),
    path('contact/', contact),

    path('jobs/', jobs_page),   # ✅ ONLY THIS (REMOVE home one)
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_user),
]