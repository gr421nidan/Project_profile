from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='base'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('log_out/', views.UserLogoutView.as_view(), name='log_out'),
    path('register/', views.register, name='register'),
    path('<int:pk>/delete/', views.UserDelete.as_view(), name='delete'),
    path('<int:pk>/update/', views.UserUpdate.as_view(), name='update'),
    path('cabinet/', views.CabinetView.as_view(), name='cabinet'),
    path('polls/', views.IndexView.as_view(), name='polls'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/result_polls/', views.ResultsView.as_view(), name='result'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
