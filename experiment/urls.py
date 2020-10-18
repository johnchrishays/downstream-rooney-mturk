from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("goodbye/", views.goodbye, name="goodbye"),
    path("nomorehits/", views.nomorehits, name="nomorehits"),
    path("iteration/", views.iteration, name="iteration"),
    path("iteration/demo/", views.demo, name="demo"),
    path("iteration/submit", views.submit, name="submit"),
    path("iteration/new", views.iteration_json, name="new"),
    path("iteration/herokuSubmit", views.indep_submit, name="herokuSubmit")]
