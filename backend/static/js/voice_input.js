(function () {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    function setStatus(statusEl, message) {
        if (statusEl) {
            statusEl.textContent = message;
        }
    }

    function setButtonState(buttonEl, label, disabled = false) {
        if (!buttonEl) return;
        buttonEl.textContent = label;
        buttonEl.disabled = disabled;
    }

    window.initVoiceInput = function initVoiceInput({ textareaId, buttonId, statusId, language = 'en-US' }) {
        const textareaEl = document.getElementById(textareaId);
        const buttonEl = document.getElementById(buttonId);
        const statusEl = document.getElementById(statusId);

        if (!textareaEl || !buttonEl || !statusEl) {
            return;
        }

        if (!SpeechRecognition) {
            setButtonState(buttonEl, '🎤 Voice Not Supported', true);
            setStatus(statusEl, 'Voice: Not supported in this browser');
            return;
        }

        const recognition = new SpeechRecognition();
        recognition.lang = language;
        recognition.interimResults = true;
        recognition.continuous = true;

        let listening = false;

        recognition.onstart = function () {
            listening = true;
            setButtonState(buttonEl, '🛑 Stop Voice Input');
            setStatus(statusEl, 'Voice: Listening...');
        };

        recognition.onresult = function (event) {
            let transcript = '';
            for (let i = event.resultIndex; i < event.results.length; i += 1) {
                transcript += event.results[i][0].transcript;
            }

            if (transcript.trim().length > 0) {
                const spacer = textareaEl.value.trim().length > 0 ? ' ' : '';
                textareaEl.value = `${textareaEl.value}${spacer}${transcript.trim()}`;
                textareaEl.dispatchEvent(new Event('input'));
            }
        };

        recognition.onerror = function () {
            setStatus(statusEl, 'Voice: Error detected, try again');
        };

        recognition.onend = function () {
            listening = false;
            setButtonState(buttonEl, '🎤 Start Voice Input');
            setStatus(statusEl, 'Voice: Off');
        };

        buttonEl.addEventListener('click', function () {
            if (!listening) {
                recognition.start();
            } else {
                recognition.stop();
            }
        });
    };
})();
