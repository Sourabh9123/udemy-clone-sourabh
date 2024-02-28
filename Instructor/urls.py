from django.urls import path
from Instructor.views import CourseCreateView, LectureView, CourseDetailView, AllCourses, LectureDetailView, enrollInCourse, RatingCourseView

urlpatterns = [
    path('',AllCourses.as_view(), name="my-courses"),  # get my courses
    path('create/',CourseCreateView.as_view(), name="create-course"), #create and get all courses
    path('enroll/<uuid:course_id>/',enrollInCourse.as_view(), name = "enroll-course" ),
    
    path('create/leacture/',LectureView.as_view(), name="create-leacture"),
    
    path('leacture/<int:leacture_id>/',LectureDetailView.as_view(), name="leacture-deatil"), # get, put , delete
    
    path('get/<uuid:course_id>/',CourseDetailView.as_view(), name="detail-courseview"),  # get, delete, update, 
    path("rating/<uuid:course_id>/", RatingCourseView.as_view(), name="rating"),
]
