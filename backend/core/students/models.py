from django.db import models


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    matricule = models.CharField(max_length=50, unique=True)
    faculty = models.CharField(max_length=255)
    department_program = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='students/')
    date_of_birth = models.DateField(blank=True, null=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    confirmed = models.BooleanField(default=False)
    issued_year = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.matricule}"


class Staff(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    job_title = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    photo = models.ImageField(upload_to='staff/')
    date_of_birth = models.DateField(blank=True, null=True)
    qr_code = models.ImageField(upload_to='staff_qrcodes/', blank=True, null=True)
    confirmed = models.BooleanField(default=False)
    issued_year = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.job_title}"

    class Meta:
        verbose_name_plural = "Staff"