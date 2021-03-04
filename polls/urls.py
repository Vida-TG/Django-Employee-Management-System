from django.urls import path
from polls import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<int:id>/details/', views.details, name='details'),
    path('<int:id>/vote/', views.vote, name='vote'),
    path('<int:pk>/delete-poll/', views.DeletePoll.as_view(), name='delete_poll'),
]