function Course_Action(Course_ID, Student_ID, Action_Type) {

    if (!confirm("确认" + (Action_Type == "Apply" ? "报名" : "取消报名") + "？")) {
        return;
    }

    $.post("/courses/selection/" + Course_ID, { Course_ID: Course_ID, Student_ID: Student_ID, Action_Type: Action_Type }, function (result) {

        alert(result.response);

        location.reload();

    });

}
