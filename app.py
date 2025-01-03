from flask import Flask, request, jsonify
from tools import fetch_weather, fetch_news, process_with_openai
import logging

# Logging Configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

# Initialize Flask App
app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    """Endpoint to handle user queries."""
    user_input = request.json.get('query', '')

    # Process the query using OpenAI API
    try:
        response = process_with_openai(user_input)
        return jsonify({"response": response})
    except Exception as e:
        logging.error(f"Error processing query: {e}")
        return jsonify({"response": "Sorry, something went wrong."}), 500

if __name__ == '__main__':
    app.run(debug=True)
