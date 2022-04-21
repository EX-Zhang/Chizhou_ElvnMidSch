
function init_Time_Info(Student_ID, Absent, Time) {

    set_Time_Info(Student_ID, Absent == "1" && Time == "None" ? 1 : 0, Time);

}

function set_Time_Info(Student_ID, Absent, Time) {

    if (Time == null) {
        return;
    }

    var btn = $("#" + Student_ID).find("#Absent");

    if (btn == null) {
        return;
    }

    if (Absent == 1) {

        btn.text("缺席");

        btn.attr('class', 'btn btn-warning btn-xs');

        btn.attr('style', 'color: white');

        btn.removeAttr('disabled');

        $("#" + Student_ID).find("#Name").removeAttr("onclick");

    }
    else if (Time != "" && Time != "None") {

        btn.text(Time.substring(0, 5) + "已到");

        btn.attr('class', 'btn btn-success btn-xs');

        btn.attr('disabled', 'disabled');

        $("#" + Student_ID).find("#Name").removeAttr("onclick");

    }

}

function set_Absent(Course_ID, Student_ID) {

    $.post('/courses/comment/setTime', { Student_ID: Student_ID, Course_ID: Course_ID, Date: new Date().toLocaleDateString() }, function (result) {

        if (result.response == "Valid") {

            set_Time_Info(Student_ID, 1, "00:00");

        }

    });

}

function set_Attend(Course_ID, Student_ID) {

    var Time = new Date().toLocaleTimeString().substring(0, 5);

    var time_info = {

        Course_ID: Course_ID,
        Student_ID: Student_ID,
        Date: new Date().toLocaleDateString(),
        Time: Time

    };

    $.post('/courses/comment/setTime', time_info, function (result) {

        if (result.response != "Valid") {

            alert("未知错误发生");
            return;

        }

        set_Time_Info(Student_ID, 0, Time);

    });

}

function init_Comment_Modal(Course_ID, Student_ID, Student_Name) {

    if ($("#" + Student_ID + "textarea").length > 0) {

        $('#CommentModal').modal('show');

        return;
    }

    $("#CommentModal").modal({ backdrop: 'static' });

    $("#CommentModalLabel").text("学生" + Student_Name + "（学号：" + Student_ID + "）评价");

    var text_html = "<div><textarea id='" + Student_ID + "textarea' rows='5' style='width:100%;resize:none;' placeholder='请勿输入过多内容'></textarea><div>";

    text_html += "<p>家长可见：<input type='checkbox' id='ParentAvail' value='Available' checked='yes' /></p>"

    $("#CommentModalBody").html(text_html);

    var prev_comment = $("#" + Student_ID).find("#Comment").text();

    if (prev_comment != null && prev_comment != "") {

        $("#" + Student_ID + "textarea").val(prev_comment);

    }

    $("#SubmitComment").attr('onclick', "submit_comment(" + Course_ID + "," + Student_ID + ",'" + Student_Name + "')");

    $('#CommentModal').modal('show');

}

function submit_comment(Course_ID, Student_ID, Student_Name) {

    var Comment = $("#" + Student_ID + "textarea").val();

    var Comment_Info = {

        Course_ID: Course_ID,
        Student_ID: Student_ID,
        Date: new Date().toLocaleDateString(),
        Comment: Comment,
        ParentAvail: $("#ParentAvail")[0].checked ? 1 : 0

    };

    $.post('/courses/comment/setComment', Comment_Info, function (result) {

        if (result.response != "Valid") {

            alert("未知错误发生");
            return;

        }

        set_comment(Student_ID, Student_Name, Comment);

        $('#CommentModal').modal('hide');

    });

}

function set_comment(Student_ID, Student_Name, Comment) {

    if (Comment == null || Comment == '' || Comment == "None") {
        return;
    }

    var comment_cell = $("#" + Student_ID).find("#Comment");

    comment_cell.text(Comment);

    comment_cell.attr("onclick", "");

    if (Comment.length > 16) {

        comment_cell.text(Comment.substring(0, 10) + "······");

        comment_cell.attr("onclick", "show_comment_modal(" + Student_ID + ",'" + Student_Name + "','" + Comment + "')");

    }

}

function show_comment_modal(Student_ID, Student_Name, Comment) {

    $("#CommentModal").modal({ backdrop: true });

    $("#AttendInfoModalLabel").text("学生" + Student_Name + "（学号：" + Student_ID + "）评价");

    $("#AttendInfoModalBody").text(Comment);

    $('#AttendInfoModal').modal('show');

}
