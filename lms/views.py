from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import User, Course, Module, Lesson
from .serializers import UserSerializer, CourseSerializer, ModuleSerializer, LessonSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "message": "User registered successfully"
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_list(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_detail(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_course(request):
    if request.user.role != 'instructor':
        return Response({"error": "Only instructors can create courses."}, status=status.HTTP_403_FORBIDDEN)

    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(instructor=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.user != course.instructor:
        return Response({"error": "You can only update your own courses."}, status=status.HTTP_403_FORBIDDEN)

    serializer = CourseSerializer(course, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enroll_course(request, course_id):
    if request.user.role != 'student':
        return Response({"error": "Only students can enroll."}, status=status.HTTP_403_FORBIDDEN)

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.user in course.students.all():
        return Response({"message": "Already enrolled in this course."}, status=status.HTTP_200_OK)

    course.students.add(request.user)
    return Response({"message": f"Enrolled in {course.title}."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_courses(request):
    if request.user.role == 'student':
        courses = Course.objects.filter(students=request.user)
    else:
        courses = Course.objects.filter(instructor=request.user)

    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_modules(request, course_id):
    modules = Module.objects.filter(course_id=course_id).order_by('order')
    serializer = ModuleSerializer(modules, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def module_lessons(request, module_id):
    lessons = Lesson.objects.filter(module_id=module_id).order_by('order')
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_module(request):
    if request.user.role != 'instructor':
        return Response({"error": "Only instructors can create modules."}, status=status.HTTP_403_FORBIDDEN)

    course_id = request.data.get('course')
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ModuleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(course=course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_lesson(request):
    if request.user.role != 'instructor':
        return Response({"error": "Only instructors can create lessons."}, status=status.HTTP_403_FORBIDDEN)

    module_id = request.data.get('module')
    try:
        module = Module.objects.get(id=module_id)
    except Module.DoesNotExist:
        return Response({"error": "Module not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = LessonSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(module=module)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lesson_detail(request, lesson_id):
    try:
        lesson = Lesson.objects.get(id=lesson_id)
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)
    except Lesson.DoesNotExist:
        return Response({"error": "Lesson not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_lesson(request, lesson_id):
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        return Response({"error": "Lesson not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.user != lesson.module.course.instructor:
        return Response({"error": "Only the instructor can update this lesson."}, status=status.HTTP_403_FORBIDDEN)

    serializer = LessonSerializer(lesson, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)