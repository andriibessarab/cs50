document.addEventListener('DOMContentLoaded', () => {

    // SOCKET DECLARE
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    //ONLOAD
    onload();

    //SET USER
    document.querySelector('#set_name').onsubmit = () => {
        const request = new XMLHttpRequest();
        request.open('POST', '/add_user');
        request.onload = () => {
            data = JSON.parse(request.responseText);
            if (data['valid']) {
                const username = document.querySelector('#username').value;
                localStorage.setItem('user', username);
                location.reload();
            }
            else {
                alert('This username is not available. Try a differen one!');
            }
        }
        const info = new FormData();
        info.append('username', document.querySelector('#username').value);
        request.send(info);
        return false;
    }

    //OPEN/CLOSE "CREATE NEW CHANNEL" FORM
    document.querySelector('#create_new_channel_open_button').onclick = () => {
        document.querySelector('#create_new_channel_open_button').style.display = 'none';
        document.querySelector('#create_new_channel_div').style.display = 'block';
    };

    document.querySelector('#create_new_channel_close_button').onclick = () => {
        document.querySelector('#create_new_channel_open_button').style.display = 'block';
        document.querySelector('#channel_name').value = '';
        document.querySelector('#create_new_channel_div').style.display = 'none';
    };

    //CHANGE COLOR OF SITE
    document.querySelector('#blue').onclick = () => {
        set_color('blue');
        localStorage.setItem('color', 'blue');
    }

    document.querySelector('#green').onclick = () => {
        set_color('green');
        localStorage.setItem('color', 'green');
    }

    document.querySelector('#orange').onclick = () => {
        set_color('orange');
        localStorage.setItem('color', 'orange');
    }

    //LOG OUT
    document.querySelector('#log_out').onclick = () => {
        if (confirm('If you will log out, you will not be able to log in again with the same username. Are you sure?') === true) {
            localStorage.removeItem('user');
            location.reload();
        }
    }


    //SOCKET IO

    //SOCKETIO ON CONNECT
    socket.on('connect', () => {

        //CREATE NEW CHANNEL
        document.querySelector('#create_new_channel_form').onsubmit = () => {
            const request = new XMLHttpRequest();
            request.open('POST', '/create_channel');
            request.onload = () => {
                data = JSON.parse(request.responseText);
                if (data['valid']) {
                    socket.emit('new channel added');
                    document.querySelector('#create_new_channel_open_button').style.display = 'block';
                    document.querySelector('#channel_name').value = '';
                    document.querySelector('#create_new_channel_div').style.display = 'none';
                    alert('Channel has been successfully added!');
                }
                else {
                    alert('A channel with this name is already exist. Try a differen one!');
                }
            }
            const info = new FormData();
            info.append('channel_name', document.querySelector('#channel_name').value);
            request.send(info);
            document.querySelector('#channel_name').innerHTML = '';
            return false;
        }

        //ADD MESSAGE
        document.querySelector('#add_message').onsubmit = () => {
            //CHECK IF USER IS ON A CHANNEL
            if (localStorage.getItem('channel') === null) {
                alert('Select a channel where you want to send a message!');
                return false;
            }
            //DECLARE NEW FORM DATA
            const data = new FormData();
            //CHECK WHAT DATA HAS BEEN SEND
            if (document.querySelector('#message_input').value === '' && document.querySelector('#file_input').files[0] === undefined) {
                alert('Please fill out at least one field!');
                return false;
            } else if (document.querySelector('#message_input').value !== '' && document.querySelector('#file_input').files[0] === undefined) {
                data.append('type', '10');
                data.append('message', document.querySelector('#message_input').value);
            } else if (document.querySelector('#message_input').value === '' && document.querySelector('#file_input').files[0] !== undefined) {
                data.append('type', '01');
                data.append('image', document.querySelector('#file_input').files[0]);
            } else if (document.querySelector('#message_input').value !== '' && document.querySelector('#file_input').files[0] !== undefined) {
                data.append('type', '11');
                data.append('message', document.querySelector('#message_input').value);
                data.append('image', document.querySelector('#file_input').files[0]);
            }
            //DEFINE FUNCTION WHICH CHECKS IF I NEED TO DELETE THE OLDEST MESSAGE
            need_to_delete();
            //GETTING TIME
            const today = new Date();
            const date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
            const time = today.getHours() + ':' + today.getMinutes() + ':' + today.getSeconds();
            //MAKING REQUEST
            const request = new XMLHttpRequest();
            request.open('POST', '/add_message');
            request.onload = () => {
                //SENDING SOCKET TO REFRESH THE CHANNEL
                socket.emit('new message added', { 'channel': localStorage.getItem('channel') });
            }
            //GIVING DATA FOR AJAX REQUEST
            data.append('channel', localStorage.getItem('channel'));
            data.append('author', localStorage.getItem('user'));
            data.append('date', date);
            data.append('time', time);
            data.append('need_to_delete', need_to_delete());
            //SENDING REQUEST
            request.send(data);
            //CLEARING INPUTS
            document.querySelector('#message_input').value = '';
            document.querySelector('#file_input').value = '';
            return false;
        }

    });

    //SOCKETIO REFRESH CHANNELS
    socket.on('refresh channels', () => {
        get_channels();
        if (localStorage.getItem('channel') !== null) {
            open_channel(localStorage.getItem('channel'));
        }
    });

    //SOCKETIO REFRESH CHANNEL
    socket.on('refresh channel', data => {
        if (localStorage.getItem('channel') === data['channel']) {
            open_channel(localStorage.getItem('channel'));
        }
        else {
            return;
        }
    });


    //FUNCTIONS

    //ONLOAD FUNCTION
    function onload() {
        //SET COLOR OF WEB PAGE
        if (localStorage.getItem('color') !== null) {
            set_color(localStorage.getItem('color'));
        }
        else {
            set_color('blue');
        }
        //CHECK IF USER LOGGED IN
        if (localStorage.getItem('user') === null) {
            document.querySelector('#unauthorized').style.display = 'flex';
            document.querySelector('#authorized').style.display = 'none';
        }
        else {
            //WHICH PAGE TO DISPLAY
            document.querySelector('#unauthorized').style.display = 'none';
            document.querySelector('#authorized').style.display = 'block';
            document.querySelector('#create_new_channel_div').style.display = 'none';
            //DISPLAY LOG OUT BUTTON
            const logout_button = document.createElement('button');
            logout_button.setAttribute('id', 'log_out');
            logout_button.innerHTML = 'Log Out';
            document.querySelector('#logout_container').appendChild(logout_button);
            //GET ALL CHANNELS
            get_channels();
            //DISPLAY USER'S USERNAME
            const username = document.createElement('p');
            username.setAttribute('id', 'display_username');
            username.innerHTML = `Username: ${localStorage.getItem('user')}`;
            document.querySelector('#display_username_container').appendChild(username);
            //DISPLAY USER A CHANNEL HE'VE BEEN ON LAST TIME
            if (localStorage.getItem('channel') !== null) {
                open_channel(localStorage.getItem('channel'));
            }
        }
    }

    //GET CHANNELS FUNCTION
    function get_channels() {
        const request = new XMLHttpRequest();
        request.open('POST', '/get_channels');
        request.onload = () => {
            const data = JSON.parse(request.responseText);
            const channels = data['channels'];
            document.querySelector('#all_channels').innerHTML = '';
            for (channel in channels) {
                const channel_name = document.createElement('button');
                channel_name.innerHTML = channel;
                channel_name.setAttribute('onclick', `open_channel('${channel}')`);
                document.querySelector('#all_channels').appendChild(channel_name);
            }
        }
        request.send();
    }

    //GET MESSAGES FUNCTION
    function open_channel(channel) {
        const request = new XMLHttpRequest();
        request.open('POST', '/get_messages');
        request.onload = () => {
            const data = JSON.parse(request.responseText);
            const messages = data['messages'];
            document.querySelector('#channel_content').innerHTML = '';
            const channel_name = document.createElement('h2');
            channel_name.innerHTML = channel;
            document.querySelector('#channel_content').appendChild(channel_name);
            if (messages.length === 0) {
                note = document.createElement('p');
                note.innerHTML = 'No messages yet!';
                document.querySelector('#channel_content').appendChild(note);
                return;
            }
            for (message in messages) {
                if (messages[message][0] === '11') {
                    const text = messages[message][1];
                    const image = messages[message][2];
                    const author = messages[message][3];
                    const date = messages[message][4];
                    const time = messages[message][5];
                    const message_container = document.createElement('div');
                    message_container.setAttribute('class', 'message_container');
                    const message_p = document.createElement('p');
                    message_p.innerHTML = `<span class="bold">${author}</span><br>${text}<br><img class="image" src="./static/files/${image}"><br><span class="time_mark">${date} ${time}</span>`;
                    message_container.appendChild(message_p);
                    document.querySelector('#channel_content').appendChild(message_container);
                }
                if (messages[message][0] === '10') {
                    const text = messages[message][1];
                    const author = messages[message][2];
                    const date = messages[message][3];
                    const time = messages[message][4];
                    console.log(text, author, date, time);
                    const message_container = document.createElement('div');
                    message_container.setAttribute('class', 'message_container');
                    const message_p = document.createElement('p');
                    message_p.innerHTML = `<span class="bold">${author}</span><br>${text}<br><span class="time_mark">${date} ${time}</span>`;
                    message_container.appendChild(message_p);
                    document.querySelector('#channel_content').appendChild(message_container);
                }
                if (messages[message][0] === '01') {
                    const image = messages[message][1];
                    const author = messages[message][2];
                    const date = messages[message][3];
                    const time = messages[message][4];
                    console.log(image, author, date, time);
                    const message_container = document.createElement('div');
                    message_container.setAttribute('class', 'message_container');
                    const message_p = document.createElement('p');
                    message_p.innerHTML = `<span class="bold">${author}</span><br><img class="image" src="./static/files/${image}"><br><span class="time_mark">${date} ${time}</span>`;
                    message_container.appendChild(message_p);
                    document.querySelector('#channel_content').appendChild(message_container);
                }
            }
        }
        const info = new FormData();
        info.append('channel', channel);
        request.send(info);
        localStorage.setItem('channel', channel);
    }

    //NEED TO DELETE FUNCTION
    function need_to_delete() {
        var numOfMessages = document.querySelectorAll('.message_container').length;
        if (numOfMessages > 99) {
            return true;
        }
        else {
            return false;
        }
    }
    //SET COLOR FUNCTION
    function set_color(color) {
        var light;
        var dark;
        if (color === 'blue') {
            light = 'rgb(0, 172, 230)';
            dark = 'rgb(0, 115, 153)';
        }
        if (color === 'green') {
            light = 'rgb(0, 204, 0)';
            dark = 'rgb(0, 128, 0)';
        }
        if (color === 'orange') {
            light = 'rgb(255, 153, 0)';
            dark = 'rgb(179, 107, 0)';
        }
        document.querySelector('header').setAttribute('style', `background-image: linear-gradient(to right, ${light}, ${dark});`);
        document.querySelector('#all_channels_section').setAttribute('style', `background-image: linear-gradient(to bottom, ${light}, ${dark});`);
        document.querySelector('#set_name').setAttribute('style', `background-color: ${light};`);
    }
});