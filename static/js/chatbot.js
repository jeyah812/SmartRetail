document.addEventListener("DOMContentLoaded", function () {


    // ============================================================
    // ELEMENTS
    // ============================================================

    const toggle =
        document.getElementById("chatbot-toggle");

    const close =
        document.getElementById("chatbot-close");

    const chatbot =
        document.getElementById("chatbot-window");

    const input =
        document.getElementById("chatbot-input");

    const send =
        document.getElementById("chatbot-send");

    const messages =
        document.getElementById("chatbot-messages");

    const typing =
        document.getElementById("chatbot-typing");


    // ============================================================
    // SAFETY CHECK
    // ============================================================

    if (
        !toggle ||
        !close ||
        !chatbot ||
        !input ||
        !send ||
        !messages ||
        !typing
    ) {

        return;

    }


    // ============================================================
    // CONVERSATION
    // ============================================================

    let conversation = [];



    // ============================================================
    // OPEN CHATBOT
    // ============================================================

    toggle.addEventListener(
        "click",
        function () {

            chatbot.classList.toggle(
                "chatbot-open"
            );


            if (
                chatbot.classList.contains(
                    "chatbot-open"
                )
            ) {

                setTimeout(
                    function () {

                        input.focus();

                    },
                    250
                );

            }

        }
    );



    // ============================================================
    // CLOSE CHATBOT
    // ============================================================

    close.addEventListener(
        "click",
        function () {

            chatbot.classList.remove(
                "chatbot-open"
            );

        }
    );



    // ============================================================
    // SEND BUTTON
    // ============================================================

    send.addEventListener(
        "click",
        sendMessage
    );



    // ============================================================
    // ENTER KEY
    // ============================================================

    input.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Enter"
            ) {

                event.preventDefault();

                sendMessage();

            }

        }
    );



    // ============================================================
    // SEND MESSAGE
    // ============================================================

    async function sendMessage() {


        const message =
            input.value.trim();


        if (!message) {

            return;

        }


        // --------------------------------------------------------
        // USER MESSAGE
        // --------------------------------------------------------

        addMessage(
            message,
            "user"
        );


        input.value = "";

        input.disabled = true;

        send.disabled = true;


        // --------------------------------------------------------
        // TYPING INDICATOR
        // --------------------------------------------------------

        typing.classList.add(
            "typing-visible"
        );


        scrollToBottom();


        try {


            // ----------------------------------------------------
            // REQUEST
            // ----------------------------------------------------

            const response =
                await fetch(
                    "/chatbot",
                    {

                        method: "POST",

                        headers: {

                            "Content-Type":
                                "application/json"

                        },

                        body:
                            JSON.stringify({

                                message:
                                    message,

                                conversation:
                                    conversation

                            })

                    }
                );


            const data =
                await response.json();


            typing.classList.remove(
                "typing-visible"
            );


            // ----------------------------------------------------
            // SUCCESS
            // ----------------------------------------------------

            if (data.success) {


                addMessage(

                    data.response,

                    "bot"

                );


                conversation.push({

                    role: "user",

                    content:
                        message

                });


                conversation.push({

                    role: "assistant",

                    content:
                        data.response

                });


            }

            else {


                addMessage(

                    data.error ||
                    "I couldn't process that request.",

                    "bot"

                );

            }


        }

        catch (error) {


            console.error(
                "Chatbot error:",
                error
            );


            typing.classList.remove(
                "typing-visible"
            );


            addMessage(

                "⚠️ I couldn't connect to SmartRetail AI right now.",

                "bot"

            );

        }


        // --------------------------------------------------------
        // RESTORE INPUT
        // --------------------------------------------------------

        input.disabled = false;

        send.disabled = false;

        input.focus();

        scrollToBottom();

    }



    // ============================================================
    // ADD MESSAGE
    // ============================================================

    function addMessage(
        text,
        type
    ) {


        const wrapper =
            document.createElement(
                "div"
            );


        wrapper.classList.add(
            "chat-message"
        );


        // --------------------------------------------------------
        // USER
        // --------------------------------------------------------

        if (
            type === "user"
        ) {


            wrapper.classList.add(
                "user-message"
            );


            wrapper.innerHTML = `

                <div class="message-bubble">

                    ${formatMessage(text)}

                </div>

            `;

        }


        // --------------------------------------------------------
        // BOT
        // --------------------------------------------------------

        else {


            wrapper.classList.add(
                "bot-message"
            );


            wrapper.innerHTML = `

                <div class="message-avatar">

                    <i class="bi bi-robot"></i>

                </div>

                <div class="message-bubble">

                    ${formatMessage(text)}

                </div>

            `;

        }


        messages.appendChild(
            wrapper
        );


        scrollToBottom();

    }



    // ============================================================
    // FORMAT AI RESPONSE
    // ============================================================

    function formatMessage(text) {


        if (!text) {

            return "";

        }


        let formatted =
            escapeHTML(text);


        // --------------------------------------------------------
        // BOLD
        // --------------------------------------------------------

        formatted =
            formatted.replace(

                /\*\*(.*?)\*\*/g,

                "<strong>$1</strong>"

            );


        // --------------------------------------------------------
        // HEADINGS
        // --------------------------------------------------------

        formatted =
            formatted.replace(

                /^### (.*?)$/gm,

                "<div class='chat-heading'>$1</div>"

            );


        formatted =
            formatted.replace(

                /^## (.*?)$/gm,

                "<div class='chat-heading'>$1</div>"

            );


        formatted =
            formatted.replace(

                /^# (.*?)$/gm,

                "<div class='chat-heading'>$1</div>"

            );


        // --------------------------------------------------------
        // BULLET POINTS
        // --------------------------------------------------------

        formatted =
            formatted.replace(

                /^[•*-]\s+(.*?)$/gm,

                "<div class='chat-bullet'>"
                + "<span>•</span>"
                + "<div>$1</div>"
                + "</div>"

            );


        // --------------------------------------------------------
        // LINE BREAKS
        // --------------------------------------------------------

        formatted =
            formatted.replace(
                /\n/g,
                "<br>"
            );


        // --------------------------------------------------------
        // REMOVE EXTRA BREAKS AROUND BULLETS
        // --------------------------------------------------------

        formatted =
            formatted.replace(
                /<br><div class='chat-bullet'>/g,
                "<div class='chat-bullet'>"
            );


        formatted =
            formatted.replace(
                /<\/div><br>/g,
                "</div>"
            );


        return formatted;

    }



    // ============================================================
    // ESCAPE HTML
    // ============================================================

    function escapeHTML(text) {


        const div =
            document.createElement(
                "div"
            );


        div.textContent =
            text;


        return div.innerHTML;

    }



    // ============================================================
    // SCROLL TO BOTTOM
    // ============================================================

    function scrollToBottom() {


        messages.scrollTop =
            messages.scrollHeight;

    }


});