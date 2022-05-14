window.onload = function (e) {
    const current_user_id = JSON.parse(document.querySelector('#current-user-id').textContent)
    const chat_room_id = JSON.parse(document.querySelector('#chat-room-id').textContent)
    const msg_history = document.querySelector('.msg_history')
    const room_type = JSON.parse(document.querySelector('#room-type').textContent)
    const solo_chat_socket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + room_type
        + '/'
        + chat_room_id
        + '/'
    )

    // Append value to the textarea.
    solo_chat_socket.onmessage = function (e) {
        let div = document.createElement('div')
        e.data.text().then(text => {
            console.log(text)
            div.innerHTML = text
        })
        msg_history.appendChild(div)
    };

    solo_chat_socket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly')
    };

    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function (e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click()
        }
    };

    document.querySelector('#chat-message-submit').onclick = (e) => {
        const message_input_elm = document.querySelector('#chat-message-input')
        const message = message_input_elm.value
        // Send message to the server.
        solo_chat_socket.send(JSON.stringify({
            'message': message,
            'user_id': current_user_id,
            'chat_room_id': chat_room_id,
        }));
        // Send success, reset the input value.
        message_input_elm.value = ''
    };
}