
from django.http import JsonResponse

from datetime import date

from Course.models import *

def get_courses(Student_ID):

    Course_Dict = {}

    courses = Course.objects.filter(available_date__gte = date.today())

    Applied_Course = -1

    for course in courses:

        Applied_Course = get_course_info(course, Student_ID, Course_Dict)

    if Applied_Course != -1:

        for ID in Course_Dict:

            cur = Course_Dict[ID]

            if cur['ID'] != Applied_Course:

                cur['Valid'] = 2

    return Course_Dict


def get_course_info(Course_Info, Student_ID, Course_Dict):

    ID = Course_Info.course_id

    Valid = 2

    if Student_ID >= 0:

        Valid = len(Application.objects.filter(student_id = Student_ID, course_id = ID))

    Course_Dict[ID] = {

        'ID': ID,
            
        'Name': Course_Info.course_name,
            
        'Info': Course_Info.course_info,

        'Teacher': Course_Info.teacher_id,

        'Place': Course_Info.course_place,

        'Total': Course_Info.total_num,

        'Current': len(Application.objects.filter(course_id = ID)),

        'Valid': Valid,

    }

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
