from flask import Flask, render_template, request, jsonify
import os
import webbrowser
from langchain_ai21 import AI21LLM
from langchain_core.prompts import PromptTemplate
from threading import Timer

# Set up your AI21 API key
os.environ["AI21_API_KEY"] = "oPEAPlzuLdhnhKVRHloolJMz1Hs21dLF"

# Define the prompt template
template = """Question: {question}

Answer: give some short wellness tips. The chatbot should be able to interpret simple prompts related to stress
levels, emotions, or mood. Recommend simple exercises, such as guided breathing
or relaxation techniques, based on user input. Please offer motivational quotes, short wellness tips."""

prompt = PromptTemplate.from_template(template)

# Initialize the AI21 model
model = AI21LLM(model="j2-ultra", max_tokens=400)

chain = prompt | model

# Initialize the Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    response = get_chat_response(msg)
    return jsonify({"response": response})

def get_chat_response(text):
    # Use the AI21 model to generate a response based on user input
    response = chain.invoke({
        "question": text
    })

    # Check if the response seems truncated, and if so, ask the model to continue
    if response.strip().endswith('...'):
        follow_up_prompt = "Please continue the above answer in detail."
        follow_up_response = chain.invoke({"question": follow_up_prompt})
        response += " " + follow_up_response

    return response.strip()

def open_browser():
    # Only open the browser if this is the main thread (and not the reloader)
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    # Start the Flask app in a separate thread and open the browser after a slight delay
    Timer(1, open_browser).start()
    app.run(debug=True)
