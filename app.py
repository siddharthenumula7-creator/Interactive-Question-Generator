import os
import gradio as gr
from google import genai


# Get Gemini API key from Render Environment Variable
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")


# Create Gemini client
client = genai.Client(api_key=API_KEY)


def generate_questions(topic, difficulty, number):

    if not topic.strip():
        return "Please enter a topic."

    prompt = f"""
You are an Interactive Question Generator.

Topic: {topic}
Difficulty Level: {difficulty}
Number of Questions: {number}

Generate exactly {number} questions.

Requirements:
- Number each question clearly.
- Make every question relevant to the topic.
- Match the selected difficulty level.
- Do not provide answers.
- Keep the questions suitable for students.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


# Create Gradio interface
interface = gr.Interface(
    fn=generate_questions,

    inputs=[
        gr.Textbox(
            label="Enter Topic",
            placeholder="Example: Python Programming"
        ),

        gr.Dropdown(
            choices=["Easy", "Medium", "Hard"],
            value="Medium",
            label="Difficulty Level"
        ),

        gr.Number(
            value=5,
            precision=0,
            label="Number of Questions"
        )
    ],

    outputs=gr.Textbox(
        label="Generated Questions",
        lines=12
    ),

    title="Interactive Question Generator",

    description=(
        "Enter a topic, select the difficulty level "
        "and number of questions."
    )
)


# Render provides the PORT environment variable
port = int(os.environ.get("PORT", 7860))

interface.launch(
    server_name="0.0.0.0",
    server_port=port
)
