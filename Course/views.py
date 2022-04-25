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

    return JsonResponse({"response": "未知错误发生"})


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

        StudentID = []

        applications = Application.objects.filter(course_id = Course_ID)

        for application in applications:

            Student = {

                'Absent': None,
                'Attend': "",
                'Comment': "",
                
            }

            student_id = application.student_id

            Student['ID'] = student_id

            Student['Name'] = student_id

            StudentID.append(student_id)

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

            'StudentID': StudentID,
            
        }

        return render(request,'Comment/Comment.html',context)
    
    except DoesNotExist:
        return HttpResponse("课程ID不存在")

    return HttpResponse("未知错误发生")

def CommentSummary(request, Course_ID):

    courses = Course.objects.filter(course_id = Course_ID)

    return render(request, 'Comment/Summary.html', {'Course':{'ID': Course_ID, 'Name': courses[0].course_name}, 'Comments': dumps(getComments(Course_ID, "", date.today()))})

def CourseManage(request):

    cur_term = getCurrentTerm()

    Courses = Course.objects.filter(available_date__gte = cur_term[0], available_date__lte = cur_term[1])

    Courses_Info = []

    for Current_Course in Courses:

        Course_ID = Current_Course.course_id

        Student_Num = len(Application.objects.filter(course_id = Course_ID))

        Course_Info = {

            'ID': Course_ID,
            
            'Name': Current_Course.course_name,

            'Teacher': Current_Course.teacher_id,

            'Place': Current_Course.course_place,

            'StudentNum': Student_Num,

            'AttendNum': getRecentAttendNum(Course_ID, Student_Num),
            
        }

        Courses_Info.append(Course_Info)

    Course_Term = date_to_str(cur_term[0]) + " - " + date_to_str(cur_term[1])

    return render(request, 'Manage/Course.html', {'Course_Term': Course_Term, 'Courses': Courses_Info})

def Manage(request):

    return render(request, 'Manage/Manage.html', {})

@csrf_exempt
def CourseUpload(request):

    if request.method == "POST":

        post = request.POST

        if post:

            Name = post.get('Name')

            Info = post.get('Info')

            Teacher = post.get('Teacher')

            Place = post.get('Place')

            Avail = post.get('Avail')

            Time = post.get('Time')

            Number = post.get('Number')

            Courses = Course.objects.filter(course_name = Name, course_info = Info, teacher_id = Teacher, course_place = place, course_time = Time, available_date = date, total_num = Number)
            if len(Courses > 0):

                return JsonResponse({'response':'exist'}) 

            Course.objects.create(course_name = Name, course_info = Info, teacher_id = Teacher, course_place = place, course_time = Time, available_date = date, total_num = Number)

            return JsonResponse({'response','success'})

    return JsonResponse({'response','error'})
