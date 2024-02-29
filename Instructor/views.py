from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import  GenericAPIView
from Instructor.models import Course, Category, Instructor, Leacture, RatingCourse
from Instructor.serializers import (CourseSerializer, CategorySerializer,InstructorSerializer, 
                                    LeactureSerializer, RatingCourseSerializer
                                    )
from rest_framework.permissions import  IsAdminUser, IsAuthenticated
from students.models import Learner
from django.db import transaction
from accounts_user.models import User
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models import Avg




User = get_user_model()









class CourseCreateView(GenericAPIView):
    
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        
        data  =  request.data
        
        current_user = request.user
        if current_user.role =='instructor':
            
            instructor_obj = Instructor.objects.filter(user=current_user).exists()
            if instructor_obj:
                instructor_obj = Instructor.objects.filter(user=current_user).first()
                data['instructor'] = instructor_obj.id
            
                # data['category'] = 'Ai'  # in front end i will show then all category and pass here category id only
                serializer = CourseSerializer(data=data)      
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
        
        else: 
            return Response("you're not an instructor",status=status.HTTP_204_NO_CONTENT)
            
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    def get(self, request, *args, **kwargs):
        
        
        try:
            user=request.user
            if user.role == "instructor":
                instructor = Instructor.objects.filter(user=user).first()
                
                courses =  Course.objects.filter(instructor=instructor)
                serializer = CourseSerializer(courses, many=True)
            else:
                return Response("You are not a instructor")
            
        except Exception as e:
            return Response("something went wrong please try agin later")
        
        if not courses:
            
            return Response("no courses release for this user")
            
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    
    
    
class CourseDetailView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer
    
    def get(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id') 
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        leactures = Leacture.objects.filter(course__id=course_id)
        
        serializer = LeactureSerializer(leactures, many=True)
        course_serializer = CourseSerializer(course)
        
        data = {
            "course": course_serializer.data,
            "leactures": serializer.data
        }
         
        return Response(data, status=status.HTTP_200_OK)
   
    
    
    
    def delete(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id') 
        user = request.user
        if user.role == "instructor":
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return Response('No course ', status=status.HTTP_404_NOT_FOUND)
            
            instructor = Instructor.objects.get(user=user)
            
            
            if course.instructor == instructor:
                course.delete()
                return Response('course deleted successfuly', status=status.HTTP_204_NO_CONTENT)
        
        else:
            return Response('you are not the owner of this course', status=status.HTTP_200_OK)
            
            
                
    def put(self, request , *args, **kwargs):
        course_id = kwargs.get('course_id') 
        user = request.user
        data = request.data
        
        
        if user.role == "instructor":
            try:
                course = Course.objects.get(id=course_id)
               
                instructor_obj = Instructor.objects.filter(user=user).first()
                data['instructor'] = instructor_obj.id
             
                serializer = CourseSerializer(instance=course,data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Course.DoesNotExist:
                return Response('No course ', status=status.HTTP_404_NOT_FOUND)
        
        return Response("sorry you don't own this course ", status=status.HTTP_404_NOT_FOUND)
        
            
                
            
            
        
        
    
    



class LectureDetailView(GenericAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = LeactureSerializer
    
    def get(self, request, *args, **kwargs):
        leacture_id = kwargs.get('leacture_id')
        
        
        try:
            leacture = Leacture.objects.get(id=leacture_id)
            serializer = LeactureSerializer(leacture)
            # course = Course.objects.get(id=leacture.course)
            # course_serializer = CourseSerializer(course)
            # data = {
            #     "leacture" : serializer.data,
            #     "course" : course_serializer.data
                
            # }
            
            return Response(serializer.data , status=status.HTTP_404_NOT_FOUND)
        except Leacture.DoesNotExist:
            
            return Response("no leacture" , status=status.HTTP_404_NOT_FOUND)
        
        
        
    def put(self, request, *args, **kwargs):
        user =  request.user
        
        leacture_id = kwargs.get('leacture_id')
        data = request.data
        
        try:
            leacture = Leacture.objects.get(id=leacture_id)
            if leacture.course__instructor__user == user:
                print('yes im the owner of this course', leacture)
        except Leacture.DoesNotExist:
            return Response("no leacture" , status=status.HTTP_404_NOT_FOUND)
        
        serializer = LeactureSerializer(instance=leacture, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
    
    
    # def delete(self, request, *args, **kwargs):
    #     leacture_id = kwargs.get('leacture_id')
        
        
        
        
                
    

        
     
    
class LectureView(GenericAPIView):
    
    serializer_class = LeactureSerializer
    permission_classes = [IsAuthenticated]
    
    
    def post(self, request, *args, **kwargs):
        
    
        data = request.data
        serializer = LeactureSerializer(data= data)
   
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 
    
    # def get(self, request, *args, **kwargs):
        
        
        
        
        
        
        


class AllCourses(GenericAPIView):
    serializer_class = CourseSerializer
    # permission_classes = [IsAuthenticated]
        
    def get(self, request, *args, **kwargs):
        search_query = request.query_params.get('search', None)
        courses = Course.objects.all()
        if  search_query:
            # courses = Course.objects.filter(Q (title__icontains=search_query) |
            #                                    Q(category__title__icontains= search_query) |
            #                                    Q(instructor__name__icontains=search_query) |
            #                                    Q(description__icontains=search_query) |
            #                                    Q(tags__icontains=search_query)
            #                                    )
            
            courses = Course.objects.filter(
                    Q(title__icontains=search_query) |
                    Q(title__startswith=search_query) |
                    Q(title__endswith=search_query) |
                    
                    Q(category__title__icontains=search_query) |
                    Q(category__title__startswith=search_query) |
                    Q(category__title__endswith=search_query) |
                    
                    Q(instructor__name__icontains=search_query) |
                    Q(instructor__name__startswith=search_query) |
                    Q(instructor__name__endswith=search_query) |
                    
                    Q(description__icontains=search_query) |
                    Q(description__startswith=search_query) |
                    Q(description__endswith=search_query) |
                    
                    Q(tags__icontains=search_query) |
                    Q(tags__startswith=search_query) |
                    Q(tags__endswith=search_query)
                    
                    )
        
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

class enrollInCourse(GenericAPIView):
    
    serializer_class = CourseSerializer
    
    
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                course_id = kwargs.get('course_id')
                data = request.data
                current_user = request.user
                
                try:
                  
                    user = User.objects.get(id=current_user.id)
                    learner = Learner.objects.get(user=user)
                    learner_id = learner.id
             
                except User.DoesNotExist:
                    return Response('User not found', status=status.HTTP_404_NOT_FOUND)

                try:
                    
                    course_qs = Course.objects.get(id=course_id)
                except Course.DoesNotExist:
                    return Response('Course not found', status=status.HTTP_404_NOT_FOUND)
                
                # Update the learner field of the course using set() for many-to-many relationship
                course_qs.learner.set([learner_id])
                course_qs.save()
                
                return Response('Enrolled in course', status=status.HTTP_200_OK)
        except Exception as e:
            # Handle other exceptions, e.g., database errors
            return Response('Something went wrong: {}'.format(str(e)), status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        
        
        
class RatingCourseView(GenericAPIView):
    
    serializer_class = RatingCourseSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        
        data =  request.data
        user =  request.user    
        course_id = kwargs.get("course_id",None)
        
        if course_id:
            course = Course.objects.filter(id=course_id).first()
            if course:
                
                rating = data.get('rating')
                rating = int(rating)
                if rating >= 1 and rating <= 5:
                    data_to_pass = {
                                    "rating" : data.get("rating"),
                                    "course" : course.id,
                                    "user" :  user.id
                                }
                
                
                    serializer = RatingCourseSerializer(data=data_to_pass)
                    if serializer.is_valid():
                        serializer.save()
                        return Response("Thank Your for Your feedback", status=status.HTTP_200_OK)
                    else:
                            
                        return Response("You have already given feedback for this course or you can edit", status=status.HTTP_400_BAD_REQUEST) 
                else:
                    return Response("rating musting in range between 1 to 5", status=status.HTTP_400_BAD_REQUEST)
                
        return    Response("some thing went wrong", status=status.HTTP_404_NOT_FOUND) 
    
    
    def put(self, request, *args, **kwargs):
        
        course_id = kwargs.get('course_id',None)
        data = request.data
        user = request.user
        data['user'] = user.id
        data['course'] = course_id
        
        
        
        if data.get("rating"):
            if data.get('rating') >= 1 and data.get('rating') <= 5:
                
                if course_id:
                    instance = RatingCourse.objects.filter(course__id =  course_id , user__id = user.id).first()
                    if instance:
                        serializer = RatingCourseSerializer(instance, data=data)
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response("you haven't rated this course before so you can not edit ", status=status.HTTP_200_OK)
            else:
                return Response("rating musting in range between 1 to 5", status=status.HTTP_400_BAD_REQUEST) 

        return Response("You haven't reviewd this course" , status=status.HTTP_400_BAD_REQUEST)
        
        Response("some thing went wrong", status=status.HTTP_404_NOT_FOUND)
        
        
    
    def delete(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id',None)
        data = request.data
        user = request.user
        
        instance = RatingCourse.objects.filter(course__id = course_id, user__id =user.id)
        if instance:
            instance.delete()
            return Response("Successfully deleted your review " ,status=status.HTTP_204_NO_CONTENT)
        return Response("you haven't revied this course " ,status=status.HTTP_404_NOT_FOUND)
    
    
    
    
    
    
    
    
    
    
    
    

class mostRatedCourses(GenericAPIView):
    serializer_class = CourseSerializer
    
    def get(self, request, *args, **kwargs):
        courses_with_avg_rating = Course.objects.annotate(avg_rating=Avg('rating__rating')).order_by('-avg_rating')
        
        courses = Course.objects.all()
        for course in courses:
            print("titlle", course.title)
            print(course.rating)
        print(courses_with_avg_rating)
        
        
        serializer = CourseSerializer(courses_with_avg_rating, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)





