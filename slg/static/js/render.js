var n;
var numericFeatures;
var categoricalFeatures;
var parameters;

$(function () {
    $.getJSON('/_get_features', {

    }, function(data) {
        var result = data.result;

        n = getValuesFromUrl()["n"];
        numericFeatures = result["numeric_features"];
        categoricalFeatures = result["categorical_features_list"];
        parameters = renderEmptyParameters();

        for (let i = 0; i < n; i++) {
            renderList(i+1);
            renderFeatures(result, i+1);
        }
        
        renderSameFeatures(result);

        renderDifferOptions(result);

        if (n == 1) {
            $("#differ").hide();
        }
    });
});

function renderEmptyParameters() {
    var parameters = {};
    for (let i = 0; i < n; i++) {
        parameters["list"+(i+1)] = {};

        for (let feature in numericFeatures) {
            parameters["list" + (i+1)][feature] = {
                "matters": false,
                "value": null,
                "categorical": false
            }
        }

        for (let j = 0; j < categoricalFeatures.length; j++) {
            parameters["list" + (i+1)][categoricalFeatures[j]] = {
                "matters": false,
                "value": null,
                "categorical": true
            }
        }

    }
    return parameters;
}

function renderDifferOptions(result) {
    var differSelect = document.getElementById("differ_feature");
    var numericFeatures = result["numeric_features"];
    for (let feature in numericFeatures) {
        let option = renderSameOption(feature);
        differSelect.appendChild(option);
    }
}

function renderSameFeatures(result) {
    var sameSelect = document.getElementById("same_features");
    var numericFeatures = result["numeric_features"];
    for (let feature in numericFeatures) {
        let option = renderSameOption(feature);
        sameSelect.appendChild(option);
    }
}

function renderSameOption(value) {
    var option = document.createElement("option");
    option.setAttribute("value", value);
    option.innerHTML = value;
    return option;
}

function renderFeatures(result, i) {
    var listCategoricalFeatures = document.getElementById("list" + i + "_categorical_features");
    var categoricalFeatures = result["categorical_features"];
    var categoricalFeaturesList = result["categorical_features_list"];
    for (let j = 0; j < categoricalFeaturesList.length; j++) {
        let select = renderCategoricalSelect("list" + i, categoricalFeaturesList[j], categoricalFeatures);
        listCategoricalFeatures.appendChild(select);
    }

    var listNumericFeatures = document.getElementById("list" + i + "_numeric_features_table");
    var numericFeatures = result["numeric_features"];
    // console.log(numericFeatures);
    for (let feature in numericFeatures) {
        let raw = renderNumericRow("list" + i, feature, numericFeatures[feature]);
        listNumericFeatures.appendChild(raw);
    }
}

function renderList(i) {
    var lists = document.getElementById("lists");

    var list = document.createElement("div");
    list.setAttribute("class", "w3-half custom-container");


    var listName = document.createElement("div");
    listName.setAttribute("class", "w3-card-4 list-header");
    listName.innerHTML = "<h5>Лист №" + i + "</h5>";
    list.appendChild(listName);

    var listAccordion = document.createElement("div");
    listAccordion.setAttribute("class", "w3-accordion w3-light-grey");

    var buttonCategorical = document.createElement("button");
    buttonCategorical.setAttribute("class", "w3-btn-block w3-left-align");
    buttonCategorical.setAttribute("onclick", "toggleAccordion('list" + i + "_categorical_features')");
    buttonCategorical.innerHTML = "Фильтр категориальных переменных";
    listAccordion.appendChild(buttonCategorical);

    var categoricalFeatures = document.createElement("div");
    categoricalFeatures.setAttribute("class", "w3-accordion-content w3-container");
    categoricalFeatures.setAttribute("id", "list" + i + "_categorical_features");
    listAccordion.appendChild(categoricalFeatures);

    var buttonNumeric = document.createElement("button");
    buttonNumeric.setAttribute("class", "w3-btn-block w3-left-align");
    buttonNumeric.setAttribute("onclick", "toggleAccordion('list" + i + "_numeric_features')");
    buttonNumeric.innerHTML = "Фильтр количественных переменных (опционально)";
    listAccordion.appendChild(buttonNumeric);

    var numericFeatures = document.createElement("div");
    numericFeatures.setAttribute("class", "w3-accordion-content w3-container");
    numericFeatures.setAttribute("id", "list" + i + "_numeric_features");
    numericFeatures.innerHTML = '<table id="list' + i + '_numeric_features_table" style="width:100%"></table>';
    listAccordion.appendChild(numericFeatures);

    list.appendChild(listAccordion);

    lists.appendChild(list);
}

function renderCategoricalSelect(list, feature, featuresHash) {
    var select = document.createElement("select");
    select.setAttribute("class", "verb-features__select");
    select.setAttribute("id", list + "_" + feature);

    var option = document.createElement("option");
    option.setAttribute("value", "question");
    option.innerHTML = "-- " + feature + " --";
    select.appendChild(option);

    var options = featuresHash[feature];

    for (let i = 0; i < options.length; i++) {
        let option = renderOption(options[i]);
        select.appendChild(option);
    }

    var halfOption = document.createElement("option");
    halfOption.setAttribute("value", "half");
    halfOption.innerHTML = "50 / 50";
    select.appendChild(halfOption);

    return select;
}

function renderOption(value) {
    var option = document.createElement("option");
    option.setAttribute("value", value);
    option.innerHTML = value;

    return option;
}

function renderNumericRow(list, feature, rangeHash) {
    var tr = document.createElement("tr");

    var tdName = document.createElement("td");
    tdName.innerHTML = feature;

    var tdRange = document.createElement("td");
    tdRange.innerHTML = 'от <input id="' + list + '_' + feature + '_from" type="number" value="' + rangeHash['min'] + '"><span> до </span><input id="' + list + '_' + feature + '_to" type="number" value="' + rangeHash['max'] + '">';

    tr.appendChild(tdName);
    tr.appendChild(tdRange);

    return tr;
}
