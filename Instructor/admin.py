from django.contrib import admin
from Instructor.models import Course, Instructor, Category,Leacture , RatingCourse, EnrolledCourses




class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','title']

admin.site.register(Category,CategoryAdmin)


class LeactureAdmin(admin.ModelAdmin):
    list_display = ['title','order', 'content', 'course', 'created_at','updated_at']
    
    


admin.site.register(Leacture,LeactureAdmin)
 

class CourseAdmin(admin.ModelAdmin):
    list_display = ['id','title','instructor','price','category']
    
    


class InstructorAdmin(admin.ModelAdmin):
    list_display = ['id','name','user']
    
    

admin.site.register(Course,CourseAdmin)

admin.site.register(Instructor,InstructorAdmin)


class RatingCourseAdmin(admin.ModelAdmin):
    list_display = ["id","user", "rating","course"]
    
    
admin.site.register(RatingCourse, RatingCourseAdmin)



admin.site.register(EnrolledCourses)