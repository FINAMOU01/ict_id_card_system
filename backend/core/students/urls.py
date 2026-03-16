from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('register/', views.register, name='register'),
    path('preview/<int:student_id>/', views.preview, name='preview'),
    path('cards/preview/', views.bulk_preview, name='bulk_preview'),
    path('confirm/<int:student_id>/', views.confirm_card, name='confirm_card'),
    path('download/pdf/<int:student_id>/', views.download_pdf, name='download_pdf'),
    path('download/png/<int:student_id>/', views.download_png, name='download_png'),
    path('cards/select/', views.student_selection, name='student_selection'),
    path('cards/pdf/', views.bulk_pdf, name='bulk_pdf'),
]