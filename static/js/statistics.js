function createLists() {
    var statisticsParameters = {};
    statisticsParameters["length"] = document.getElementById("length").value;
    statisticsParameters["statistics"] = document.getElementById("statistics").value;
    statisticsParameters["frequency"] = document.getElementById("frequency").value;

    var body = document.body;

    body.className = "loading";
    $.ajax({
        url: '_create',
        type: 'post',
        data: JSON.stringify(statisticsParameters),
        contentType: 'application/json',
        dataType: 'json',
        success: function (data) {
            // window.location = "/statistics";
            // let feedback = data.result["feedback"];
            // let id = data.result["id"];
            //
            // if (feedback == "success") {
            //     let ok = document.getElementById('ok');
            //     ok.onclick = function () {
            //         window.location.assign("/search?id=" + id);
            //     };
            //     showSuccessMessage();
            // } else {
            //     let ok = document.getElementById('ok');
            //     ok.onclick = function () {
            //         hideSuccessMessage();
            //     };
            //
            //     let message = document.getElementById('message');
            //     message.innerText = "Невозможно сохранить статью. Обратитесь к администрации.";
            //     showSuccessMessage();
            // }
        }
    }).done(function () {
        body.className = "";
    });

    console.log(statisticsParameters);
}
