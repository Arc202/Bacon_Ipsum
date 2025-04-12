from flask import Flask, request, jsonify
from cerebras.cloud.sdk import Cerebras
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialize Cerebras client
# In production, use os.environ.get("CEREBRAS_API_KEY") instead of hardcoding
cerebras_client = Cerebras(
    api_key=os.getenv("api_key")
)

@app.route('/generate-bacon', methods=['GET'])
def generate_bacon():
    # Get parameters from request with defaults
    paragraphs = int(request.args.get('paragraphs', 3))
    temperature = float(request.args.get('temperature', 0.7))
    
    # Limit paragraphs to a reasonable range
    if paragraphs < 1:
        paragraphs = 1
    elif paragraphs > 10:
        paragraphs = 10
    
    # Create the prompt for generating bacon ipsum
    system_prompt = """You are a specialized text generator that creates bacon-themed lorem ipsum text.
    Your text should be filled with meat terminology, especially bacon, but follow the style of lorem ipsum
    as placeholder text. Generate text that sounds professional but is entirely about various meat products."""
    
    user_prompt = f"Generate {paragraphs} paragraphs of bacon-themed lorem ipsum. Make it meaty and delicious."
    
    # Call Cerebras API
    response = cerebras_client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        model="llama-4-scout-17b-16e-instruct", 
        max_completion_tokens=1024,
        temperature=temperature,
        stream=False
    )
    
    # Extract the generated text
    bacon_text = response.choices[0].message.content
    
    # Return as JSON
    return jsonify({
        "paragraphs": paragraphs,
        "bacon_ipsum": bacon_text
    })

@app.route('/', methods=['GET'])
def home():
    return """
    <html>
        <head>
            <title>Cerebras Bacon Ipsum API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                h1 { color: #d02323; }
                code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <h1>Cerebras Bacon Ipsum API</h1>
            <p>Generate bacon-themed lorem ipsum text using Cerebras AI.</p>
            <h2>Endpoints:</h2>
            <p><code>GET /generate-bacon</code> - Generate bacon ipsum text</p>
            <h2>Parameters:</h2>
            <ul>
                <li><code>paragraphs</code> - Number of paragraphs (default: 3, max: 10)</li>
                <li><code>temperature</code> - Creativity level (0.0-1.0, default: 0.7)</li>
            </ul>
            <h2>Example:</h2>
            <p><code>/generate-bacon?paragraphs=2&temperature=0.8</code></p>
        </body>
    </html>
    """

if __name__ == '__main__':
    # For production, use proper deployment with gunicorn or similar
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)