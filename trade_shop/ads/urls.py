from django.urls import path
from ads import views

urlpatterns = [
    path("", views.all_ads, name="all_ads"),
    path("<int:id>/", views.current_ad, name="current_ad"),
    path("my_ads/", views.get_my_ads, name="my_ads"),
    path("create/", views.create_ad, name="create_ad"),
    path("delete/<int:id>/", views.delete_ad, name="delete_ad"),
    path("update/<int:id>/", views.update_ad, name="update_ad"),
    path("search/", views.search, name="search")
]