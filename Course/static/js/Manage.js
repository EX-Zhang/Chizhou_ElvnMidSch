
function ReadExcelFile() {

    var filePath = $("#ExcelFile").get(0).files[0];

    if (filePath == undefined || filePath == null) {
        return;
    }

    var fileReader = new FileReader();

    fileReader.onload = function (ev) {
        try {

            var data = ev.target.result;

            workbook = XLSX.read(data, { type: 'binary', cellDates: true });

            courses = [];

        } catch (e) {

            alert('文件类型不正确');

            return;
        }

        var fromTo = '';

        for (var sheet in workbook.Sheets) {

            if (workbook.Sheets.hasOwnProperty(sheet)) {

                fromTo = workbook.Sheets[sheet]['!ref'];

                courses = courses.concat(XLSX.utils.sheet_to_json(workbook.Sheets[sheet]));

            }

        }

        $(".CoursesRow").remove();

        read_Excel_Table(courses);

    };

    fileReader.readAsBinaryString(filePath);

}

function read_Excel_Table(Courses) {

    var n = Courses.length;

    var table = $("#CoursesTable");

    for (var i = 0; i < n; i++) {

        set_Table_Row(read_Excel_Row(i, Courses[i]));

    }

}

function set_Table_Row(Course) {

    var ID = Course.ID;

    $("#CoursesTable").append("<tr id='" + ID + "' class='CoursesRow'></tr>");

    var row = $("#" + ID);

    row.append(set_Info(Course, "Name"));

    row.append("<td><button id='" + ID + "info_btn' type='button' value='" + Course.Info + "' onclick='Course_Info_Editor(" + ID + ',"' + Course.Name + '"' + ")'>详细</button></td>");

    row.append(set_Info(Course, "Teacher"));

    row.append(set_Info(Course, "Place"));

    row.append(set_Info(Course, "Avail"));

    row.append("<td class='Time' onclick='Time_Editor(" + ID + ',"' + Course.Name + '"' + ")'>" + Course.Time + "</td>");

    row.append(set_Info(Course, "Number"));

}

function set_Info(Course, Info_Type) {

    var modal_fun = "Info_Edit(" + Course.ID + ',"' + Info_Type + '")';

    return "<td class='" + Info_Type + "' onclick='" + modal_fun + "'>" + Course[Info_Type] + "</td>";

}

function Course_Info_Editor(id, Name) {

    $("#InfoModalLabel").text(Name + "详情");

    var text_html = "<div><textarea id='" + id + "Info' rows='3' style='width:100%;resize:none;' placeholder='请勿输入过多内容'></textarea><div>";

    $("#InfoModalBody").html(text_html);

    $("#" + id + "Info").val($('#' + id + 'info_btn').val());

    $("#SubmitInfo").attr('onclick', 'Course_Info_Edit(' + id + ')');

    $("#InfoModal").modal('show');

}

function Course_Info_Edit(id) {

    $('#' + id + "info_btn").val($('#' + id + "Info").val());

    $("#InfoModal").modal('hide');

}

function Info_Edit(id, Info_Type) {

    var input_type = 'text';

    switch (Info_Type) {

        case "Number":

            input_type = 'number';
            break;

        case "Avail":

            input_type = 'date';
            break;

    }

    var cell = $("#" + id).find("." + Info_Type);

    var onBlur = 'set_Info_Edit(' + id + ',"' + Info_Type + '")';

    cell.html("<input id='" + id + Info_Type + "'class='" + Info_Type + " text-center CoursesRow' type='" + input_type + "' onBlur='" + onBlur + "' value='" + cell.text() + "'/>");

    $("#" + id + Info_Type).focus();

    cell.removeAttr('onclick');

}

function set_Info_Edit(id, Info_Type) {

    var cell = $("#" + id).find("." + Info_Type);

    cell.html($("#" + id + Info_Type).val());

    cell.attr("onclick", "Info_Edit(" + id + ",'" + Info_Type + "')");

}

function Time_Editor(id, name) {

    $("#InfoModalLabel").text(name + "上课时间");

    var text = $("#" + id).find(".Time").text().split(' ');

    var time = text[1];

    var week = text[0];

    var html = "<div>";

    html += "<input type='checkbox' id='day1' value='一'/>星期一&ensp;";

    html += "<input type='checkbox' id='day2' value='二'/>星期二&ensp;";

    html += "<input type='checkbox' id='day3' value='三'/>星期三&ensp;";

    html += "<input type='checkbox' id='day4' value='四'/>星期四&ensp;";

    html += "<input type='checkbox' id='day5' value='五'/>星期五&ensp;";

    html += "</div><br>";

    html += "上课时间：<input type='time' id='Time' value='" + time + "'/>";

    $("#InfoModalBody").html(html);

    for (var i in week) {

        var day = week[i];

        switch (day) {

            case '一':

                $("#day1").attr("checked", "checked");
                break;

            case '二':

                $("#day2").attr("checked", "checked");
                break;

            case '三':

                $("#day3").attr("checked", "checked");
                break;

            case '四':

                $("#day4").attr("checked", "checked");
                break;

            case '五':

                $("#day5").attr("checked", "checked");
                break;

        }

    }

    $("#SubmitInfo").attr('onclick', 'Time_Edit(' + id + ')');

    $("#InfoModal").modal('show');

}

function Time_Edit(id) {

    var value = "";

    for (var i = 1; i <= 5; i++) {

        var cur = $("#day" + i);

        if (cur.get(0).checked) {

            value += cur.val() + "，";

        }

    }

    $("#" + id).find(".Time").text(value.substring(0, value.length - 1) + " " + $("#Time").val());

    $("#InfoModal").modal('hide');

}

function upload_Courses() {

    var Courses = $("#CoursesTable").find(".CoursesRow");

    var n = Courses.length;

    var Courses_Uploaded = [];

    var Keys = ['Name', 'Teacher', 'Place', 'Avail', 'Time', 'Number'];

    for (var i = 0; i < n; i++) {

        var ID = Courses[i].id;

        var Course = { ID: ID, Info: $("#" + ID + "info_btn").val() };

        for (var i in Keys) {

            var key = Keys[i];

            Course[key] = $("#" + ID).find("." + key).text();

        }

        Courses_Uploaded.push(Course);

    }

    console.log(Courses_Uploaded.toString());

    $.post("/courses/manage/upload", {}, function (result) {


    });

}

function read_Excel_Row(ID, Course) {

    return {

        ID: ID,

        Name: Course['课程名称'],

        Info: Course['课程详情'],

        Teacher: Course['授课老师'],

        Place: Course['授课地点'],

        Avail: function (date) {

            var m = date.getMonth() + 1;

            return date.getFullYear() + "-" + (m < 10 ? "0" : "") + m + "-" + date.getDate();

        }(Course['截止时间']),

        Time: Course['上课时间'],

        Number: Course['上课人数']

    };

}
