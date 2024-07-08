from rest_framework import serializers
from .models import User, Student, Staff, Course, Attendance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['id', 'user', 'courses']

class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Staff
        fields = ['id', 'user', 'courses']

class CourseSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)
    lecturers = StaffSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'active_for_attendance', 'students', 'lecturers']

class AttendanceSerializer(serializers.ModelSerializer):
    attendees = StudentSerializer(many=True, read_only=True)
    absences = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'course', 'date', 'time', 'attendees', 'absences']
