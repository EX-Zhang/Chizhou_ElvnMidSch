
function set_Summary_table(Comments, Course_ID) {

    var table = $("#SummaryTable");

    var bgcolor = false;

    for (var i in Comments.Students) {

        var Student = Comments.Students[i];

        table.append("<tr id='" + Student.ID + "'" + (bgcolor ? ' bgcolor="#FEB6A6"' : '') + " class='SummaryRow'><td class='NameCol'>" + Student.Name + "</td></tr>");

        bgcolor = bgcolor ? false : true;

    }

    add_to_tail(Comments.Dates, Comments.Students, Course_ID);

    if (Comments.Dates.length >= 3) {

        var div = $("#btnDiv");

        div.append("<button type='button' id='Prev_btn' class='btn btn-default btn-xs CommentAction' style='float:left;'>上一日</button>");

        div.append("<button type='button' id='Next_btn' class='btn btn-default btn-xs CommentAction' style='float:right;'>下一日</button>");

        var prev_html = "set_New_Comments(" + Course_ID + ",'Prev')";

        $("#Prev_btn").attr("onclick", "'" + prev_html + "'");

        var next_html = "set_New_Comments(" + Course_ID + ",'Next')";

        $("#Next_btn").attr("onclick", "'" + next_html + "'");

    }

}

function add_to_tail(Dates, Students, Course_ID) {

    var n = Dates.length;

    var DateHeader = $("#Date");

    var ContentHeader = $("#Head");

    for (var i = 0; i < n; i++) {

        var date = Dates[i];

        DateHeader.append("<th colspan='2' class='" + date + "'><B>" + date + "</B></th>");

        ContentHeader.append("<th class='AttendCol " + date + "'>考勤</th>");

        ContentHeader.append("<th class='CommentCol " + date + "'>评价</th>");

    }

    for (var j in Students) {

        Student = Students[j];

        var row = $("#" + Student.ID);

        for (var i = 0; i < n; i++) {

            var date = Dates[i];

            row.append("<td id='Attend' class='AttendCol " + date + "'>" + Student.Comments[i].Attend + "</td>");

            var Comment = Student.Comments[i].Comment;

            if (Comment.length > 15) {

                var btn_HTML = "show_Comment(" + Student.ID + "," + Course_ID + ',"' + date + '")';

                row.append("<td id='Comment' class='CommentCol " + date + "' onclick='" + btn_HTML + "'>" + Comment.substring(0, 10) + "······" + "</td>");

            }
            else {

                row.append("<td id='Comment' class='CommentCol " + date + "'>" + Comment + "</td>");

            }

        }

    }

}

function add_to_head(Dates, Students, Course_ID) {

    var n = Dates.length;

    var DateHeader = $("#Date");

    var ContentHeader = $("#Head");

    for (var i = 0; i < n; i++) {

        var date = Dates[i];

        DateHeader.prepend("<th colspan='2' class='" + date + "'><B>" + date + "</B></th>");

        ContentHeader.prepend("<th class='Attend " + date + "'>考勤</th>");

        ContentHeader.prepend("<th class='Comment " + date + "'>评价</th>");

    }

    for (var j in Students) {

        var Student = Students[j];

        var row = $("#" + Student.ID);

        for (var i = 0; i < n; i++) {

            var date = Dates[i];

            row.prepend("<td id='Attend' class='Attend " + date + "'>" + Student.Comments[i].Attend + "</td>");

            var Comment = Student.Comments[i].Comment;

            row.prepend("<td id='Comment' class='Comment " + date + "'>" + Comment + "</td>");

            if (Comment.length > 15) {

                var btn_HTML = "show_Comment(" + Student.ID + "," + Course_ID + ",'" + date + "')";

                row.find("#Comment").find("." + date).attr("onclick", "'" + btn_HTML + "'");

            }

        }

    }
}

function show_Comment(Student_ID, Course_ID, Course_Date) {

    $.post("/courses/summary/getComment", { Student_ID: Student_ID, Course_ID: Course_ID, Course_Date: Course_Date }, function (result) {

        if (result.response == 'Valid') {

            $('#CommentModalLabel').text(result.student_name + "评价");

            $('#CommentModalBody').text(result.comment);

            $('#CommentModal').modal('show');

        }

    });

}

function set_New_Comments(ID, Direct) {

    var Dates = $("#Date").children();

    var n = Dates.length;

    if (n < 4) {
        return;
    }

    var first = Dates[1].innerText;

    var last = Dates[n - 1].innerText;

    var Date = "";

    if (Direct == "Next") {

        Date = last;

    }
    else if (Direct == "Prev") {

        Date = first;

    }

    $.post('/courses/summary/getNewComments', { ID: ID, Direct: Direct, Date: Date }, function (result) {

        if (result.response != "Valid") {
            return;
        }

        var Comments = result.comments;

        if (Direct == "Next") {

            add_to_tail(Comments.Dates, Comments.Students, Course_ID);

            $("." + first).remove();

        }
        else if (Direct == "Prev") {

            add_to_head(Comments.Dates, Comments.Students, Course_ID);

            $("." + last).remove();

        }

    });

}
