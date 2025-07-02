from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('courses/', CourseView.as_view(), name='courses'),
    path('course_details/<int:id>/', CourseDetailView.as_view(), name='course_details'),  # Correct class-based view usage
    path('enroll/<int:course_id>/', EnrollView.as_view(), name='enroll'),
    path('verify_payment/', verify_payment, name='verify_payment'),
    path('registration/', CustomerRegistrationView.as_view(), name='customerregistration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
