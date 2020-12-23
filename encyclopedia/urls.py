from django.urls import path, re_path

from . import views
app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("encyclopedia/search", views.search_entries, name="search_entry"),
    re_path(r"^encyclopedia/(?P<action>new|edit)$", views.add_new, name="add_new"),
    path("encyclopedia/random", views.get_random_page, name="random"),
    path("encyclopedia/<str:title>", views.get_entry, name="entry"),
]

