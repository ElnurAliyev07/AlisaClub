from django.urls import path
from .views.home.views import home, contact, about
from .views.auth.views import registration, user_login, user_logout
from .views.blog.views import blog, blog_detail, event_detail
from .views.services.views import service, service_detail
from .views.birthday.views import birthday
from .views.profile.views import profile, edit_profile, add_child, edit_child, delete_child

urlpatterns = [
    path('', home, name='home'),
    
    # Auth URL-ləri
    path('registration/', registration, name='registration'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),

    path('blog/', blog, name='blog'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
    path('event/<slug:slug>/', event_detail, name='event_detail'),
    
    path('service/', service, name='service'),
    path('service/<slug:slug>/', service_detail, name='service_detail'),

    path('birthday/', birthday, name='birthday'),
    
    # Profil URL-ləri
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/child/add/', add_child, name='add_child'),
    path('profile/child/<int:child_id>/edit/', edit_child, name='edit_child'),
    path('profile/child/<int:child_id>/delete/', delete_child, name='delete_child'),
]
