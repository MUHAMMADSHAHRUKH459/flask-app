from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OPENROUTER_API_KEY = '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'  # ← Yahan apna key lagayein

@app.route('/generate-design-prompt', methods=['POST'])
def generate_prompt():
    user_input = request.json.get("message")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "yourdomain.com",  # Required by OpenRouter
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

    output = response.json()
    reply = output['choices'][0]['message']['content']

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(port=5000)
