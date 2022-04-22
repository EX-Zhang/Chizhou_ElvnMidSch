
function ReadExcelFile() {

    var filePath = $("#ExcelFile").get(0).files[0];

    var fileReader = new FileReader();

    fileReader.onload = function (ev) {
        try {

            var data = ev.target.result;

            workbook = XLSX.read(data, { type: 'binary' });

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

    };

    fileReader.readAsBinaryString(filePath);

}

function read_Excel_Table(Courses) {

    var n = Courses.length;

    var table = $("#CoursesTable");

    for (var i = 0; i < n; i++) {

        set_Table_Row(i, Courses[i]);

    }

}

function set_Table_Row(id, Course) {

    table.append("<tr id='" + i + "' class='CoursesRow'></tr>");

    var row = $.("#" + id);

}
