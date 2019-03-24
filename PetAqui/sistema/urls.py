from django.conf.urls import url
from django.urls import include, path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from .views import (
    index,
    cadastro,
    cadastro_novo,
    cadastro_negocio,
    cadastro_negocio_novo,
    activate,
    account_activation_sent,
    perfil,
    profile_detail,
    change_password
    
    
)

urlpatterns = [
    url(r'^index/$', index, name='sistema_index'),
    url(r'^cadastro/$', cadastro, name='sistema_cadastro'),
    url(r'perfil/$', perfil, name='sistema_perfil'),
    url(r'^cadastro-novo/$', cadastro_novo, name='sistema_cadastro_novo'),
    url(r'^cadastro-negocio/$', cadastro_negocio, name='sistema_cadastro_negocio'),
    url(r'^cadastro-negocio-novo/$', cadastro_negocio_novo, name='sistema_cadastro_negocio_novo'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^profile/(?P<username>[\w.@+-]+)/$', views.profile_detail, name='profile'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^change-photo/$', views.PhotoUpdate.as_view(), 
     name='sistema_change_photo'),
    url(r'^change-username/$', views.UserNameUpdate.as_view(), 
     name='sistema_change_username'),
    url(r'^change-email/$', views.EmailUpdate.as_view(), 
     name='sistema_change_email'),
    url(r'^change-data/$', views.DataUpdate.as_view(), 
     name='sistema_change_data'),
    url(r'^change-pet/$', views.PetUpdate.as_view(), 
     name='sistema_change_pet'),
    url(r'^change-data-negocio/$', views.DataUpdateNegocio.as_view(), 
     name='sistema_change_data_negocio'),
    url(r'^change-hora/$', views.HoraUpdateNegocio.as_view(), 
     name='sistema_change_hora'),
  
    
     
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
