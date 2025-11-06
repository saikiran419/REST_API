from django.contrib import admin
from .models import User, Course

# 1️⃣ Register Course model with customization
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "instructor", "created_at"]

# 2️⃣ Register User model with customization
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'role']