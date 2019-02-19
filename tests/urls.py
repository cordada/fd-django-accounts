from django.conf.urls import url, include


urlpatterns = [
    url(r'^', include('fd_dj_accounts.urls', namespace='fd_dj_accounts')),
]
