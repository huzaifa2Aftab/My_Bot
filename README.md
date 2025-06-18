# My_Bot
#This is a simple functional chatbot that serves as an interactive version of my portfolio.
Instead of reading a traditional CV, users can talk to this bot and ask about my projects, skills, hobbies, and experiences—just like having a conversation with me.

How It Works Technically:
Intent Training Using Neural Networks:
I trained the bot using a basic intent classification system. Each intent (like "ask about skills" or "ask about hobbies") has example phrases. These phrases were first converted into numerical form using vectorization techniques (like Bag of Words or TF-IDF), so they can be processed by the neural network.

Neural Network Model:
The vectorized data was then passed through a simple neural network, which learned to identify the correct intent behind a user's message. This helps the bot understand what the user wants to know (e.g., “Tell me about your projects”).

Response Handling with Functions:
I created custom functions to handle different types of user input. Based on the predicted intent, the bot calls the relevant function to generate an appropriate response from my portfolio.

Web Integration Using Flask:
To make the bot accessible online, I built a web interface using HTML and Flask (a Python web framework). Flask runs the server, connects the chatbot logic to the web page, and handles user inputs in real time.
