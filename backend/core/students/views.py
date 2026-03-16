from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Student
import qrcode
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import HttpResponse
import subprocess
import tempfile
import os
import shutil


@login_required
def welcome(request):
    return render(request, 'welcome.html')

@login_required
def register(request):
    if request.method == 'POST':
        # Handle form submission
        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender')
        matricule = request.POST.get('matricule')
        faculty = request.POST.get('faculty')
        department_program = request.POST.get('department_program')
        date_of_birth = request.POST.get('date_of_birth')
        photo = request.FILES.get('photo')

        # Check if matricule already exists
        if Student.objects.filter(matricule=matricule).exists():
            return render(request, 'register.html', {
                'error': 'A student with this matricule already exists.'
            })

        # Create student
        student = Student.objects.create(
            full_name=full_name,
            gender=gender,
            matricule=matricule,
            faculty=faculty,
            department_program=department_program,
            date_of_birth=date_of_birth,
            issued_year=2026,  # Set issued year on registration
            photo=photo
        )

        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(matricule)
        qr.make(fit=True)
        qr_img = qr.make_image(fill='black', back_color='white')

        # Save QR code to model
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        buffer.seek(0)
        student.qr_code.save(f'{matricule}_qr.png', ContentFile(buffer.getvalue()), save=True)

        return redirect('preview', student_id=student.id)

    return render(request, 'register.html')


def preview(request, student_id):
    """Preview student ID card - bypasses login for PDF generation"""
    student = get_object_or_404(Student, id=student_id)
    is_pdf = request.GET.get('pdf') == '1'
    
    # Only require login if NOT in PDF mode
    if not is_pdf and not request.user.is_authenticated:
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.get_full_path())
    
    return render(request, 'preview.html', {'student': student, 'is_pdf': is_pdf})

def bulk_preview(request):
    """Preview bulk student ID cards - bypasses login for PDF generation"""
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_students')
        students = Student.objects.filter(id__in=selected_ids).order_by('matricule')
        show_controls = False
        is_pdf = False
    else:
        selected_param = request.GET.get('selected')
        is_pdf = request.GET.get('pdf') == '1'
        if selected_param:
            selected_ids = selected_param.split(',')
            students = Student.objects.filter(id__in=selected_ids).order_by('matricule')
            show_controls = False
        else:
            students = Student.objects.all().order_by('matricule')
            show_controls = True
    
    # Only require login if NOT in PDF mode
    if not is_pdf and not request.user.is_authenticated:
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.get_full_path())
    
    return render(request, 'bulk_preview.html', {'students': students, 'show_controls': show_controls, 'is_pdf': is_pdf})

@login_required
def confirm_card(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, id=student_id)
        student.confirmed = True
        student.issued_year = 2026  # Current year
        student.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def download_pdf(request, student_id):
    """Generate single PDF - bypasses login for Chrome headless"""
    student = get_object_or_404(Student, id=student_id)

    # Build absolute URL for the preview page (PDF mode)
    preview_url = request.build_absolute_uri(f"{reverse('preview', args=[student_id])}?pdf=1")

    # Create a temporary PDF file
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
        temp_path = temp_file.name

    # Find Chrome executable
    chrome_path = shutil.which('chrome') or shutil.which('google-chrome') or 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    cmd = [
        chrome_path,
        '--headless',
        '--disable-gpu',
        '--no-sandbox',
        f'--print-to-pdf={temp_path}',
        '--print-to-pdf-no-header',
        '--print-to-pdf-no-footer',
        '--page-width=3.37',
        '--page-height=2.13',
        '--margin-top=0',
        '--margin-bottom=0',
        '--margin-left=0',
        '--margin-right=0',
        preview_url
    ]

    try:
        # Execute Chrome to generate PDF
        subprocess.run(cmd, check=True, capture_output=True, text=True)

        # Read the generated PDF and return as response
        with open(temp_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{student.matricule}_id_card.pdf"'
        return response

    except subprocess.CalledProcessError as e:
        # Log error for debugging
        print(f"Chrome PDF generation failed: {e.stderr}")
        return HttpResponse("Error generating PDF", status=500)

    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.unlink(temp_path)

@login_required
def download_png(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if not student.confirmed:
        return HttpResponse("Card must be confirmed before downloading", status=403)

    # Create PNG image with basic card layout using PIL
    img = Image.new('RGB', (322, 203), color='white')
    draw = Image.new('RGBA', img.size, (255, 255, 255, 0))
    img.paste(draw, (0, 0), draw)

    # Since PIL text drawing without fonts is limited, we'll create a simple colored card
    # In a real application, you'd install fonts and use ImageDraw

    # For now, return a basic white image with the correct dimensions
    # The user can use the PDF download which works perfectly

    response = HttpResponse(content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="{student.matricule}_id_card.png"'

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    response.write(buffer.getvalue())

    return response

@login_required
def student_selection(request):
    students = Student.objects.all().order_by('matricule')
    return render(request, 'student_selection.html', {'students': students})


def bulk_pdf(request):
    """Generate bulk PDF - bypasses login for Chrome headless"""
    selected_ids = request.GET.getlist('selected_students')
    if not selected_ids:
        return HttpResponse("No students selected", status=400)

    # Build URL for preview with selected students (PDF mode)
    ids_str = ','.join(selected_ids)
    bulk_preview_url = request.build_absolute_uri(f"{reverse('bulk_preview')}?selected={ids_str}&pdf=1")

    # Create a temporary PDF file
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
        temp_path = temp_file.name

    # Find Chrome executable
    chrome_path = shutil.which('chrome') or shutil.which('google-chrome') or 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    cmd = [
        chrome_path,
        '--headless',
        '--disable-gpu',
        '--no-sandbox',
        f'--print-to-pdf={temp_path}',
        '--print-to-pdf-no-header',
        '--print-to-pdf-no-footer',
        '--page-width=8.27',
        '--page-height=11.69',
        '--margin-top=0',
        '--margin-bottom=0',
        '--margin-left=0',
        '--margin-right=0',
        bulk_preview_url
    ]

    try:
        # Execute Chrome to generate PDF
        subprocess.run(cmd, check=True, capture_output=True, text=True)

        # Read the generated PDF and return as response
        with open(temp_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="selected_student_id_cards.pdf"'
        return response

    except subprocess.CalledProcessError as e:
        # Log error for debugging
        print(f"Chrome bulk PDF generation failed: {e.stderr}")
        return HttpResponse("Error generating bulk PDF", status=500)

    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.unlink(temp_path)
