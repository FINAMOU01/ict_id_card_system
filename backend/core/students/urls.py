from django.urls import path
from . import views

urlpatterns = [
    # General
    path('', views.welcome, name='welcome'),

    # ── Students ──────────────────────────────────────────────────
    path('register/', views.register, name='register'),
    path('preview/<int:student_id>/', views.preview, name='preview'),
    path('cards/preview/', views.bulk_preview, name='bulk_preview'),
    path('confirm/<int:student_id>/', views.confirm_card, name='confirm_card'),
    path('download/pdf/<int:student_id>/', views.download_pdf, name='download_pdf'),
    path('download/png/<int:student_id>/', views.download_png, name='download_png'),
    path('cards/select/', views.student_selection, name='student_selection'),
    path('cards/pdf/', views.bulk_pdf, name='bulk_pdf'),

    # ── Staff ─────────────────────────────────────────────────────
    path('staff/register/', views.register_staff, name='register_staff'),
    path('staff/preview/<int:staff_id>/', views.staff_preview, name='staff_preview'),
    path('staff/cards/preview/', views.staff_bulk_preview, name='staff_bulk_preview'),
    path('staff/download/pdf/<int:staff_id>/', views.staff_download_pdf, name='staff_download_pdf'),
    path('staff/cards/select/', views.staff_selection, name='staff_selection'),
    path('staff/cards/pdf/', views.staff_bulk_pdf, name='staff_bulk_pdf'),
]