function toggleAccordion(id) {
    var x = document.getElementById(id);
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else {
        x.className = x.className.replace(" w3-show", "");
    }
}

function setParameters() {
    if (document.getElementById("list1_pos_verb").checked) {
        var list1_pos = "verb"
    } else {
        list1_pos = "noun"
    }

    var parameters = {
        "list1": {
            "pos": list1_pos,
            "arguments": document.getElementById("list1_arguments").value,
            "reflexivity": document.getElementById("list1_reflexivity").value,
            "instrumentality": document.getElementById("list1_instrumentality").value,
            "relation": document.getElementById("list1_name_relation").value,
            "part": document.getElementById("list1_part").value,
            "features": {
                "name_agreement_percent": {
                    "from": document.getElementById("list1_name_agreement_percent_from").value,
                    "to": document.getElementById("list1_name_agreement_percent_to").value
                },
                "name_agreement_abs": {
                    "from": document.getElementById("list1_name_agreement_abs_from").value,
                    "to": document.getElementById("list1_name_agreement_abs_to").value
                }
            }
        }
    };
    console.log(parameters);
}