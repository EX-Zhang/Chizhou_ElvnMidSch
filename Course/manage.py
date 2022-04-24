
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from datetime import date

from . import models

@csrf_exempt
def CoursesUpload(request):

    if request.method == "POST":

        post = request.POST

        if post:

            Courses = post.get('Courses')

            Course_Uploaded = []

            

def CourseUpload(Course):

    Name = Course.get('Name')

    Info = Course.get('Info')

    Teacher = Course.get('Teacher')

    Place = Course.get('Place')

    y, m, n = Course.get('Avail').split('-')

    Avail = date(int(y), int(m), int(n))

    Time = Course.get('Time')

    Number = Course.get('Number')

    Courses = Course.objects.filter(course_name = Name, course_info = Info, teacher_id = Teacher, course_place = place, course_time = Time, available_date = date, total_num = Number)

    if len(Courses > 0):

            return JsonResponse({'response':'exist', 'ID': Course.get("ID")}) 

    Course.objects.create(course_name = Name, course_info = Info, teacher_id = Teacher, course_place = place, course_time = Time, available_date = date, total_num = Number)

    return JsonResponse({'response': 'success', 'ID': Course.get("ID")})
