from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from django.db.models import Count

from datetime import date, timedelta

from Course.models import *

@csrf_exempt
def setTime(request):

    if request.method == "POST":

        post = request.POST

        if post:

            Course_ID = post.get('Course_ID',0)

            Student_ID = post.get('Student_ID',0)

            year, mon, day = post.get('Date',0).split('/')

            Date = date(int(year), int(mon), int(day))

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

        comments = Comment.objects.filter(course_id = Course_ID, course_date__lt = date).order_by('course_date')

        for comment in comments:

            date = comment.course_date

            if date not in commentDates:

                commentDates.append(date)

            if len(commentDates) == 1:

                break

    elif Direct == "Next":

        comments = Comment.objects.filter(course_id = Course_ID, course_date__gt = date).order_by('-course_date')

        for comment in comments:

            date = comment.course_date

            if date not in commentDates:

                commentDates.append(date)

            if len(commentDates) == 1:

                break

    else:

        comments = Comment.objects.filter(course_id = Course_ID, course_date__lte = date).order_by('course_date')

        for comment in comments:

            date = comment.course_date

            if date not in commentDates:

                commentDates.append(date)

            if len(commentDates) == 3:

                break

    Dates = []

    for date in commentDates:

        Dates.append(date.strftime("%Y-%m-%d"))

    Students = []

    for application in Application.objects.filter(course_id = Course_ID):

        student_id = application.student_id

        Student = {

            'ID': student_id,
            "Name": student_id,
            "Comments": [],
            
        }

        for date in commentDates:

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

                return JsonResponse({'response': 'Valid', 'comments': Comments})

    return JsonResponse({'response': 'inValid'})

