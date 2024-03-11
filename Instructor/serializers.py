from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from Instructor.models  import Course, Instructor, Category, Leacture, RatingCourse


class LeactureSerializer(ModelSerializer):
    
    
    class Meta:
        
        model = Leacture
        fields = '__all__'
        
        


class InstructorSerializer(ModelSerializer):
    class Meta:
        
        model = Instructor
        fields = '__all__'
        
        

class CourseSerializer(ModelSerializer):
    leactures = LeactureSerializer(many=True, read_only=True)
    # instructor = InstructorSerializer()
    class Meta:
        model = Course
        fields = ('title', 'id', 'leactures','instructor','price','category','description','learner','tags',)
    
   
            
        
        
        


class CategorySerializer(ModelSerializer):
    class Meta:
        
        model = Category
        fields = '__all__'
        
        
        
class RatingCourseSerializer(ModelSerializer):
    class Meta:
        model = RatingCourse
        fields = "__all__"
        

