
function init_Time_Info(Student_ID, Absent_Time, Attend_Time) {

    set_Time_Info(Student_ID, "Absent", Absent_Time);

    set_Time_Info(Student_ID, "Attend", Attend_Time);

}

function set_Time_Info(Student_ID, Time_Type, Time) {

    if (Time == null || Time == "" || Time == "None") {
        return;
    }

    var btn = $("#" + Student_ID).find("#" + Time_Type);

    if (btn == null) {
        return;
    }

    if (Time_Type == "Absent") {

        btn.text(Time.substring(0, 5) + "未到");

        btn.attr('class', 'btn btn-warning btn-xs');

        btn.attr('style', 'color: white');

    }
    else if (Time_Type == "Attend") {

        btn.text(Time.substring(0, 5) + "已到");

        btn.attr('class', 'btn btn-success btn-xs');

    }

}

function init_Attend_Modal(Course_ID, Student_ID, Student_Name) {

    $("#AttendInfoModal").modal({ backdrop: 'static' });

    $("#AttendInfoModalLabel").text("学生" + Student_Name + "（学号：" + Student_ID + "）出勤");

    var time_html = "<div style='text-align:center;'><input type='time' id='Absent_Time'><button type='button' style='text-align:center;' id='Absent_btn' class='btn btn-warning btn-sm'>设置未到时间</button></div>";

    time_html += "<br><div style='text-align:center;'><input type='time' id='Attend_Time'><button type='button' style='text-align:center;' id='Attend_btn' class='btn btn-success btn-sm'>设置已到时间</button></div>";

    var cur_time = new Date().toLocaleTimeString().substring(0, 5);

    var Absent_Time = $("#" + Student_ID).find("#Absent").text().substring(0, 5);

    var Attend_Time = $("#" + Student_ID).find("#Attend").text().substring(0, 5);

    $("#AttendInfoModalBody").html(time_html);

    $("#Absent_Time").val(Absent_Time == null || Absent_Time == "" || Absent_Time == "None" ? cur_time : Absent_Time);

    $("#Attend_Time").val(Attend_Time == null || Attend_Time == "" || Attend_Time == "None" ? cur_time : Attend_Time);

    $("#Absent_btn").attr("onclick", "set_Absent_Time(" + Course_ID + "," + Student_ID + ",'" + Student_Name + "')");

    $("#Attend_btn").attr("onclick", "set_Attend_Time(" + Course_ID + "," + Student_ID + ",'" + Student_Name + "')");

    $('#AttendInfoModal').modal('show');

}

function set_Absent_Time(Course_ID, Student_ID, Student_Name) {

    var Time = $("#Absent_Time").val();

    if (Time == null || Time == "" || Time == "None") {

        alert("请设置未到时间");
        return;

    }

    if (!confirm("确认设置" + Student_Name + "（学号：" + Student_ID + "）" + Time + "未到？")) {
        return;
    }

    set_Time(Course_ID, Student_ID, "Absent", Time);

}

function set_Attend_Time(Course_ID, Student_ID, Student_Name) {

    var Time = $("#Attend_Time").val();

    if (Time == null || Time == "" || Time == "None") {

        alert("请设置已到时间");
        return;

    }

    if (!confirm("确认设置" + Student_Name + "（学号：" + Student_ID + "）" + Time + "已到？")) {
        return;
    }

    set_Time(Course_ID, Student_ID, "Attend", Time);

}

function set_Time(Course_ID, Student_ID, Time_Type, Time) {

    var time_info = {

        Course_ID: Course_ID,
        Student_ID: Student_ID,
        Date: new Date().toLocaleDateString(),
        Time: Time,
        Type: Time_Type

    };

    $.post('/courses/comment/setTime', time_info, function (result) {

        if (result.response != "Valid") {

            alert("未知错误发生");
            return;

        }

        alert("设置成功");

        set_Time_Info(Student_ID, Time_Type, Time);

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

    if (!confirm("确认评价" + Student_Name + "（学号：" + Student_ID + "）？")) {
        return;
    }

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

        alert("提交成功");

        set_comment(Student_ID, Student_Name, Comment);

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
