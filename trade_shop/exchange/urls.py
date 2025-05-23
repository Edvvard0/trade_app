from django.urls import path
from exchange import views

urlpatterns = [
    path("", views.get_my_proposals, name="my_proposals"),
    path("sent_me/", views.get_proposals_sent_me, name="proposals_sent_me"),
    path("<int:id>", views.get_current_proposal, name="current_proposal"),
    path("delete/<int:id>/", views.delete_proposal, name="delete_proposal"),
    path("update/<int:id>/", views.update_proposal, name="update_proposal"),
    path('accept/<int:id>/', views.accept_proposal, name='accept_proposal'),
    path('reject/<int:id>/', views.reject_proposal, name='reject_proposal'),
    path('create/', views.create_proposal, name='create_proposal'),

]
