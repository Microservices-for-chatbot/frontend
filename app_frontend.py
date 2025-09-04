from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)


@app.route('/')
def home():
    """Serve the HTML file for the user interface."""
    return render_template('question.html', chat_history=[])


@app.route('/healthz')
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200


@app.route('/chatbot', methods=['POST'])
def chatbot():
    """
    Forward the user's question to the AI microservice.
    """
    data = request.get_json()
    question = data.get('question')
    user_id = data.get('user_id')

    if not question or not user_id:
        return jsonify({'answer': 'Please provide a question and user ID.'}), 400

    try:
        # Replace with your AI microservice's actual address if not using Docker Compose.
        # [2025-08-10] Note: This line has a hardcoded IP.
        # If you restart your EC2 instance, you will need to change this.
        ai_api_url = "http://ai-service:5001/generate-response"

        response = requests.post(
            ai_api_url,
            json={
                'question': question,
                'user_id': user_id
            },
            timeout=10 # It's a good practice to set a timeout for requests.
        )
        response.raise_for_status()

        ai_response_data = response.json()
        ai_response_text = ai_response_data.get(
            'answer',
            'An unexpected error occurred.'
        )

        return jsonify({'answer': ai_response_text})

    except requests.exceptions.RequestException as e:
        error_msg = (
            "Sorry, an error occurred while connecting to the AI service: "
            f"{e}"
        )
        return jsonify({'answer': error_msg}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
