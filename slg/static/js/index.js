function goToParameters() {
    var number_of_lists = document.getElementById("number_of_lists").value;

    window.location.assign('/parameters?n=' + number_of_lists)
}
