#!/usr/bin/env python3
"""
EU Parliament Member Contact Web Application
Allows users to send emails to their MEPs about AI risks
"""

import json
import os
import urllib.parse
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import re
import requests

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

def record_submission_to_sheet(user_data):
    """Record a submission to Google Sheets via Apps Script"""
    
    # Get the Google Apps Script Web App URL from environment variable
    apps_script_url = os.environ.get('GOOGLE_APPS_SCRIPT_URL')
    
    if not apps_script_url:
        print("Warning: GOOGLE_APPS_SCRIPT_URL not set. Tracking disabled.")
        return False
    
    try:
        # Send data to Google Apps Script
        response = requests.post(
            apps_script_url,
            json=user_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ Recorded submission: {user_data.get('first_name')} {user_data.get('last_name')} from {user_data.get('country')}")
                return True
            else:
                print(f"❌ Apps Script error: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout recording to Google Sheets")
        return False
    except Exception as e:
        print(f"❌ Error recording submission: {e}")
        return False

def load_mep_data():
    """Load MEP data from JSON file"""
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, 'members_by_country.json')
        
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: members_by_country.json not found at {json_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {}

def format_email(obfuscated_email):
    """Convert obfuscated email to proper format"""
    if not obfuscated_email:
        return None
    
    # Replace [at] with @ and [dot] with .
    email = obfuscated_email.replace('[at]', '@').replace('[dot]', '.')
    
    # Reverse the email (it appears to be reversed in the data)
    email = email[::-1]
    
    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_pattern, email):
        return email
    else:
        return None

def generate_ai_risk_letter(user_first_name, user_last_name, mep_name, country):
    """Generate a template letter about AI risks (OLD VERSION - NOT USED)"""
    template = f"""Dear {mep_name},

I hope this email finds you well. I am writing to express my concerns about the development of artificial intelligence and its potential impact on our society.

It has come to my attention that the leaders of the foremost AI companies and top experts in the field are currently warning about the risk of extinction from AI. Specifically, this risk stems from the development of what those in the field refer to as 'superintelligence'.

One such example is the CAIS open statement on AI risk which states, "Mitigating the risk of extinction from AI should be a global priority alongside other societal-scale risks such as pandemics and nuclear war." This statement is supported by both the CEOs of the field's leading AI companies and it's most preeminent experts, including Nobel Prize and Turing Award winners.

Given this information, I find it deeply concerning that several of the largest AI companies explicitly aim to develop superintelligence, despite the clear warnings from top experts in the field.

While I recognise the transformative benefits advanced AI technologies can bring, the creation of systems with intelligence far surpassing human capabilities carries irreversible and potentially catastrophic risks that cannot be ignored. We must approach this development with caution and responsibility.

I urge you to publicly call for new laws to protect us from the threat posed by the development of superintelligent AI systems. It is vital that our legislature takes a proactive approach in forming a coalition aimed at banning superintelligence and ensuring we remain in control of our future.

I would welcome the opportunity to provide any additional information that might be helpful in your consideration of this matter with either yourself or your office.

Thank you for your time and attention to this critical matter.

Yours sincerely,

{user_first_name} {user_last_name}

{country}"""
    return template

def generate_ai_risk_letter_whistleblower(user_first_name, user_last_name, mep_name, country):
    """Generate a template letter about AI Whistleblower Protection Act"""
    template = f"""Dear {mep_name},

As the EU Parliament assesses strategies for mitigating risks associated with emerging technologies like artificial intelligence, I write in support of the AI Whistleblower Protection Act.

AI is reshaping society, defense capabilities, and global industries. With this transformation comes increasing potential for misuse, ethical lapses, and unintended consequences that could impact the public on a large scale. Ensuring transparency and accountability is both a public interest and national security imperative.

Employees and industry insiders have consistently been first to warn about technology risks. In Silicon Valley, engineers have exposed AI models released without proper safeguards, former staff have surfaced data on digital harms, and researchers have stepped forward when serious risks were ignored. Their disclosures gave the public and policymakers evidence needed to act.

However, without strong legal safeguards, individuals may be deterred from reporting issues due to fear of retaliation. In June 2024, over a dozen current and former employees from leading AI companies, including OpenAI and Google DeepMind, stated publicly that confidentiality agreements and fear of retaliation prevented them from raising legitimate safety concerns. This silences critical voices and undermines technological integrity.

Congress has the opportunity to protect individuals who come forward in good faith and reinforce that safety, ethics, and accountability must accompany innovation. In an age where AI systems influence everything from elections to defense systems, whistleblower protections are more urgent than ever.

The AI Whistleblower Protection Act ensures those developing AI systems are not punished for acting in the public interest. Strong whistleblower protections are essential to guiding AI development in a way that upholds our shared democratic values.

Thank you for your consideration.

Yours sincerely,

{user_first_name} {user_last_name}

{country}"""
    return template



@app.route('/')
def index():
    """Main page with country selection and form"""
    mep_data = load_mep_data()
    countries = sorted(mep_data.keys()) if mep_data else []
    return render_template('mep_contact.html', countries=countries)

@app.route('/api/meps/<country>')
def get_meps_by_country(country):
    """API endpoint to get MEPs for a specific country"""
    mep_data = load_mep_data()
    
    if country not in mep_data:
        return jsonify({'error': 'Country not found'}), 404
    
    meps = []
    for mep in mep_data[country]:
        formatted_email = format_email(mep.get('contact_data', {}).get('email', ''))
        if formatted_email:  # Only include MEPs with valid emails
            meps.append({
                'name': mep['fullName'][0] if mep.get('fullName') else 'Unknown',
                'email': formatted_email,
                'political_group': mep.get('politicalGroup', ['Unknown'])[0],
                'national_group': mep.get('nationalPoliticalGroup', ['Unknown'])[0]
            })
    
    return jsonify(meps)

@app.route('/preview', methods=['POST'])
def preview_email():
    """Preview the email before sending"""
    data = request.json
    
    user_first_name = data.get('first_name', '').strip()
    user_last_name = data.get('last_name', '').strip()
    country = data.get('country', '').strip()
    mep_name = data.get('mep_name', '').strip()
    
    if not all([user_first_name, user_last_name, country, mep_name]):
        return jsonify({'error': 'All fields are required'}), 400
    
    letter_content = generate_ai_risk_letter(user_first_name, user_last_name, mep_name, country)
    
    return jsonify({
        'subject': 'Concerns about AI risks',
        'content': letter_content
    })

@app.route('/record_submission', methods=['POST'])
def record_submission_endpoint():
    """Record a user submission to Google Sheets"""
    data = request.json
    
    user_first_name = data.get('first_name', '').strip()
    user_last_name = data.get('last_name', '').strip()
    user_email = data.get('user_email', '').strip()
    country = data.get('country', '').strip()
    mep_name = data.get('mep_name', '').strip()
    mep_email = data.get('mep_email', '').strip()
    
    if not all([user_first_name, user_last_name, country, mep_name, mep_email]):
        return jsonify({'error': 'All required fields must be filled'}), 400
    
    # Record to Google Sheets
    submission_data = {
        'first_name': user_first_name,
        'last_name': user_last_name,
        'user_email': user_email,
        'country': country,
        'mep_name': mep_name,
        'mep_email': mep_email
    }
    
    success = record_submission_to_sheet(submission_data)
    
    if success:
        return jsonify({'success': True, 'message': 'Submission recorded successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to record submission'}), 500

@app.route('/send', methods=['POST'])
def generate_mailto_link():
    """Generate mailto link for the user to send email from their own client"""
    data = request.json
    
    user_first_name = data.get('first_name', '').strip()
    user_last_name = data.get('last_name', '').strip()
    user_email = data.get('user_email', '').strip()
    country = data.get('country', '').strip()
    mep_name = data.get('mep_name', '').strip()
    mep_email = data.get('mep_email', '').strip()
    
    # Get custom content if provided
    custom_subject = data.get('custom_subject', '').strip()
    custom_content = data.get('custom_content', '').strip()
    
    if not all([user_first_name, user_last_name, country, mep_name, mep_email]):
        return jsonify({'error': 'All required fields must be filled'}), 400
    
    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if user_email and not re.match(email_pattern, user_email):
        return jsonify({'error': 'Invalid user email format'}), 400
    
    if not re.match(email_pattern, mep_email):
        return jsonify({'error': 'Invalid MEP email format'}), 400
    
    # Use custom content if provided, otherwise generate the default letter
    if custom_subject and custom_content:
        subject = custom_subject
        letter_content = custom_content
    else:
        letter_content = generate_ai_risk_letter(user_first_name, user_last_name, mep_name, country)
        subject = 'Support for AI Whistleblower Protection'
    
    # URL encode the content for mailto link
    encoded_subject = urllib.parse.quote(subject)
    encoded_body = urllib.parse.quote(letter_content)
    
    # Generate mailto link
    mailto_link = f"mailto:{mep_email}?subject={encoded_subject}&body={encoded_body}"
    
    return jsonify({
        'success': True, 
        'mailto_link': mailto_link,
        'mep_name': mep_name,
        'mep_email': mep_email
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    # Check if MEP data file exists
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'members_by_country.json')
    
    if not os.path.exists(json_path):
        print(f"Warning: members_by_country.json not found at {json_path}")
        print("Please make sure the MEP data file is in the same directory as this script")
    
    print("✅ MEP Contact App using mailto links - no email configuration needed!")
    print("📧 Users will send emails directly from their own email clients")
    
    apps_script_url = os.environ.get('GOOGLE_APPS_SCRIPT_URL')
    if apps_script_url:
        print("📊 Google Sheets integration: ENABLED - submissions will be tracked")
    else:
        print("📊 Google Sheets integration: DISABLED - submissions will not be tracked")
        print("   (Set GOOGLE_APPS_SCRIPT_URL environment variable to enable)")
    
    # Use environment variables for production
    port = int(os.environ.get('PORT', 5001))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
