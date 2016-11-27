function goToParameters() {
    // console.log('foo');

    $.getJSON('/_read_data_file', {

    }, function(data) {
        var result = data.result;

        if (result['success'] == 'success') {
            var number_of_lists = document.getElementById("number_of_lists").value;
            window.location.assign('/parameters?n=' + number_of_lists);
        } else {
            // console.log(result['error']);

            var error = document.getElementById('error');
            error.innerHTML = result['error'];

            showSuccessMessage();
        }
    });
}

function showSuccessMessage() {
    var modal = document.getElementById('successMessage');
    modal.style.display = "block";
}

function hideSuccessMessage() {
    var modal = document.getElementById('successMessage');
    modal.style.display = "none";
}
