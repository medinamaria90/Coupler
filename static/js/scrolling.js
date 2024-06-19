// LIKE AND DISLIKE
document.getElementById('likecircle').addEventListener('click', function() {
    var modal = document.getElementById('popup-container');
    var modalInstance = new bootstrap.Modal(modal);
    modalInstance.show();
    fetch('/like_couple', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ /* datos que desees enviar */ }),
    })
    .then(response => response.json())
    .then(data => {
        // Maneja la respuesta del servidor
        console.log(data.message);
        if (data.match === true) {
            var modal = document.getElementById('popup-container');
            var modalInstance = new bootstrap.Modal(modal);
            modalInstance.show();
        } else if (data.match === false) {
            window.location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

document.getElementById('dislikecircle').addEventListener('click', function() {
    fetch('/dislike_couple', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ /* datos que desees enviar */ }),
    })
    .then(response => response.json())
    .then(data => {
        // Maneja la respuesta del servidor
        console.log(data.message);
        window.location.reload();
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
