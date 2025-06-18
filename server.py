from flask import Flask, request, jsonify, render_template_string
import bot
import random

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>MY GPT</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: #f7f7f7;
            min-height: 100vh;
            height: 100vh;
        }
        #main-layout {
            display: flex;
            height: 100vh;
            min-height: 100vh;
        }
        #sidebar {
            width: 220px;
            background: #fff;
            border-right: 1px solid #e0e0e0;
            padding: 24px 0 0 0;
            display: flex;
            flex-direction: column;
            align-items: stretch;
        }
        #sidebar h3 {
            text-align: center;
            margin: 0 0 18px 0;
            font-size: 1.1em;
            color: #4f8cff;
            letter-spacing: 1px;
        }
        #voice-switch-row {
            text-align: center;
            margin-bottom: 18px;
        }
        #voice-switch-row label {
            font-size: 1em;
            color: #444;
            user-select: none;
        }
        #new-chat-btn {
            margin: 0 auto 18px auto;
            display: block;
            background: #4f8cff;
            color: #fff;
            border: none;
            border-radius: 6px;
            padding: 7px 16px;
            font-size: 0.98em;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.2s;
        }
        #new-chat-btn:hover {
            background: #2563eb;
        }
        #history-list {
            flex: 1;
            overflow-y: auto;
            padding: 0 10px;
        }
        .history-item {
            background: #f7faff;
            border-radius: 6px;
            margin-bottom: 8px;
            padding: 8px 10px;
            cursor: pointer;
            transition: background 0.2s;
            border: 1px solid #e0e7ff;
            font-size: 0.98em;
            color: #333;
        }
        .history-item:hover {
            background: #e0e7ff;
        }
        #clear-history {
            margin: 12px auto 20px auto;
            display: block;
            background: #ff6a88;
            color: #fff;
            border: none;
            border-radius: 6px;
            padding: 7px 16px;
            font-size: 0.98em;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.2s;
        }
        #clear-history:hover {
            background: #ff4081;
        }
        #container {
            flex: 1;
            display: flex;
            flex-direction: column;
            height: 100vh;
            max-width: 900px;
            margin: 0 auto;
            background: #fff;
            position: relative;
        }
        h2 {
            text-align: center;
            margin: 18px 0 10px 0;
            color: #2a2a2a;
            font-size: 1.3em;
            letter-spacing: 1.2px;
            font-weight: 700;
        }
        #chat-area {
            flex: 1;
            overflow-y: auto;
            padding: 0 0 16px 0;
            display: flex;
            flex-direction: column;
            gap: 0;
        }
        .message-row {
            display: flex;
            margin: 0 0 0 0;
            padding: 0 18px;
        }
        .message.user {
            justify-content: flex-end;
        }
        .message.bot {
            justify-content: flex-start;
        }
        .bubble {
            max-width: 70%;
            font-size: 1em;
            line-height: 1.7;
            background: none;
            border-radius: 0;
            color: #222;
            box-shadow: none;
            border: none;
            word-break: break-word;
            white-space: pre-line;
            padding: 10px 0;
        }
        .bot .bubble {
            color: #222;
            background: none;
            text-align: left;
        }
        .user .bubble {
            color: #2563eb;
            background: none;
            text-align: right;
        }
        .divider {
            height: 1px;
            background: #f0f0f0;
            margin: 0 0 0 0;
            border: none;
        }
        #input-bar {
            width: 100%;
            background: #fff;
            border-top: 1px solid #e0e0e0;
            padding: 10px 12px 10px 12px;
            position: sticky;
            bottom: 0;
            left: 0;
            z-index: 10;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        input[type=text] {
            flex: 1;
            padding: 10px;
            font-size: 1em;
            border: 1.5px solid #b3b3b3;
            border-radius: 6px;
            outline: none;
            transition: border 0.2s, box-shadow 0.2s;
            background: #fff;
        }
        input[type=text]:focus {
            border: 2px solid #4f8cff;
        }
        button, .mic-btn {
            padding: 8px 14px;
            font-size: 1em;
            border: none;
            border-radius: 6px;
            background: #4f8cff;
            color: #fff;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.2s;
        }
        button:hover, .mic-btn:hover {
            background: #2563eb;
        }
        .mic-btn {
            background: #eaeaea;
            color: #333;
            border: 1.5px solid #b3b3b3;
            padding: 8px 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: none;
            transition: background 0.2s, border 0.2s;
        }
        .mic-btn.listening {
            background: #ff5252;
            color: #fff;
            border-color: #ff5252;
        }
        #loading {
            display: none;
            margin-top: 8px;
            text-align: center;
            color: #4f8cff;
            font-size: 1em;
        }
        @media (max-width: 900px) {
            #main-layout { flex-direction: column; }
            #sidebar { width: 100vw; min-height: 120px; border-right: none; border-bottom: 1px solid #e0e0e0; flex-direction: row; overflow-x: auto; }
            #container { max-width: 99vw; }
            h2 { font-size: 1.1em; }
            #chat-area { padding-right: 0; }
            .bubble { max-width: 90vw; }
            #input-bar { padding: 8px 4px; }
        }
    </style>
</head>
<body>
    <div id="main-layout">
        <div id="sidebar">
            <h3>Chat History</h3>
            <div id="voice-switch-row">
                <label>
                    <input type="checkbox" id="voice_switch" checked style="vertical-align:middle; margin-right:4px;">
                    Voice Mode
                </label>
            </div>
            <button id="new-chat-btn">+ New Chat</button>
            <div id="history-list"></div>
            <button id="clear-history">Clear History</button>
        </div>
        <div id="container">
            <h2>MY GPT</h2>
            <div id="chat-area"></div>
            <div id="loading">Thinking...</div>
            <div id="input-bar">
                <input type="text" id="user_input" placeholder="Ask me anything..." autocomplete="off" autofocus>
                <button onclick="ask()" id="ask_btn">Ask</button>
                <button class="mic-btn" id="mic_btn" title="Speak your question" onclick="startListening()">
                    <svg id="mic_icon" width="22" height="22" viewBox="0 0 24 24">
                        <path fill="currentColor" d="M12 15a3 3 0 0 0 3-3V6a3 3 0 0 0-6 0v6a3 3 0 0 0 3 3zm5-3a1 1 0 1 0-2 0 5 5 0 0 1-10 0 1 1 0 1 0-2 0 7 7 0 0 0 6 6.92V21h2v-2.08A7 7 0 0 0 19 12z"/>
                    </svg>
                </button>
            </div>
        </div>
    </div>
    <script>
        // --- Chat History Logic ---
        let chatHistory = JSON.parse(localStorage.getItem('chatHistory') || '[]');
        let currentChat = [];
        let currentHistoryIndex = null;

        function saveHistory() {
            localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
        }
        function renderHistory() {
            const list = document.getElementById('history-list');
            list.innerHTML = '';
            if (chatHistory.length === 0) {
                list.innerHTML = '<div style="color:#aaa;text-align:center;margin-top:30px;">No history yet</div>';
                return;
            }
            chatHistory.forEach((chat, idx) => {
                const item = document.createElement('div');
                item.className = 'history-item';
                item.innerText = chat[0]?.text?.slice(0, 30) || 'Conversation ' + (idx+1);
                item.onclick = () => loadHistory(idx);
                list.appendChild(item);
            });
        }
        function loadHistory(idx) {
            currentHistoryIndex = idx;
            currentChat = chatHistory[idx].slice();
            renderChat();
        }
        function addToHistory(chat) {
            chatHistory.push(chat);
            if (chatHistory.length > 20) chatHistory.shift();
            saveHistory();
            renderHistory();
        }
        function clearHistory() {
            chatHistory = [];
            saveHistory();
            renderHistory();
        }
        document.getElementById('clear-history').onclick = clearHistory;

        // --- New Chat Logic ---
        document.getElementById('new-chat-btn').onclick = function() {
            if (currentChat.length > 0) {
                addToHistory(currentChat.slice());
            }
            currentChat = [];
            currentHistoryIndex = null;
            renderChat();
        };

        // --- Chat UI Logic ---
        const userInput = document.getElementById('user_input');
        const chatArea = document.getElementById('chat-area');
        const loadingDiv = document.getElementById('loading');
        const micBtn = document.getElementById('mic_btn');
        const voiceSwitch = document.getElementById('voice_switch');
        let recognizing = false;
        let recognition = null;

        function renderChat() {
            chatArea.innerHTML = '';
            (currentChat || []).forEach((msg, idx) => {
                if (idx > 0) {
                    const divider = document.createElement('div');
                    divider.className = 'divider';
                    chatArea.appendChild(divider);
                }
                const row = document.createElement('div');
                row.className = 'message-row ' + msg.role;
                const bubble = document.createElement('div');
                bubble.className = 'bubble';
                if (msg.role === 'bot' && idx === currentChat.length - 1) {
                    typeText(bubble, msg.text);
                } else {
                    bubble.innerText = msg.text;
                }
                row.appendChild(bubble);
                row.classList.add(msg.role);
                chatArea.appendChild(row);
            });
            chatArea.scrollTop = chatArea.scrollHeight;
        }

        // Word-by-word typing animation for bot responses
        function typeText(element, text, i=0) {
            element.innerHTML = '';
            let words = text.split(' ');
            let idx = 0;
            function typeWord() {
                if (idx < words.length) {
                    element.innerHTML += (idx > 0 ? ' ' : '') + words[idx];
                    idx++;
                    chatArea.scrollTop = chatArea.scrollHeight;
                    setTimeout(typeWord, 80 + Math.random()*60);
                }
            }
            typeWord();
        }

        function ask() {
            const user_input = userInput.value.trim();
            if (!user_input) return;
            if (!currentChat) currentChat = [];
            currentChat.push({role: 'user', text: user_input});
            renderChat();
            userInput.value = '';
            loadingDiv.style.display = 'block';
            fetch('/api/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: user_input })
            })
            .then(response => response.json())
            .then(data => {
                loadingDiv.style.display = 'none';
                currentChat.push({role: 'bot', text: data.response});
                renderChat();
                // Save to history if it's a new chat or update current
                if (currentHistoryIndex === null) {
                    addToHistory(currentChat.slice());
                    currentHistoryIndex = chatHistory.length - 1;
                } else {
                    chatHistory[currentHistoryIndex] = currentChat.slice();
                    saveHistory();
                }
            })
            .catch(() => {
                loadingDiv.style.display = 'none';
                currentChat.push({role: 'bot', text: 'Error: Could not get response.'});
                renderChat();
            });
        }

        userInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') ask();
        });

        // Voice recognition
        function startListening() {
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                alert('Sorry, your browser does not support speech recognition.');
                return;
            }
            if (recognizing) {
                recognition.stop();
                return;
            }
            micBtn.classList.add('listening');
            micBtn.title = 'Listening... click to stop';
            userInput.placeholder = 'Listening...';
            loadingDiv.style.display = 'none';

            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.lang = 'en-US';
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;

            recognition.onstart = function() {
                recognizing = true;
            };
            recognition.onresult = function(event) {
                recognizing = false;
                micBtn.classList.remove('listening');
                micBtn.title = 'Speak your question';
                userInput.placeholder = 'Ask me anything...';
                if (event.results && event.results[0] && event.results[0][0]) {
                    const transcript = event.results[0][0].transcript;
                    userInput.value = transcript;
                    ask();
                }
            };
            recognition.onerror = function(event) {
                recognizing = false;
                micBtn.classList.remove('listening');
                micBtn.title = 'Speak your question';
                userInput.placeholder = 'Ask me anything...';
            };
            recognition.onend = function() {
                recognizing = false;
                micBtn.classList.remove('listening');
                micBtn.title = 'Speak your question';
                userInput.placeholder = 'Ask me anything...';
            };
            recognition.start();
        }

        // Voice switch logic
        function updateMicBtn() {
            if (voiceSwitch.checked) {
                micBtn.style.display = '';
            } else {
                micBtn.style.display = 'none';
                if (recognizing && recognition) {
                    recognition.stop();
                }
            }
        }
        voiceSwitch.addEventListener('change', updateMicBtn);
        updateMicBtn(); // Initial call

        // Initial render
        renderHistory();
        if (chatHistory.length > 0) {
            loadHistory(chatHistory.length - 1);
        } else {
            currentChat = [];
            renderChat();
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.get_json()
    message = data.get('message', '')
    if not message.strip():
        return jsonify({'response': "Please enter a message."})
    ints = bot.predict_class(message)
    if ints:
        res = bot.get_response(ints, bot.intents)
    else:
        tag, sim = bot.cosine_intent(message, bot.intents, bot.words)
        if tag is not None and sim > 0.7:
            for i in bot.intents['intents']:
                if i['tag'] == tag:
                    res = random.choice(i['responses'])
                    break
        else:
            res = "Sorry, I didn't understand that."
    return jsonify({'response': res})

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000)