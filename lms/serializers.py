from rest_framework import serializers
from .models import User, Course, Module, Lesson, Enrollment
from django.contrib.auth.hashers import make_password

# 1️⃣ User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

# 2️⃣ Course Serializer
class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.StringRelatedField(read_only=True)  # Show username instead of ID
    students = serializers.StringRelatedField(many=True, read_only=True)  # Optional: can show enrolled student names

    class Meta:
        model = Course
        fields = '__all__'

# 3️⃣ Module Serializer
class ModuleSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Module
        fields = '__all__'

# 4️⃣ Lesson Serializer
class LessonSerializer(serializers.ModelSerializer):
    module = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'

# 5️⃣ Enrollment Serializer (Optional unless needed in views)
class EnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Enrollment
        fields = '__all__'