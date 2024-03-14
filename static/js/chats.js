

$(document).ready(function(){

    const leftColumn = document.getElementById('left_column')
    const middleColumn = document.getElementById('middle_column')
    const rightColumn = document.getElementById('right_column')
    const chatsDiv = document.querySelectorAll('.chats_div');
    const chatEntry = document.getElementById("chat_entry");
    const messengerHeader = document.getElementById('messenger_header');
    const messengerAvatar = document.getElementById('messenger_avatar')
    const all_content = document.getElementById("all_content");
    const chatBody = document.getElementById('chat_body');
    const user_id = all_content.getAttribute('data-user-id');
    const leftDiv = document.getElementById('left-div');
    const chatCoupleName = document.getElementById('couple_name');
    const messageDate = document.getElementById('message_date');
    const messageInput = document.getElementById('message_input');
    const carousel_tags = document.querySelector('#carousel_tags');
    const carouselInner = document.querySelector('.carousel-inner');
    const carouselIndicators = document.getElementById('carouselIndicators');

    if (window.innerWidth > 992) {
        messengerAvatar.classList.add('no_chats_img');
        chatCoupleName.textContent = '¡Bienvenido a tu app para hacer amigos!';
        messageDate.textContent = 'Recuerda que esta app está en fase de pruebas';
        chatEntry.style.display='none';
    }

    function moveChatDivToTop(chatDiv) {
      leftDiv.prepend(chatDiv);
    }

    var socket = io.connect('https://' + document.domain + ':' + location.port, {
        transports: ['websocket'],
        secure : true
    });
    socket.emit('join_rooms');
    
    // Manejar la respuesta del servidor
    socket.on('get_rooms', function(rooms) {
        console.log('Salas recibidas:', rooms);
    });

    //Hay un mensaje recibido del servidor
    socket.on('message', function(data) {
        console.log(data);
        const match_id = data.match_id;
        const open_chat_match_id = messengerHeader.getAttribute('data-match-id');
        const sender_id = data.sender_id.toString();
        const next_with_photo = messengerHeader.getAttribute('next_with_photo');
        const isMessageFromCurrentUser = sender_id === user_id.toString();

        // Está la conversacion abierta?
        if (match_id === open_chat_match_id) {
            const avatarSrc = messengerAvatar.getAttribute('src');
            let messageContent;
    //      ¿El remitente es distinto que yo? Si soy yo, no debe hacer nada.
            if (isMessageFromCurrentUser === false) {
                if (next_with_photo === 'true') {
                    // Si no eres el remitente y se espera una foto, muestra el mensaje con la foto.
                    messageContent = createReceivedMessage(data.message, avatarSrc);
                } else {
                    // Si no eres el remitente y no se espera una foto, muestra el mensaje sin foto.
                    messageContent = createReceivedMessageNoPhoto(data.message);
                }
                chatBody.appendChild(messageContent);
            }
            chatBody.scrollTop = chatBody.scrollHeight;
    //      Ahora escribimos el mensaje en le resumen a la izquierda de chats
            chatsDiv.forEach(function(chatDiv) {
                const matchId = chatDiv.getAttribute('data-match_id');
    //          Si el match Id del resumen de la izquierda coincide con el de nuestro Header
                if (matchId === match_id) {
                    const lastMessage = chatDiv.querySelector('p.message');
                    if (lastMessage) {
                        console.log("in last message");
                        lastMessage.textContent = data.message;
                        console.log("about to read_message_opened");
                        read_message_opened(matchId);
                        return;
                    }
                    else{
                    console.log("in else")
                    }
                }
            });
        }
        else {
            chatsDiv.forEach(function(chatDiv) {
                const matchId = chatDiv.getAttribute('data-match_id');
                if (matchId === match_id) {
                    const lastMessage = chatDiv.querySelector('p.message');
                    if (lastMessage) {
                        lastMessage.textContent = data.message;
                        lastMessage.classList.add("bold_text");
                        if (chatDiv.getAttribute('new_message') !== "true") {
                            add_new_message(chatDiv);
                            moveChatDivToTop(chatDiv);
                        }
                        return;
                    }
                }
            });
        }
    });

    //ENVIAR MENSAJE
    var messageInputJquery = $("#message_input");
     $('#send-button').click(sendMessage);

    // Agregar evento de teclado para el campo de entrada
    messageInputJquery.keydown(function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });

    function sendMessage() {
        chatBody.focus();
        var messageText = messageInputJquery.val();
        const open_chat_match_id = messengerHeader.getAttribute('data-match-id');
        const first_message = messengerHeader.getAttribute('first_message');
        if (messageText.trim() !== "") {
        messageDiv = createSentMessage(messageText)
        chatBody.append(messageDiv);
        const textArea = chatEntry.querySelector("textarea");
        textArea.value="";

        // Luego, añade ese mensaje al panel de la izquierda
        chatsDiv.forEach(function(chatDiv) {
            if (chatDiv.getAttribute("data-match_id") === open_chat_match_id) {
                chatDiv.querySelector('p').textContent = "Tú: " + messageText;
                moveChatDivToTop(chatDiv);
            }
        });

    chatBody.scrollTop = chatBody.scrollHeight;
    //    Aqui es cuando lo enviamos al servidor
    socket.emit('message', {
        message: messageText,
        match_id: open_chat_match_id,
        first_message: first_message
    });
    }}

    function callFlaskEndpoint(avatarSrc, matchId) {
        fetch(`/retrieve_chats?match_id=${matchId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('La solicitud no fue exitosa');
                }
                return response.json();
            })
            .then(data => {
                if (data.resultado === 'correcto') {
                    // Accede al objeto "chat" desde la respuesta JSON
                    const chats = data.chats;
                    const profile_photos = data.profile_photos;
                    const pareja = data.pareja;
                    const tags = data.pareja_activa_tags;
                    // LLAMAMOS A LAS FUNCIONES CORRESPONDIENTES
                    generateChatMessages(chats, avatarSrc, matchId);
                    update_carousel_info(profile_photos);
                    update_profile_info(pareja, tags);
                } 
                else {
                    console.error('Error al recuperar el chat:', data.mensaje);
                }
            })
            .catch(error => {
                console.error('Error al llamar al endpoint', error);
            });
    }

    function get_messenger_data(clickedDiv, history=false) {
        // Eliminar la clase "selected-chat" de todos los divs de chat
        // Obtener el matchId
        const matchId = clickedDiv.getAttribute('data-match_id');
        // Actualizar el messenger_header
        messengerHeader.setAttribute('data-match-id', matchId);
        // Obtener la fuente del avatar y actualizar la imagen
        const avatarSrc = clickedDiv.querySelector('.match_img').getAttribute('src');
        messengerAvatar.src = avatarSrc;
        // Obtener los nombres y edades de la pareja
        const matchesNamesDiv = clickedDiv.querySelector('.data_div');
        const name1 = matchesNamesDiv.getAttribute('data-name1');
        const name2 = matchesNamesDiv.getAttribute('data-name2');
        const age1 = matchesNamesDiv.getAttribute('data-age1');
        const age2 = matchesNamesDiv.getAttribute('data-age2');
        // Actualizar los nombres en el HTML
        chatCoupleName.textContent = `${name1} (${age1}) y ${name2} (${age2})`;
        if (history === false){
        // Obtener la fecha y mostrarla
        const fecha = "Conectásteis " + clickedDiv.getAttribute('data-match_date');
        messageDate.textContent = fecha;
        messengerHeader.setAttribute('first_message', true);
        }
        if (history === true){
        // Obtener la fecha y mostrarla
        const fecha = "Último mensaje " + clickedDiv.getAttribute('chat_date');
        messageDate.textContent = fecha;}
        // Vaciar el cuerpo del chat y el área de texto
        chatBody.innerHTML = '';
        messageInput.value = '';

        // Verificar el tamaño de la pantalla y hacer cambios en el diseño si es necesario
        if (window.innerWidth < 992) {
            chatBody.focus();
            leftColumn.style.display = 'none';
            middleColumn.style.display="block"
            document.querySelector('.navbar-toggler').style.display = 'none';
            document.querySelector("#back_to_chats").style.display = 'block';
        }
        return { avatarSrc, matchId };
    }

    function read_message_opened(matchId){
        console.log(matchId);
        fetch('/last_chat_read', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ matchId: matchId }),
        })
    }

    function read_message(chatDiv){
        console.log("I am trying to make it seem read")
        if (chatDiv.querySelector("div.circle")) {
          chatDiv.querySelector("div.circle").style.display = "none";
        }
        if (chatDiv.querySelector("p.bold_text")) {
          chatDiv.querySelector("p.bold_text").classList.remove('bold_text');
        }
        if (chatDiv.classList.contains("new_message")) {
          chatDiv.classList.remove('new_message');
        }
        const chat_id = chatDiv.getAttribute("chat_id");
        console.log("about to tell the server it has been read");
        fetch('/message_read', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ chat_id: chat_id }),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('La solicitud no fue exitosa');
                }
                return response.json(); // Parse the response as JSON
            })
            .then(data => {
                if (data.resultado === 'correcto') {
                    console.log("done");
                } else {
                    console.error('Error al recuperar la respuesta:', data.mensaje);
                }
            })
            .catch(error => {
                console.error('Error al llamar al endpoint', error);
            });
    }

    function add_new_message(chatDiv){
        if (chatDiv.querySelector(".circle")){
        chatDiv.querySelector(".circle").remove();
        };
        const circleDiv = document.createElement('div');
        circleDiv.classList.add('circle'); // Puedes agregar una clase para aplicar estilos
        chatDiv.classList.add('new_message'); // Puedes agregar una clase para aplicar estilos
        // Agrégalo al chatDiv
        chatDiv.appendChild(circleDiv);
    }

    //¿Se clica en un match o en un chat?
    document.addEventListener('click', function(event) {
        let messengerData = null;
        const target = event.target;
        // Verificar si el clic ocurrió en un elemento con la clase "every_match_div"
        if  (target.closest('.match_img')) {
            chatEntry.style.display='flex'
            middleColumn.style.display='flex';
            // Eliminar la clase "selected-chat" de todos los divs de chat
            chatsDiv.forEach(div => div.classList.remove('selected-chat'));
            const matchDiv = target.parentNode.parentNode;
            messengerData = get_messenger_data(matchDiv);
        }
        else if  (target.closest('.chats_div')) {
                chatEntry.style.display='flex'
                const chatDiv = target.closest('.chats_div');
                chatsDiv.forEach(div => div.classList.remove('selected-chat'));
                chatDiv.classList.add("selected-chat");
                messengerData = get_messenger_data(chatDiv, history=true);
                middleColumn.style.display='flex';
                if (chatDiv.classList.contains('new_message')){
                console.log("i am going to call read_message func");
                read_message(chatDiv)
                }
        }
    //    LLamar al carousel con los datos obtenidos
        if(messengerData){
            callFlaskEndpoint(messengerData.avatarSrc, messengerData.matchId);
            }
    });

    //Ahora introducimos las funciones necesarias para generar los mensajes en el chat
    function createSentMessage(message) {
        messengerHeader.setAttribute('next_with_photo', true);
        const sentMessageDiv = document.createElement('div');
        sentMessageDiv.classList.add('user_chat', );
        sentMessageDiv.innerHTML = `
            <div class="sent_msj">
                <p class="messenger_text sent">${message}</p>
            </div>
        `;
        return sentMessageDiv;
    }

    // Función para generar la estructura de un mensaje recibido
    function createReceivedMessage(message, avatarSrc) {
        messengerHeader.setAttribute('next_with_photo', false);
        const receivedMessageDiv = document.createElement('div');
        receivedMessageDiv.classList.add('received_msj_div');
        receivedMessageDiv.innerHTML = `
            <img class="messenger_avatar chatting_avatar"
                 src="${avatarSrc}">
            <div class="received_msj_content">
                <p class="messenger_text">${message}</p>
            </div>
        `;
        return receivedMessageDiv;
    }

    function createReceivedMessageNoPhoto(message, avatarSrc) {
        const receivedMessageDiv = document.createElement('div');
        receivedMessageDiv.classList.add('received_msj_div');
        receivedMessageDiv.innerHTML = `
            <div class="received_msj_content no_photo">
                <p class="messenger_text">${message}</p>
            </div>
        `;
        return receivedMessageDiv;
    }

    // Función para procesar los chats y generar la estructura de mensajes en el HTML
    function generateChatMessages(chats, avatarSrc) {
        chatBody.innerHTML = '';
        let prevChatIsSent = true;
        for (const chat of chats) {
            const { sent, message } = chat;
            if (sent) {
                chatBody.appendChild(createSentMessage(message));
            } else if (prevChatIsSent) {
                chatBody.appendChild(createReceivedMessage(message, avatarSrc));
            } else {
                chatBody.appendChild(createReceivedMessageNoPhoto(message));
            }
            prevChatIsSent = sent;
        chatBody.scrollTop = chatBody.scrollHeight;
        }
    }

    function update_profile_info(pareja, tags){
    //    UPDATING NAMES
        carousel_tags.innerHTML = '';
        const carousel_couples_name = document.querySelector('#carousel_couples_name');
    //    UPDATING TAGS
        const carousel_couple_info = document.querySelector('.preview_content');
        tags.forEach((tag, index) => {
            const carousel_tag = document.createElement('span');
            carousel_tag.classList.add('badge', 'rounded-pill', 'bg-primary', 'personalized_badge')
            carousel_tag.textContent=tag;
            carousel_tags.appendChild(carousel_tag)
        }
        )
    //    UPDATING COUPLE_INFO
        const couple_description_content = document.querySelector('#couple_description_content');
        couple_description_content.innerHTML = '';
        const couple_description = document.createElement('p');
        couple_description.classList.add('couple_description_text');
        couple_description.textContent=pareja["couple_description"]
        couple_description_content.appendChild(couple_description);
    }

    function update_carousel_info(profile_photos) {
       // Obtén el elemento con la clase "carousel-inner" para actualizar el contenido
       // Limpia el contenido actual del carrousel
       carouselInner.innerHTML = '';
       // Itera sobre las fotos en profile_photos y crea elementos para cada una
       profile_photos.forEach((photo, index) => {
          const carouselItemDiv = document.createElement('div');
          carouselItemDiv.classList.add('carousel-item');
          if (index === 0) {
             carouselItemDiv.classList.add('active');
          }
          const imgElement = document.createElement('img');
          imgElement.alt = 'Photo';
          imgElement.classList.add('carousel_photo');
          imgElement.src = `/serve_upload/${photo}`;
          // Agrega la imagen al elemento del carrousel
          carouselItemDiv.appendChild(imgElement);
          // Agrega el elemento del carrousel al elemento "carousel-inner"
          carouselInner.appendChild(carouselItemDiv);
       });

       // Limpia el contenido actual de los indicadores
       carouselIndicators.innerHTML = '';
       // Crea botones según la cantidad de fotos en profile_photos
       for (let i = 0; i < profile_photos.length; i++) {
       const button = document.createElement('button');
       button.setAttribute('aria-label', `Slide ${i + 1}`);
       if (i === 0) {
          button.classList.add('active');
       }
       button.setAttribute('data-bs-slide-to', i);
       button.setAttribute('data-bs-target', '#carouselExampleIndicators');
       button.setAttribute('type', 'button');
       carouselIndicators.appendChild(button);
        }
    }

    if (window.innerWidth < 992) {
            middleColumn.style.display="none"
            rightColumn.style.display="none"
            const backToChats = document.getElementById("back_to_chats");
            const backToMessenger = document.getElementById("back_to_messenger");
            // Delegación de eventos para elementos similares (avatares)
            document.body.addEventListener('click', function (event) {
    //Si clicamos en uno de los matches de la izquierda, el evento esta mas arriba
    //,en esta misma pagina, con el listener del click
                if (event.target.classList.contains('messenger_avatar')) {
                    // Ocultar la segunda columna (chat)
                    middleColumn.style.display = 'none';
                    rightColumn.style.display = 'block';
                    backToMessenger.style.display='block'
                    backToChats.style.display='none'
                }
            });

            // Manejar el botón "Ir atrás" para volver al resumen de chats
            backToChats.addEventListener('click', function () {
                document.getElementById("chat_body").focus();
                backToChats.style.display='none';
                // Mostrar la primera columna
                setTimeout(function () {
                // Restablecer la primera columna
                leftColumn.style.display = 'block';
                }, 100);
                middleColumn.style.display = 'none';
            });
            // Manejar el botón "Ir atrás" para volver al messenger
            backToMessenger.addEventListener('click', function () {
                rightColumn.style.display = 'none';
                middleColumn.style.display = 'block';
                backToMessenger.style.display='none';
                backToChats.style.display='block';
            });
        }
});
