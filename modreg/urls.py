from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

app_name ='modreg'

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('modules/', PostListView.as_view(), name = 'modules'),
    path('modules/<int:code>', PostDetailView.as_view(), name = 'module-detail'),
    path('modules/new', PostCreateView.as_view(), name = 'module-create'),
    path('modules/<int:code>/update/', PostUpdateView.as_view(), name = 'module-update'),
    path('modules/<int:code>/delete/', PostDeleteView.as_view(), name = 'module-delete'),
    path('modules/<int:code>/register/', views.toggle_module_registration, name='module-register'),
    path('my-registrations/', views.my_registrations, name='my-registrations'),
    ]

