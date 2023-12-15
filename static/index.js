        var currentUserId = '{{user_id}}'; 
        var eventSource = null;

        function sendMessage() {
            var message = document.getElementById("messageInput").value;
            var userId = document.getElementById("userIdInput").value || '{{user_id}}'; 

            fetch('/send_message', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ user_id: userId, messaged_us: message })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("messageInput").value = '';
                addMessageToChat(userId, message, false); 
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        function addMessageToChat(userId, message, isSystemMessage) {
            var chatDiv = document.getElementById('message-display');
            var newMessage = document.createElement('div');
            newMessage.classList.add('message');
            var displayText = isSystemMessage ? `System: ${message}` : `User ${userId}: ${message}`;
            newMessage.textContent = displayText;
            chatDiv.appendChild(newMessage);
        }

        function updateEventSource() {
            if (eventSource) {
                eventSource.close();
            }
            eventSource = new EventSource('/stream/' + currentUserId);

            eventSource.onmessage = function(event) {
                var msgData = JSON.parse(event.data);
                if (msgData.hasOwnProperty('messaged_back')) {
                    var messageText = msgData.messaged_back;
                    addMessageToChat(msgData.user_id, messageText, true);
                }
            };

        }

        document.getElementById('userIdInput').addEventListener('change', function() {
            currentUserId = this.value || '{{user_id}}';
            updateEventSource();
        });

        updateEventSource();
