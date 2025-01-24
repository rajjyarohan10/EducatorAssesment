from flask import Flask, request, render_template
from openai import OpenAI
import os

app = Flask(__app__)

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv("MY_OPEN_AI_KEY"))

# Helper function to generate a lesson plan
def generate_lesson_plan(prompt):
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-4o-mini",
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"Error generating lesson plan: {e}")
        return "There was an issue generating the lesson plan."

# Helper function to generate an assessment
def generate_assessment(prompt):
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-4o-mini",
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"Error generating assessment: {e}")
        return "There was an issue generating the assessment."

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Generate route to handle form submission
@app.route('/generate', methods=['POST'])
def generate():
    # Get user inputs from the form
    time = request.form['time']
    grade = request.form['grade']
    environment = request.form['environment']
    confidence = request.form['confidence']
    include_assessment = request.form['assessment']

    # Generate lesson plan using the provided inputs
    lesson_plan_prompt = f"""
    Create a lesson plan for a hands-on activity.
    Time: {time}
    Grade: {grade}
    Environment: {environment}
    Confidence level: {confidence}
    Include assessment: {include_assessment}
    """
    lesson_plan = generate_lesson_plan(lesson_plan_prompt)

    # Generate assessment if requested
    assessment = ""
    if include_assessment.lower() == "yes":
        assessment_prompt = f"Create an assessment for the above lesson plan."
        assessment = generate_assessment(assessment_prompt)

    # Render the results page with all outputs
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

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
