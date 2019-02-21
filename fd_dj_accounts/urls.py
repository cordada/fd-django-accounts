from typing import List

import django.urls.resolvers
# from django.urls import path

# from . import views


app_name = 'fd_dj_accounts'

urlpatterns: List[django.urls.resolvers.CheckURLMixin] = [
    # path(
    #     "User/create/",
    #     views.UserCreateView.as_view(),
    #     name='User_create',
    # ),
    # path(
    #     "User/<int:pk>/delete/",
    #     views.UserDeleteView.as_view(),
    #     name='User_delete',
    # ),
    # path(
    #     "User/<int:pk>/",
    #     views.UserDetailView.as_view(),
    #     name='User_detail',
    # ),
    # path(
    #     "User/<int:pk>/update/",
    #     views.UserUpdateView.as_view(),
    #     name='User_update',
    # ),
    # path(
    #     "User/",
    #     views.UserListView.as_view(),
    #     name='User_list',
    # ),
]
