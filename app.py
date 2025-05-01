from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
import random
import smtplib  # For sending OTP via email

app = Flask(__name__)
CORS(app)

openai.api_key = "<your_actual_openai_api_key>"

# Store OTPs temporarily (in production, use a database)
otp_storage = {}

# Email configuration (replace with your details)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "your-email@gmail.com"
EMAIL_PASSWORD = "your-email-password"


def send_email_otp(email, otp):
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f"Subject: Your OTP Code\n\nYour OTP is {otp}. It is valid for 5 minutes."
        server.sendmail(EMAIL_ADDRESS, email, message)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


@app.route("/generate-otp", methods=["POST"])
def generate_otp():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    otp = random.randint(100000, 999999)
    otp_storage[email] = otp  # Store OTP (you can add expiration logic here)

    if send_email_otp(email, otp):
        return jsonify({"message": "OTP sent successfully!"}), 200
    else:
        return jsonify({"error": "Failed to send OTP. Please try again."}), 500


@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.json
    email = data.get("email")
    otp = data.get("otp")

    if not email or not otp:
        return jsonify({"error": "Email and OTP are required"}), 400

    if email in otp_storage and otp_storage[email] == int(otp):
        del otp_storage[email]  # Remove OTP after successful verification
        return jsonify({"message": "OTP verified successfully!"}), 200
    else:
        return jsonify({"error": "Invalid or expired OTP"}), 400


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    response = generate_ai_response(user_input)
    return jsonify({"response": response})


def generate_ai_response(user_input):
    try:
        # Common questions and answers
        common_questions = {
            "I want admission": "To apply for admission, please visit the admissions office or fill out the online form on our website.",
            "What courses are available?": "Our college offers courses in Computer Science, Engineering, Business Administration, and Arts. For detailed information, please visit the courses page on our website.",
            "What is the fee structure?": "The fee structure varies by course. Please check the fee details on our website or contact the finance office.",
            "What are the college timings?": "Our college operates from 8:00 AM to 5:00 PM, Monday to Friday.",
            "How can I contact the administration?": "You can contact the administration via email at admin@college.edu or call us at +123456789."
        }

        # Check if the user input matches a predefined question
        for question, answer in common_questions.items():
            if question.lower() in user_input.lower():
                return answer

        # If no match, use AI to generate a response
        completion = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"You are a helpful college assistant chatbot. {user_input}",
            max_tokens=150
        )
        return completion.choices[0].text.strip()
    except Exception as e:
        return "I'm sorry, I couldn't process your request right now. Please try again later."


if __name__ == "__main__":
    app.run(debug=True)