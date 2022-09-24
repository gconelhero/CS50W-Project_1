from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.get_entry, name="entry"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("edit/<str:entry>", views.edit_entry, name="edit"),
    path("random_entry", views.random_entry, name="random_entry"),
]
