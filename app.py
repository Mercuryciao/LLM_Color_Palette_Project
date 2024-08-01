from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from flask import Flask, render_template, request

# Load environment variables
load_dotenv()
# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Initialize Flask app
app = Flask(__name__, template_folder = 'templates')

def get_colors(msg):
    prompt = f"""
    You are a color palette generating assistant that responds to text prompts for color palettes
    Your should generate color palettes that fit the theme, mood, or instructions in the prompt.
    The palettes should be between 2 and 8 colors.
    Q: Convert the following verbal description of a color palette into a list of colors: The Mediterranean Sea
    A: ["#006699", "#66CCCC", "#F0E68C", "#008000", "#F08080"]
    Q: Convert the following verbal description of a color palette into a list of colors: sage, nature, earth
    A: ["#EDF1D6", "#9DC08B", "#609966", "#40513B"]
    Desired Format: a JSON array of hexadecimal color codes
    Q: Convert the following verbal description of a color palette into a list of colors: {msg}
    A:
    """
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="gpt-3.5-turbo",
        max_tokens=200,
    )
    return json.loads(response.choices[0].message.content)

@app.route("/palette", methods=["POST"])
def prompt_to_palette():
    app.logger.info("I am here!")
    query = request.form.get("query")
    colors = get_colors(query)
    return {"colors": colors}


@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)