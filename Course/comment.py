from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from datetime import date, timedelta

from Course.models import *

@csrf_exempt
def setTime(request):

    if request.method == "POST":

        post = request.POST

        if post:

            Course_ID = post.get('Course_ID',0)

            Students = post.get('Students')

            year, mon, day = post.get('Date',0).split('/')

            Date = date(int(year), int(mon), int(day))

            if(Students != None):

                Students = Students[1 : len(Students) - 1]

                if len(Students) == 0:

                    return JsonResponse({'response':'发生未知错误'})

                StudentID = []

                for Student in Students.split(','):

                    cur_student = int(Student)

                    comments = Comment.objects.filter(course_id = Course_ID, student_id = cur_student, course_date = Date)

                    if len(comments) == 0:

                        Comment.objects.create(course_id = Course_ID, student_id = cur_student, course_date = Date, absent = 0)

                        StudentID.append(cur_student)

                    elif comments[0].absent != 1:

                        comments.update(absent = 0)

                        StudentID.append(cur_student)

                
                return JsonResponse({'response':'Valid', 'Students': StudentID})
            

            Student_ID = post.get('Student_ID')

            if Student_ID == None:

                return JsonResponse({'response':'发生未知错误'})

            Time = post.get('Time')

            comments = Comment.objects.filter(course_id = Course_ID, student_id = Student_ID, course_date = Date)

            if len(comments) == 0:

                if(Time == None):

                    Comment.objects.create(course_id = Course_ID, student_id = Student_ID, course_date = Date, absent = 1)

                else:

                    Comment.objects.create(course_id = Course_ID, student_id = Student_ID, course_date = Date, absent = 1, attend = Time)
                
            else:

                if Time == None:

                    comments.update(absent = 1)

                else:

                    comments.update(attend = Time)


            return JsonResponse({'response': 'Valid'})

    return JsonResponse({'response':'发生未知错误'})

@csrf_exempt
def setComment(request):

    if request.method == "POST":

        post = request.POST

        if post:

            Course_ID = post.get('Course_ID',0)

            Student_ID = post.get('Student_ID',0)

            year, mon, day = post.get('Date',0).split('/')

            Date = date(int(year), int(mon), int(day))

            CommentText = post.get('Comment',0)

            ParentAvail = post.get('ParentAvail',0)

            comments = Comment.objects.filter(course_id = Course_ID, student_id = Student_ID, course_date = Date)

            if len(comments) == 0:

                Comment.objects.create(course_id = Course_ID, student_id = Student_ID, course_date = Date, comment = CommentText, parent_available = ParentAvail)

            else:

                comments.update(comment = CommentText, parent_available = ParentAvail)

            return JsonResponse({'response': 'Valid'})

    return JsonResponse({'response':'发生未知错误'})

def getComments(Course_ID, Direct, date):

    comments = []

    commentDates = []

    if Direct == "Prev":

        comments = Comment.objects.filter(course_id = Course_ID, course_date__lt = date).order_by('-course_date')

        for comment in comments:

            date = comment.course_date

            if date not in commentDates:

                commentDates.append(date)

            if len(commentDates) == 1:

                break

    elif Direct == "Next":

        comments = Comment.objects.filter(course_id = Course_ID, course_date__gt = date).order_by('course_date')

        for comment in comments:

            date = comment.course_date

            if date not in commentDates:

                commentDates.append(date)

            if len(commentDates) == 1:

                break

    else:

        comments = Comment.objects.filter(course_id = Course_ID, course_date__lte = date).order_by('-course_date')

        for comment in comments:

            date = comment.course_date

            if date not in commentDates:

                commentDates.append(date)

            if len(commentDates) == 3:

                break

    Dates = []

    for date in commentDates[::-1]:

        Dates.append(date.strftime("%Y-%m-%d"))

    Students = []

    for application in Application.objects.filter(course_id = Course_ID):

        student_id = application.student_id

        Student = {

            'ID': student_id,
            "Name": student_id,
            "Comments": [],
            
        }

        for date in commentDates[::-1]:

            comment = comments.filter(student_id = student_id, course_date = date)
        
            Attend = "正常"

            CommentString = ""

            if len(comment) > 0:

                if comment[0].attend != None:

                    Attend = "迟到：" + comment[0].attend.strftime("%H:%M")

                elif comment[0].absent == 1:

                    Attend = "缺席"

                CommentString = comment[0].comment;

                if CommentString == None:

                    CommentString = ""

                elif len(CommentString) > 15:

                    CommentString = CommentString[0:10] + "······"

            Student['Comments'].append({'Attend': Attend, 'Comment': CommentString})

        Students.append(Student)

        print(type(Students))

    return {'Dates': Dates, 'Students': Students}
    

@csrf_exempt
def getComment(request):

    if request.method == "POST":

        post = request.POST

        if post:

            Student_ID = post.get('Student_ID')

            Course_ID = post.get('Course_ID')

            Course_Date = post.get('Course_Date')

            year, mon, day = Course_Date.split('-')

            comments = Comment.objects.filter(student_id = Student_ID, course_id = Course_ID, course_date = date(int(year), int(mon), int(day)))

            if len(comments) >= 1:

                return JsonResponse({'response': 'Valid', 'comment': comments[0].comment, 'student_name': Student_ID,})

    return JsonResponse({'response': 'inValid'})

@csrf_exempt
def getNewComments(request):

    if request.method == 'POST':

        post = request.POST

        if post:

            ID = post.get('ID')

            Direct = post.get('Direct')

            year, mon, day = post.get('Date').split('-')

            Comments = getComments(ID, Direct, date(int(year), int(mon), int(day)))

            if len(Comments['Dates']) == 1:

                return JsonResponse({'response': 'Valid', 'comments': Comments, 'id': ID,})

    return JsonResponse({'response': 'inValid'})

def getCurrentTerm():

    today = date.today()

    year = int(today.strftime("%Y"))

    mon = int(today.strftime("%m"))

    if mon >= 2 and mon <= 7:

        return [date(year,2,1), date(year,6,30)]

    return [date(year-1,9,1), date(year,1,31)]

def getRecentAttendNum(Course_ID, Student_Num):

    comments = Comment.objects.filter(course_id = Course_ID, course_date__lte = date.today()).order_by('-course_date')

    Dates = []

    for comment in comments:

        Date = comment.course_date

        if Date not in Dates:

            Dates.append(Date)

        if len(Dates) == 4:

            break

    Attend_Num = []

    for Date in Dates:

        num = 0

        for comment in comments.filter(course_date = Date):

            if comment.absent == 1 and comment.attend == None:

                num += 1

        Attend_Num.append(Date.strftime("%m") + "月" + Date.strftime("%d") + "日：" + str(Student_Num - num) + " ")

    while len(Attend_Num) < 4:

        Attend_Num.append('')

    return Attend_Num[::-1]

def date_to_str(Date):

    return Date.strftime("%Y") + '年' + Date.strftime("%m") + "月"
