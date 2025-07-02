from django.contrib import admin
from .models import Course, Video, Enrollment, Trainer

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'serial_number', 'video_id', 'is_preview')
    list_filter = ('course', 'is_preview')
    search_fields = ('title', 'video_id')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'discount', 'active', 'date', 'length')
    list_filter = ('active', 'date', 'price')
    search_fields = ('name', 'slug', 'description')

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'date')
    list_filter = ('course', 'date')
    search_fields = ('user__username', 'course__name')
    
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('trainer_name', 'experience', 'expertise')
    search_fields = ('trainer_name', 'courses__name')
    list_filter = ('experience',)

admin.site.register(Course, CourseAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Trainer, TrainerAdmin)
