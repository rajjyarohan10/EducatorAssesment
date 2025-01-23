# Import Libraries
from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)

# Replace with your OpenAI API key
openai.api_key = os.environ['MY_OPEN_AI_KEY']

"""
  Build Routes
"""
# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Process Educator Input and Generate Output
@app.route('/generate', methods=['POST'])
def generate():
    # Get user inputs
    time = request.form['time']
    grade = request.form['grade']
    environment = request.form['environment']
    confidence = request.form['confidence']
    include_assessment = request.form['assessment']

    # Generate lesson plan using OpenAI
    lesson_plan_prompt = f"""
    Create a lesson plan for a hands-on activity. 
    Time: {time}
    Grade: {grade}
    Environment: {environment}
    Confidence level: {confidence}
    Include assessment: {include_assessment}
    """
    lesson_plan = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": lesson_plan_prompt}
        ],
        max_tokens=300
    ).choices[0].message['content'].strip()

    # Create assessment if needed
    if include_assessment.lower() == "yes":
        assessment = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": assessment_prompt}
            ],
            max_tokens=150
        ).choices[0].message['content'].strip()

    # Render results
    return render_template(
        'result.html',
        time=time,
        grade=grade,
        environment=environment,
        confidence=confidence,
        include_assessment=include_assessment,
        lesson_plan=lesson_plan,
        assessment=assessment
    )

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5000)
