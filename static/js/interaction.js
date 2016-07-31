function toggleAccordion(id) {
    var x = document.getElementById(id);
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else {
        x.className = x.className.replace(" w3-show", "");
    }
}

var parameters = {
    "list1": {
        "pos": null,
        "features": {
            "arguments": {
                "matters": false,
                "value": null,
                "categorical": true
            },
            "reflexivity": {
                "matters": false,
                "value": null,
                "categorical": true
            },
            "instrumentality": {
                "matters": false,
                "value": null,
                "categorical": true
            },
            "relation": {
                "matters": false,
                "value": null,
                "categorical": true
            },
            "part": {
                "matters": false,
                "value": null,
                "categorical": true
            },
            "name_agreement_percent": {
                "matters": false,
                "value": null,
                "categorical": false
            },
            "name_agreement_abs": {
                "matters": false,
                "value": null,
                "categorical": false
            },
            "subjective_complexity": {
                "matters": false,
                "value": null,
                "categorical": false
            },
            "objective_complexity": {
                "matters": false,
                "value": null,
                "categorical": false
            },
            "familiarity": {
                "matters": false,
                "value": null,
                "categorical": false
            },
            "age": {
                "matters": false,
                "value": null,
                "categorical": false
            },
            "imageability": {
                "matters": false,
                "value": null,
                "categorical": false
            },
            "image_agreement": {
                "matters": false,
                "value": null,
                "categorical": false
            },
            "frequency": {
                "matters": false,
                "value": null,
                "categorical": false
            },
            "syllables": {
                "matters": false,
                "value": null,
                "categorical": false
            },
            "phonemes": {
                "matters": false,
                "value": null,
                "categorical": false
            }
        }
    },
    "list2": {
        "pos": null,
        "features": {
            "arguments": {
                "matters": false,
                "value": null,
                "categorical": true
            },
            "reflexivity": {
                "matters": false,
                "value": null,
                "categorical": true
            },
            "instrumentality": {
                "matters": false,
                "value": null,
                "categorical": true
            },
            "relation": {
                "matters": false,
                "value": null,
                "categorical": true
            },
            "part": {
                "matters": false,
                "value": null,
                "categorical": true
            },
            "name_agreement_percent": {
                "matters": false,
                "value": null,
                "categorical": false
            },
            "name_agreement_abs": {
                "matters": false,
                "value": null,
                "categorical": false
            },
            "subjective_complexity": {
                "matters": false,
                "value": null,
                "categorical": false
            },
            // "objective_complexity": {
            //     "matters": false,
            //     "value": null,
            //     "categorical": false
            // },
            "familiarity": {
                "matters": false,
                "value": null,
                "categorical": false
            },
            "age": {
                "matters": false,
                "value": null,
                "categorical": false
            },
            "imageability": {
                "matters": false,
                "value": null,
                "categorical": false
            },
            "image_agreement": {
                "matters": false,
                "value": null,
                "categorical": false
            },
            "frequency": {
                "matters": false,
                "value": null,
                "categorical": false
            },
            "syllables": {
                "matters": false,
                "value": null,
                "categorical": false
            },
            "phonemes": {
                "matters": false,
                "value": null,
                "categorical": false
            }
        }
    }
};

// parameters["list2"] = parameters["list1"];

var categorical = [
    "arguments",
    "reflexivity",
    "instrumentality",
    "relation",
    "part"
];

var numeric = [
    "name_agreement_percent",
    "name_agreement_abs",
    "subjective_complexity",
    // "objective_complexity",
    "familiarity",
    "age",
    "imageability",
    "image_agreement",
    "frequency",
    "syllables",
    "phonemes"
];

var lists = [
    "list1",
    "list2"
];

function setParameters() {
    for (let j = 0; j < lists.length; j++) {

        if (document.getElementById(lists[j] + "_pos_verb").checked) {
            parameters[lists[j]]["pos"] = "verb"
        } else {
            parameters[lists[j]]["pos"] = "noun"
        }

        for (let i = 0; i < categorical.length; i++) {
            parameters[lists[j]]["features"][categorical[i]]["matters"] = document.getElementById(lists[j] + "_" + categorical[i]).value != "question";
            parameters[lists[j]]["features"][categorical[i]]["value"] = document.getElementById(lists[j] + "_" + categorical[i]).value;
        }

        for (let i = 0; i < numeric.length; i++) {
            parameters[lists[j]]["features"][numeric[i]]["matters"] = document.getElementById(lists[j] + "_" + numeric[i] + "_from").value != "" || document.getElementById(lists[j] + "_" + numeric[i] + "_to").value != "";
            parameters[lists[j]]["features"][numeric[i]]["value"] = [
                document.getElementById(lists[j] + "_" + numeric[i] + "_from").value,
                document.getElementById(lists[j] + "_" + numeric[i] + "_to").value
            ];
        }
    }

    parameters["same_features"] = $('#same_features').val();

    parameters["differ_feature"] = document.getElementById("differ_feature").value;

    parameters["which_is_higher"] = document.getElementById("which_is_higher").value;

    var body = document.body;

    body.className = "loading";
    $.ajax({
        url: '_set_parameters',
        type: 'post',
        data: JSON.stringify(parameters),
        contentType: 'application/json',
        dataType: 'json',
        success: function (data) {
            window.location = "/statistics";
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

    console.log(parameters);
}