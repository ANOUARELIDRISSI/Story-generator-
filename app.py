from flask import Flask, render_template, request
from groq import Groq
import os

app = Flask(__name__)

# Initialize Groq client
groq_client = Groq(api_key="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")  # Replace with your Groq API key

def generate_story_part(prompt):
    """Generate a story part using Groq API."""
    response = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{prompt} Keep the story part short, around 1 to 2 lines.",
            }
        ],
        model="mixtral-8x7b-32768",  # Use the appropriate Groq model
    )
    return response.choices[0].message.content

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate-story", methods=["POST"])
def generate_story():
    # Get form data
    character1 = request.form.get("character1")
    character2 = request.form.get("character2")
    keywords = [
        request.form.get("keyword1"),
        request.form.get("keyword2"),
        request.form.get("keyword3"),
        request.form.get("keyword4"),
        request.form.get("keyword5"),
    ]

    # Generate story parts
    story_parts = []
    for keyword in keywords:
        # Generate story text using Groq
        prompt = f"Write a short story part about {character1} and {character2} involving {keyword}."
        story_text = generate_story_part(prompt)

        # Add story part to the list
        story_parts.append({"text": story_text})

    # Generate a title for the story
    title = f"The Adventure of {character1} and {character2}"

    return render_template("story.html", title=title, story_parts=story_parts)

if __name__ == "__main__":
    app.run(debug=True)