
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from datetime import date

from Course.models import *

@csrf_exempt
def CoursesUpload(request):

    if request.method == "POST":

        post = request.POST

        if post:

            n = int(post.get('length'))

            Course_Uploaded = []

            error_exist = False

            for i in range(n):

                result = CourseUpload(str(i), post)

                response = result['response']

                if response == 'success' or response == 'exist':

                    Course_Uploaded.append(result['ID'])

                elif response == 'error':

                    error_exist = True

                else:

                    JsonResponse({'response': 'error'})

            response = 'success'

            if error_exist:

                response = 'partsuccess'

            return JsonResponse({'response': response, 'uploaded': Course_Uploaded})

    return JsonResponse({'response': 'error'})

def CourseUpload(i, Courses):

    ID = Courses.get('Courses['+i+'][ID]')

    Name = Courses.get('Courses['+i+'][Name]')

    Info = Courses.get('Courses['+i+'][Info]')

    Teacher = Courses.get('Courses['+i+'][Teacher]')

    Place = Courses.get('Courses['+i+'][Place]')

    y, m, n = Courses.get('Courses['+i+'][Avail]').split('-')

    Avail = date(int(y), int(m), int(n))

    Time = Courses.get('Courses['+i+'][Time]')

    Number = int(Courses.get('Courses['+i+'][Number]'))

    courses = Course.objects.filter(course_name = Name, course_info = Info, teacher_id = Teacher, course_place = Place, course_time = Time, available_date = Avail, total_num = Number)

    if len(courses) > 0:

        return {'response':'exist', 'ID': ID}

    if Course.objects.get_or_create(course_name = Name, course_info = Info, teacher_id = Teacher, course_place = Place, course_time = Time, available_date = Avail, total_num = Number)[1]:
        
        return {'response': 'success', 'ID': ID}

    return {'response': 'error'}
