document.addEventListener('DOMContentLoaded', () => {
    
    // //Connect to websocket
    // var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // //When connected, request for data every second
    // socket.on('connect', () => {
    //     setInterval(requestData(), 1000);
    // });

    // //Request to flask all information 
    // function requestData(){
    //     socket.emit('all data', '12');
    // }

    // //Receive data from the server
    // socket.on('all data', function (msg) {
    //     document.querySelector('#counter').innerHTML = msg;
    // });
});