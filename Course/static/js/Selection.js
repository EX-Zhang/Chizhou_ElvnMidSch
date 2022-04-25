function Course_Action(Course_ID, Student_ID, Action_Type) {

    $.post("/courses/selection/" + Course_ID, { Course_ID: Course_ID, Student_ID: Student_ID, Action_Type: Action_Type }, function (result) {

        alert(result.response);

        location.reload();

    });

}

function init_Selection_Index(Courses) {

    var Droplist_HTML = "";

    for (var ID in Courses) {

        var Course = Courses[ID];

        Droplist_HTML += "<option value='" + ID + "'" + (Course.Valid == 1 ? 'selected' : '') + ">" + Course.Name + "</option>";

    }

    $("#CourseNameDroplist").html(Droplist_HTML);

    if (Object.keys(Courses).length > 0) {

        Name_Droplist_Change(Courses);

    }

}

function set_Selection_Index(Course) {

    $("#CourseInfoModalLabel").text(Course.Name + "简介");

    $("#CourseInfoModalBody").text(Course.Info);

    $("#CourseTeacher").text(Course.Teacher);

    $("#CoursePlace").text(Course.Place);

    $("#CourseTotal").text(Course.Total);

    $("#CourseCurrent").text(Course.Current);

    var valid = Course.Valid;

    var btn_HTML = "";

    if (valid == 0) {

        btn_HTML = generate_CourseActionbtn_HTML(Course.ID, "Apply", "#FA603F", "点击报名");

    }
    else if (valid == 1) {

        btn_HTML = generate_CourseActionbtn_HTML(Course.ID, "Cancel", "#898786", "确认取消");

    }

    $("#CourseActionDIV").html(btn_HTML);

}

function generate_CourseActionbtn_HTML(Course_ID, Action_Type, btn_Color, btn_Text) {

    return '<br><button class="btn btn-primary" onclick="Course_Action_btn(' + "'" + Course_ID + "'," + "'" + Action_Type + "'" + ')" style="background-color:' + btn_Color + '">' + btn_Text + '</button>';

}

function Name_Droplist_Change(Courses) {

    set_Selection_Index(Courses[$("#CourseNameDroplist").val()]);

}
