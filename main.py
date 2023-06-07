import os
from flask import Flask, request, render_template
from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.memory import ConversationBufferWindowMemory

os.environ["OPENAI_API_KEY"] = "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"

memory = ConversationBufferWindowMemory(memory_key="history")

def chat(condition, severity, inpt):

    chatprompt = "You are healthGPT, a health advisor. The user is suffering from " + condition + " health condition. The present severity of this condition is "+severity+"""
    . You have to act like a doctor and respond to the user queries according to the severity of their health condition. Give some basic advice and ask if they have any issues or questions they would like to ask related to their health condition adnd severity. Be very humble when replying and speak
    in a regrettable tone. Behave like an expert health advisor and answer confidently. Do not give negative respnses similar to "Sorry I don't know" or 
    "I am not a health advisor" and so. Do not greet the user. Answer in detail. Stick to the context.
    {history}
    Human: {human_input}
    Assistant:"""

    prompt = PromptTemplate(input_variables=["history", "human_input"], template=chatprompt)

    healthGPT = LLMChain(
    llm=OpenAI(temperature=0.9, top_p=0.7), 
    prompt=prompt, 
    verbose=True, 
    memory=ConversationBufferWindowMemory(k=5)) 

    response = healthGPT.predict(human_input=inpt)
    return response
    

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/get', methods=["POST"]) 
def main_page():
    condition = str(request.form["cond"])
    severity = str(request.form["sev"])
    msg = str(request.form["msg"])
    response = chat(condition, severity, msg)
    return response

if __name__=="__main__":
    app.run(debug=True)
