from flask import Flask, request, jsonify
from flask_cors import CORS

import openai
import os
import json

openai.api_key = os.environ['OPENAI_API_KEY']

# Call the openai ChatCompletion endpoint, with th ChatGPT model
response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                        messages=[{
                                            "role": "user",
                                            "content": "Hello World!"
                                        }])

# Extract the response
print(response['choices'][0]['message']['content'])

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
      "You're an AI assistant who answers user questions from the dataset."
  }, {
      "role": "user",
      "content": prompt
  }],
                                          model='gpt-3.5-turbo',
                                          temperature=0.7,
                                          max_tokens=100,
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
  return jsonify({'answer': answer})


app.run(host='0.0.0.0', port=81)
