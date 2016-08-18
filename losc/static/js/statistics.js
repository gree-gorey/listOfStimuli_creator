// window.onbeforeunload = function() {
//   return 'ВНИМАНИЕ!\nВсе несохранённые данные будут потеряны!';
// };

function createLists() {
    var statisticsParameters = {};
    statisticsParameters["length"] = document.getElementById("length").value;
    statisticsParameters["statistics"] = document.getElementById("statistics").value;
    statisticsParameters["frequency"] = document.getElementById("frequency").value;

    var givenLength = parseInt(statisticsParameters["length"]);
    // console.log(givenLength);
    var maxLength = parseInt(document.getElementById("length").getAttribute("max"));

    if (givenLength > maxLength) {
        let message = document.getElementById('message');
        message.innerHTML = "Вы ввели слишком большое значение размера листа.";
        showSuccessMessage();
    } else if (! givenLength) {
        let message = document.getElementById('message');
        message.innerHTML = "Вы не указали размер листа.";
        showSuccessMessage();
    } else {
        var body = document.body;

        body.className = "loading";
        $.ajax({
            url: '_create',
            type: 'post',
            data: JSON.stringify(statisticsParameters),
            contentType: 'application/json',
            dataType: 'json',
            success: function (data) {
                window.onbeforeunload = null;
                let feedback = data.result["feedback"];

                if (feedback == "success") {
                    let message = document.getElementById('message');
                    message.innerHTML = "Листы успешно сгенерированы.<br>Архив <b>results.zip</b> находится в папке с программой.";
                    showSuccessMessage();
                } else {
                    let message = document.getElementById('message');
                    message.innerHTML = "Не удалось сгенерировать листы с заданными параметрами.<br>Попробуйте изменить параметры.";
                    showSuccessMessage();
                }
            }
        }).done(function () {
            body.className = "";
        });
    }

    // console.log(statisticsParameters);
}

function showSuccessMessage() {
    var modal = document.getElementById('successMessage');
    modal.style.display = "block";
}

function hideSuccessMessage() {
    var modal = document.getElementById('successMessage');
    modal.style.display = "none";
}

function close_app() {
    var html = '<div class="w3-container"><div class="w3-row greeting">Вы успешно вышли из приложения.</div></div>';

    $.ajax({
        url: '_exit',
        type: 'post'
    });
    // window.location = '/';
    // window.close();
    window.document.body.innerHTML = html;
}