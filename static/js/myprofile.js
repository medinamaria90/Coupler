
//Removing pics script
function deletePicture(photoUrl, endpoint) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', endpoint, true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    // Encode the 'photoUrl' as a query parameter
    var data = "photoUrl=" + encodeURIComponent(photoUrl);

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                var scrollPosition = window.scrollY;
                location.reload();
                window.scrollTo(0, scrollPosition);
            } else {
                alert("Error: " + xhr.status);
            }
        }
    };
    // Send the data as the request body
    xhr.send(data);
}
