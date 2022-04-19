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

            Student_ID = post.get('Student_ID',0)

            Date = parseDate(post.get('Date',0))

            Time = post.get('Time',0)

            Type = post.get('Type',0)

            comments = Comment.objects.filter(course_id = Course_ID, student_id = Student_ID, course_date = Date)

            if len(comments) == 0:

                if Type == "Absent":

                    Comment.objects.create(course_id = Course_ID, student_id = Student_ID, course_date = Date, absent = Time)

                elif Type == "Attend":

                    Comment.objects.create(course_id = Course_ID, student_id = Student_ID, course_date = Date, attend = Time)

                else:

                    return JsonResponse({'response':'发生未知错误'})

            else:

                if Type == "Absent":

                    comments.update(absent = Time)

                elif Type == "Attend":

                    comments.update(attend = Time)

                else:

                    return JsonResponse({'response':'发生未知错误'})
            
            return JsonResponse({'response': 'Valid'})

    return JsonResponse({'response':'发生未知错误'})

@csrf_exempt
def setComment(request):

    if request.method == "POST":

        post = request.POST

        if post:

            Course_ID = post.get('Course_ID',0)

            Student_ID = post.get('Student_ID',0)

            Date = parseDate(post.get('Date',0))

            CommentText = post.get('Comment',0)

            ParentAvail = post.get('ParentAvail',0)

            comments = Comment.objects.filter(course_id = Course_ID, student_id = Student_ID, course_date = Date)

            if len(comments) == 0:

                Comment.objects.create(course_id = Course_ID, student_id = Student_ID, course_date = Date, comment = CommentText, parent_available = ParentAvail)

            else:

                comments.update(comment = CommentText, parent_available = ParentAvail)

            return JsonResponse({'response': 'Valid'})

    return JsonResponse({'response':'发生未知错误'})


def parseDate(datetime):

    year, mon, day = datetime.split('/')

    return date(int(year), int(mon), int(day))

def parseTime(time):

    hour, minute = time.split(':')

    return timedelta(hours = int(hour), minutes = int(minute))
