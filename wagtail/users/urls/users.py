from django.urls import path

from wagtail.users.views import users

app_name = "wagtailusers_users"
urlpatterns = [
    path("", users.Index.as_view(), name="index"),
    path("results/", users.Index.as_view(results_only=True), name="index_results"),
    path("add/", users.create_user, name="add"),
    path("<str:pk>/", users.Edit.as_view(), name="edit"),
    path("<str:pk>/delete/", users.Delete.as_view(), name="delete"),
]
