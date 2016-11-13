function getUrl(url, dict) {
    url += "?";
    for (let key in dict) {
        url += key + "=" + dict[key] + "&";
    }
    return url.substring(0, url.length-1)
}

function getValuesFromUrl() {
    let tail = window.location.href.split("?");
    if (tail.length > 1) {
        let variables = tail[1].split("&");
        let args = {};
        for (let i = 0; i < variables.length; i++) {
            let key_value = variables[i].split("=");
            args[key_value[0]] = key_value[1];
        }
        return args
    } else {
        return {}
    }
}