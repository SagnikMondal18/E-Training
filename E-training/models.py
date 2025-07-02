from django.db import models
from django.contrib.auth.models import User

class Trainer(models.Model):
    trainer_name = models.CharField(max_length=100)
    experience = models.IntegerField(help_text="Years of experience")
    expertise = models.CharField(max_length=100, help_text="Trainer's area of expertise")
    trainer_img = models.ImageField(upload_to='trainer_images', blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True, help_text="Trainer's contact email")
    github = models.URLField(blank=True, null=True, help_text="GitHub profile link")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, help_text="Average rating out of 5")

    def __str__(self):
        return self.trainer_name

class Course(models.Model):
    name = models.CharField(max_length=50, null=False)
    slug = models.SlugField(max_length=50, null=False, unique=True)
    description = models.CharField(max_length=200, null=True)
    price = models.IntegerField(null=False)
    discount = models.IntegerField(null=False, default=0)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    resource = models.FileField(upload_to="files/resource")
    length = models.IntegerField(null=False)
    trainer = models.ForeignKey(Trainer, null=True, blank=True, on_delete=models.SET_NULL, related_name='courses')

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=100, null=False)
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    serial_number = models.IntegerField(null=False)
    video_id = models.CharField(max_length=100, null=False)
    is_preview = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.course.name}'

class Payment(models.Model):
    order_id = models.CharField(max_length=50, null=False)
    payment_id = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.name} - {self.status}"
