from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, storage
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
api_key = os.getenv("OPENAI_API_KEY")
cred = credentials.Certificate("firebase-credentials.json")
firebase_admin.initialize_app(cred, {
    "storageBucket": "talos-app.firebasestorage.app"
})

'''
    provide a detailed analysis in JSON format.

    Survey Data: {survey_data}

    Respond with a JSON object containing:
    - "allocations": A dictionary where keys are categories (e.g., Marketing, Operations, Debt Repayment) and values are suggested amounts or details.
    - "risks": A list of potential risks identified and a respective risk score (0 = no risk, 100 = critical risk).
    - "recommendations": A list of detailed, actionable recommendations to mitigate risks.
    - "total_after_suggestions": Total finances after implementing the recommendations.
'''

client = OpenAI(api_key=api_key)

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    survey_responses = request.form.get('survey_responses')
    if file:
        bucket = storage.bucket()
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)
        blob.make_public()
        image_url = blob.public_url

        try:
            system = """
                You are an experienced financial analyst and business consultant. I will provide you with financial data for a business. Please analyze this data and provide a structured response addressing the following areas:
            """
            user = f"""
                Business information: {survey_responses}
                Image URL: {image_url}
            """
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ]
            )
            analysis = response.choices[0].message.content
        except Exception as e:
            analysis = f"Error during OpenAI analysis: {str(e)}"

        return jsonify({"url": image_url, "analysis": analysis})
    
    return jsonify({"error": "No file uploaded"}), 400

if __name__ == '__main__':
    app.run(debug=True)