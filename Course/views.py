from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from datetime import date

from Course.models import *

from Course.selection import *

from Course.comment import *

from json import dumps

# Create your views here.

def SelectionIndex(request):

    if request.method == "POST":

        post = request.POST

        if post:

            Action_Type = post.get('Action_Type',0)

            Student_ID = post.get("Student_ID",0)

            Course_ID = post.get('Course_ID',0)

            if Action_Type == 'Apply':

                return apply_for_course(Course_ID,Student_ID)

            elif Action_Type == 'Cancel':

                return cancel_course(Course_ID,Student_ID)

            else:

                return JsonResponse({"response": "未知错误发生"})

    Student_ID = -1

    if request.method == "GET":

        Student_ID = int(request.GET.get('id',default='-1'))

    return render(request,'Selection/Selection.html',{"Courses": dumps(get_courses(Student_ID)), "Student_ID": Student_ID})
    

@csrf_exempt
def Selection(request,Course_ID):

    if request.method == "POST":

        post = request.POST

        if post:

            Action_Type = post.get('Action_Type',0)

            Student_ID = post.get("Student_ID",0)

            Course_ID = post.get('Course_ID',0)

            if Action_Type == 'Apply':

                return apply_for_course(Course_ID,Student_ID)

            elif Action_Type == 'Cancel':

                return cancel_course(Course_ID,Student_ID)

            else:

                return JsonResponse({"response": "未知错误发生"})

    try:
        course = Course.objects.get(course_id = Course_ID)

        current_num = len(Application.objects.filter(course_id = Course_ID))

        valid = 2

        Student_ID = -1

        if request.method == "GET":

            Student_ID = int(request.GET.get('id',default='-1'))

            if Student_ID >= 0:

                valid = len(Application.objects.filter(course_id = Course_ID, student_id = Student_ID))

        if date.today() > course.available_date or (valid != 1 and current_num >= course.total_num):

            valid = 2

        context = {

            'Course': {

                'ID': Course_ID,
                'Name': course.course_name,
                'Info': course.course_info,
                'Place': course.course_place,
                'Total': course.total_num,
                'Current': current_num,

            },
            'Valid': valid,
            'Student_ID': Student_ID,

        }

        return render(request,'Selection/Selection.html',context)
    
    except DoesNotExist:
        return HttpResponse("课程ID不存在")

    return HttpResponse("未知错误发生")



@csrf_exempt
def CommentIndex(request, Course_ID):

    Course_Date = date.today()

    if request.method == "POST":

        post = request.POST

        if post:

            year, mon, day = post.get("Course_Date",0).split('-')

            Course_Date = date(int(year), int(mon), int(day))

    try:
        course = Course.objects.get(course_id = Course_ID)

        Students = []

        applications = Application.objects.filter(course_id = Course_ID)

        for application in applications:

            Student = {

                'Absent': "",
                'Attend': "",
                'Comment': "",
                
            }

            student_id = application.student_id

            Student['ID'] = student_id

            Student['Name'] = student_id

            Comments = Comment.objects.filter(course_id = Course_ID, student_id = student_id, course_date = Course_Date)

            if len(Comments) > 0:

                Student['Absent'] = Comments[0].absent
                Student['Attend'] = Comments[0].attend
                Student['Comment'] = Comments[0].comment

            Students.append(Student)

        context = {

            'Course': {

                'ID': Course_ID,
                'Name': course.course_name,
                'Date': Course_Date,
                
            },
            'Students': Students,
            
        }

        return render(request,'Comment/Comment.html',context)
    
    except DoesNotExist:
        return HttpResponse("课程ID不存在")

    return HttpResponse("未知错误发生")

def CommentSummary(request, Course_ID):

    courses = Course.objects.filter(course_id = Course_ID)

    return render(request, 'Comment/Summary.html', {'Course':{'ID': Course_ID, 'Name': courses[0].course_name}, 'Comments': dumps(getComments(Course_ID, "", date.today()))})
