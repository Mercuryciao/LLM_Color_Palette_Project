import openai
import json
from dotenv import dotenv_values

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]
from IPython.display import Markdown, display


def display_colors(colors):
    display(
        Markdown(
            " ".join(
                f"<span style='color: {color}'>{chr(9608) * 4}</span>"
                for color in colors
            )
        )
    )

def get_and_render_colors(msg):
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

    response = openai.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="gpt-3.5-turbo",
        max_tokens=200,
    )




    colors = json.loads(response.choices[0].message.content)

    display_colors(colors)