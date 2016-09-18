function toggleAccordion(id) {
    var x = document.getElementById(id);
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else {
        x.className = x.className.replace(" w3-show", "");
    }
}

function setParameters() {
    for (let j = 0; j < n; j++) {



        for (let i = 0; i < categoricalFeatures.length; i++) {
            parameters["list"+(j+1)][categoricalFeatures[i]]["matters"] = document.getElementById("list"+(j+1) + "_" + categoricalFeatures[i]).value != "question" && document.getElementById("list"+(j+1) + "_" + categoricalFeatures[i]).value != "half";
            parameters["list"+(j+1)][categoricalFeatures[i]]["value"] = document.getElementById("list"+(j+1) + "_" + categoricalFeatures[i]).value;
        }

        for (let i = 0; i < numericFeatures.length; i++) {
            parameters["list"+(j+1)][numericFeatures[i]]["matters"] = document.getElementById("list"+(j+1) + "_" + numericFeatures[i] + "_from").value != "" || document.getElementById("list"+(j+1) + "_" + numericFeatures[i] + "_to").value != "";
            parameters["list"+(j+1)][numericFeatures[i]]["value"] = [
                document.getElementById("list"+(j+1) + "_" + numericFeatures[i] + "_from").value,
                document.getElementById("list"+(j+1) + "_" + numericFeatures[i] + "_to").value
            ];
        }
    }

    parameters["same_features"] = $('#same_features').val();

    parameters["differ_feature"] = document.getElementById("differ_feature").value;

    parameters["which_is_higher"] = document.getElementById("which_is_higher").value;

    parameters["bonferroni"] = document.getElementById("bonferroni").value;

    parameters["n"] = n;


    if ($.inArray(parameters["differ_feature"], parameters["same_features"]) != -1) {
        let message = document.getElementById('message');
        message.innerHTML = "Параметр, по которому листы должны отличаться не может одновременно быть в списке параметров, " +
            "по которым листы не дожны отличаться.";
        showSuccessMessage();
        return
    }

    if (parameters["differ_feature"] != "question" && parameters["which_is_higher"] === "question") {
        let message = document.getElementById('message');
        message.innerHTML = "Вы не указали, какой лист должен иметь высокие значения.";
        showSuccessMessage();
        return
    }

    var body = document.body;

    body.className = "loading";
    $.ajax({
        url: '_set_parameters',
        type: 'post',
        data: JSON.stringify(parameters),
        contentType: 'application/json',
        dataType: 'json',
        success: function (result) {
            if (result['result'] == 'success') {
                window.location = "/statistics";
            } else {
                let message = document.getElementById('message');
                message.innerHTML = "Фильтр с заданными параметрами возвращает пустой лист. Измените фильтр.";
                showSuccessMessage();
                return
            }
        }
    }).done(function () {
        body.className = "";
    });

    // console.log(parameters);
}

function showSuccessMessage() {
    var modal = document.getElementById('successMessage');
    modal.style.display = "block";
}

function hideSuccessMessage() {
    var modal = document.getElementById('successMessage');
    modal.style.display = "none";
}