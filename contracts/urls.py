from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='registrations/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('create/', views.create_contract, name='create_contract'),
    path('redirect/', views.redirect_to_docusign, name='redirect_to_docusign'),
    path('docusign/callback/', views.docusign_callback, name='docusign_callback'),
    path('contracts/overview/', views.contracts_overview, name='contracts_overview'),

    path('start_signing/<int:contract_id>/', views.start_signing, name='start_signing'),

]

