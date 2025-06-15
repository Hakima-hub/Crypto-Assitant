from flask import Flask, render_template, request
import requests
import openai

app = Flask(__name__)

openai.api_key = "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"


def get_price(coin):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    response = requests.get(url).json()
    return response.get(coin, {}).get("usd", "Not found")

def ask_gpt(question):
    prompt = f"You are a crypto expert assistant. Explain this clearly for a beginner:\n\n{question}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Or gpt-4 if you have access
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    if request.method == "POST":
        user_input = request.form["query"].lower()
        words = user_input.split()
        for word in words:
            price = get_price(word)
            if price != "Not found":
                answer = f"The current price of {word} is ${price}"
                break
        if answer == "":
            answer = "Sorry, I couldn’t find that coin 😕"
    return render_template("index.html", response=answer)

if __name__ == "__main__":
    app.run(debug=True)
