from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        resume_content = request.form["resume"]
        feedback = get_rule_based_feedback(resume_content)  # Call the function to get feedback
        return render_template("index.html", feedback=feedback, resume=resume_content)
    return render_template("index.html")

def get_rule_based_feedback(resume_content):
    feedback = []
    
    # Rule 1: Check for resume length
    word_count = len(resume_content.split())
    if word_count > 500:
        feedback.append("❌ Your resume is too long. Try to keep it under 500 words.")
    elif word_count < 100:
        feedback.append("❌ Your resume is too short. Add more details about your skills and experience.")
    else:
        feedback.append("✅ Your resume length looks good!")
    
    # Rule 2: Check for action verbs
    action_verbs = ["achieved", "managed", "developed", "led", "improved", "created", "implemented"]
    found_verbs = [verb for verb in action_verbs if verb in resume_content.lower()]
    if not found_verbs:
        feedback.append("❌ Add more action verbs like 'achieved', 'managed', or 'developed'.")
    else:
        feedback.append(f"✅ Great! You used action verbs like: {', '.join(found_verbs)}.")
    
    # Rule 3: Check for quantifiable achievements
    if not any(word.isdigit() for word in resume_content.split()):
        feedback.append("❌ Add quantifiable achievements, e.g., 'Increased sales by 20%'.")
    else:
        feedback.append("✅ Good job! Your resume includes quantifiable achievements.")
    
    # Rule 4: Check for contact information
    if "email" not in resume_content.lower() and "phone" not in resume_content.lower():
        feedback.append("❌ Add your contact information (email or phone number).")
    else:
        feedback.append("✅ Your contact information is included.")
    
    # Rule 5: Check for keywords (customize based on job role)
    keywords = ["teamwork", "communication", "problem-solving", "leadership"]
    missing_keywords = [kw for kw in keywords if kw not in resume_content.lower()]
    if missing_keywords:
        feedback.append(f"❌ Consider adding these keywords: {', '.join(missing_keywords)}.")
    else:
        feedback.append("✅ Your resume includes important keywords.")
    
    # Rule 6: Check for grammar (basic rules)
    if not any(sentence.endswith(('.', '!', '?')) for sentence in resume_content.split('\n')):
        feedback.append("❌ Ensure each sentence ends with proper punctuation (., !, or ?).")
    else:
        feedback.append("✅ Your resume uses proper punctuation.")
    
    # Rule 7: Check for formatting (bullet points)
    if "- " not in resume_content and "* " not in resume_content:
        feedback.append("❌ Use bullet points (- or *) to list your achievements and responsibilities.")
    else:
        feedback.append("✅ Your resume uses bullet points effectively.")
    
    # Rule 8: Check for key sections
    required_sections = ["Education", "Experience", "Skills"]
    missing_sections = [section for section in required_sections if section.lower() not in resume_content.lower()]
    if missing_sections:
        feedback.append(f"❌ Add these missing sections: {', '.join(missing_sections)}.")
    else:
        feedback.append("✅ Your resume includes all key sections.")
    
    return "\n\n".join(feedback)

if __name__ == "__main__":
    app.run(debug=True)