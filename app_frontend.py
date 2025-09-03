from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

# This route serves the HTML file for the user interface
@app.route('/')
def home():
    return render_template('question.html', chat_history=[])

@app.route('/healthz')
def health_check():
    return jsonify({"status": "healthy"}), 200



# This route forwards the user's question to the AI microservice
@app.route('/chatbot', methods=['POST'])
def chatbot():
    # Get the user's question and the unique user ID from the request data
    data = request.get_json()
    question = data.get('question')
    user_id = data.get('user_id')

    if not question or not user_id:
        return jsonify({'answer': 'Please provide a question and user ID.'}), 400

    try:
        # NOTE: Replace 'http://ai-service:5001' with your AI microservice's actual address if not using Docker Compose.
        ai_api_url = "http://ai-service:5001/generate-response"
        
        # Send the user's question and unique ID to the AI service as JSON
        response = requests.post(ai_api_url, json={'question': question, 'user_id': user_id})
        response.raise_for_status()
        
        # The AI microservice returns a JSON response
        ai_response_data = response.json()
        ai_response_text = ai_response_data.get('answer', 'An unexpected error occurred.')

        return jsonify({'answer': ai_response_text})

    except requests.exceptions.RequestException as e:
        print("Error connecting to AI microservice:", e)
        return jsonify({'answer': f"Sorry, an error occurred while connecting to the AI service: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
