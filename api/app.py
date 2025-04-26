from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OPENROUTER_API_KEY = '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'

@app.route('/generate-design-prompt', methods=['POST'])
def generate_prompt():
    user_input = request.json.get("message")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourdomain.com",  # apni domain ya localhost ka URL daalo yahan
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Your task is to understand design ideas written in Roman Urdu by the user, "
                    "and generate a creative, high-quality English prompt for AI image generation. "
                    "Make sure the prompt is suitable for tools like Midjourney, DALL·E, or for T-shirt and cap designs. "
                    "Reply only with the English prompt."
                )
            },
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.9,
        "max_tokens": 200
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch from OpenRouter", "details": response.text}), 500

    output = response.json()

    if 'choices' not in output:
        return jsonify({"error": "Invalid response from OpenRouter", "details": output}), 500

    reply = output['choices'][0]['message']['content']

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(port=5000)
