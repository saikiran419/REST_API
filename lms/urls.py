from django.urls import path
from .views import (
    register,
    course_list, course_detail, create_course, update_course,
    enroll_course, my_courses,
    course_modules, create_module,
    module_lessons, create_lesson, lesson_detail, update_lesson
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Authentication
    path('auth/register/', register),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Courses
    path('courses/', course_list),
    path('courses/create/', create_course),
    path('courses/<int:course_id>/', course_detail),
    path('courses/<int:course_id>/update/', update_course),
    path('courses/<int:course_id>/enroll/', enroll_course),
    path('courses/my/', my_courses),

    # Modules
    path('modules/<int:course_id>/', course_modules),
    path('modules/create/', create_module),

    # Lessons
    path('lessons/<int:module_id>/', module_lessons),
    path('lessons/create/', create_lesson),
    path('lessons/<int:lesson_id>/', lesson_detail),
    path('lessons/<int:lesson_id>/update/', update_lesson),
]