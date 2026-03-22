import os
from flask import Flask, render_template, request, redirect
import google.generativeai as genai

# Configure Gemini API
API_KEY = "REPLACE THIS WITH YOUR API KEY"  # REPLACE THIS WITH YOUR API KEY
genai.configure(api_key=API_KEY)

app = Flask(__name__)

def generate(youtube_link, model, additional_prompt):
    """Generate summary using Gemini API"""
    
    # Prepare the prompt
    if not additional_prompt:
        additional_prompt = ""
    
    prompt = f"Please provide a detailed summary of this YouTube video:\n{youtube_link}\n\nAdditional instructions: {additional_prompt}"
    
    try:
        # Use the newer API with model.generate_content
        response = genai.GenerativeModel(model).generate_content(prompt)
        return response.text if response.text else "No summary generated"
    except Exception as e:
        raise Exception(f"Error generating summary: {str(e)}")

@app.route('/', methods=['GET'])
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/summarize', methods=['GET', 'POST'])
def summarize():
    """Summarize the user provided YouTube video."""
    
    if request.method == 'POST':
        youtube_link = request.form.get('youtube_link', '')
        model = request.form.get('model', 'gemini-2.0-flash-001')
        additional_prompt = request.form.get('additional_prompt', '')
        
        try:
            summary = generate(youtube_link, model, additional_prompt)
            return summary
        except Exception as e:
            return f"Error: {str(e)}", 500
    else:
        return redirect('/')

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')