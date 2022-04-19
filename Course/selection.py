
from django.http import JsonResponse

from datetime import date

from Course.models import *

def get_courses(Student_ID):

    Courses_Array = []

    courses = Course.objects.filter(available_date <= date.today())

    Applied_Course = -1

    for course in courses:

        Applied_Course = get_course_info(course, Student_ID, Courses_Array)

    if Applied_Course != -1:

        for cur in Courses_Array:

            if cur['Course']['ID'] != Applied_Course:

                cur['Valid'] = 2

    return {'Courses': Courses_Array, 'Student_ID': Student_ID}


def get_course_info(Course_Info, Student_ID, Courses_Array):

    ID = Course_Info.course_id

    Name = Course_Info.course_name

    Valid = 2

    if Student_ID >= 0:

        Valid = len(Application.objects.filter(student_id = Student_ID, course_id = ID))

    Courses_Array.append({

        'Course': {

            'ID': ID,
            
            'Name': Name,
            
            'Info': Course_Info.course_info,

            'Place': Course_Info.course_place,

            'Total': Course_Info.total_num,

            'Current': len(Application.objects.filter(course_id = ID)),
            
        },

        'Valid': Valid,

    })

    if Valid == 1:

        return ID

    return -1

def apply_for_course(Course_ID,Student_ID):

    try:
        course = Course.objects.get(course_id = Course_ID)

        current_num = len(Application.objects.filter(course_id = Course_ID))

        if date.today() > course.available_date:

            return JsonResponse({'response':'已经超过报名截止时间'})

        if len(Application.objects.filter(course_id = Course_ID, student_id = Student_ID)) > 0:

            return JsonResponse({'response':"请勿重复报名"})

        if current_num >= course.total_num:

            return JsonResponse({'response':"报名人数超过班级人数"})

        Application.objects.create(course_id = Course_ID, student_id = Student_ID)

        return JsonResponse({'response':"成功报名"},)

    except DoesNotExist:
        return JsonResponse({'response':"课程ID不存在"})

    return JsonResponse({'response':"未知错误发生"})

def cancel_course(Course_ID,Student_ID):

    result = Application.objects.filter(course_id = Course_ID, student_id = Student_ID)

    if len(result) < 1:
        
        return JsonResponse({'response':"您尚未报名"},)

    result.delete()

    return JsonResponse({'response':"成功取消"},)
