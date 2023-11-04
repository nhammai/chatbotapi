from flask import Flask, request, jsonify
from flask_cors import CORS

import openai
import os
import json

openai.api_key = os.environ['OPENAI_API_KEY']

# Call the openai ChatCompletion endpoint, with th ChatGPT model
# response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
#                                         messages=[{
#                                             "role": "user",
#                                             "content": "Hello World!"
#                                         }])

# # Extract the response
# print(response['choices'][0]['message']['content'])

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
  return 'Hello from Flask!'


def ask_gpt3(prompt):
  response = openai.ChatCompletion.create(messages=[{
      "role":
      "system",
      "content":
      "You're a helpful assistant that can help people have their best knowledge and have great experience"
  }, {
    "role": "user",
    "content": "Act like you're an expert know alots about geography. First tell them about yourself. You can answer questions about countries, capitals, languages, currency, population, climate. Also you can help people answer their question about where should they travel. You're so funny and friendly. And you will say it in a nice format. If the people ask you about another topic that you don't know about just act friendly and talk about what you know. But most of the time you will focus on the topic you know. Only speak in only 1 sentence. And be precisely and to point about what you say. To the point don't ramble. Now the text bellow is from the people: "
  },
                                        


                                                    
                                                    {
      "role": "user",
      "content": prompt
  }],
                                          model='gpt-3.5-turbo',
                                          temperature=0.7,
                                          
                                          n=1,
                                          stop=None,
                                          frequency_penalty=0,
                                          presence_penalty=0)

  answer = response['choices'][0]['message']['content']
  return answer


# ask_gpt3("Hello what is your name?")


# post method to request the gpt model to answer the question asked by user
@app.route('/ask', methods=['POST'])
def ask():
  prompt = request.json.get('prompt')
  if not prompt:
    return 'No prompt provided', 400
  answer = ask_gpt3(prompt)
  print(answer)
  return jsonify({'answer': answer})


app.run(host='0.0.0.0', port=81)
