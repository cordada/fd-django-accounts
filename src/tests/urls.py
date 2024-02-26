from django.urls import include, path


urlpatterns = [
    path('', include('fd_dj_accounts.urls')),
]
