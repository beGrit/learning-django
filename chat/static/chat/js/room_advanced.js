window.onload = function (e) {
    const user = JSON.parse(document.querySelector('#user-info').textContent)
    const roomName = JSON.parse(document.querySelector('#room-name').textContent);
    const msgHistory = document.querySelector('.msg_history');

    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/solo/'
        + roomName
        + '/'
    );

    // Append value to the textarea.
    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        if ('content' in document.createElement('template')) {
            let template = document.querySelector('#outgoing_msg_template');
            if (data['type'] === 'outgoing') {
                template = document.querySelector('#outgoing_msg_template');
                let rootNode = template.content.querySelector('.outgoing_msg');
                rootNode.querySelector('.sent_msg p').textContent = data['msg_data']['data'];
                rootNode.querySelector('.sent_msg .time_date').textContent = data['datetime']['data'];
            } else if (data['type'] === 'incoming') {
                template = document.querySelector('#incoming_msg_template');
                let rootNode = template.content.querySelector('.incoming_msg');
                rootNode.querySelector('.incoming_msg_img img').setAttribute('src', '/static' + data['user']['avatar_path']);
                rootNode.querySelector('.received_msg .received_withd_msg p').textContent = data['msg_data']['data'];
                rootNode.querySelector('.received_msg .received_withd_msg .time_date').textContent = data['datetime']['data'];
            }
            let clone = document.importNode(template.content, true);
            msgHistory.appendChild(clone);
        }
    };

    chatSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function (e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };

    document.querySelector('#chat-message-submit').onclick = (e) => {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message,
            'user': user,
        }));
        messageInputDom.value = '';
    };
}