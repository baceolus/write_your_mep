# MEP Contact Web Application

A web application that allows EU citizens to contact their Members of the European Parliament (MEPs) about AI risks and governance issues.

## Features

- 🌍 **Country Selection**: Choose from all EU countries to find your MEPs
- 📧 **Email Formatting**: Automatically converts obfuscated emails to proper format
- ✍️ **AI Risk Letter Template**: Pre-written professional letter about AI governance
- 👀 **Email Preview**: Review your message before sending
- 🚀 **Automated Sending**: Direct email delivery to selected MEPs
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices

## Setup Instructions

### 1. Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- MEP data file (`members_by_country.json`)

### 2. Installation

1. **Clone or download** the project files to your local machine

2. **Navigate to the project directory**:
   ```bash
   cd write_your_mep
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure the MEP data file is present**:
   Make sure `members_by_country.json` is in the same directory as `mep_webapp.py`

### 3. Email Configuration

To enable email sending functionality, you need to configure SMTP settings using environment variables:

#### For Gmail (Recommended):

1. **Enable 2-Factor Authentication** on your Google account
2. **Generate an App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
3. **Set environment variables**:

   **On macOS/Linux**:
   ```bash
   export EMAIL_USER="your-email@gmail.com"
   export EMAIL_PASSWORD="your-app-password"
   export SMTP_SERVER="smtp.gmail.com"
   export SMTP_PORT="587"
   ```

   **On Windows**:
   ```cmd
   set EMAIL_USER=your-email@gmail.com
   set EMAIL_PASSWORD=your-app-password
   set SMTP_SERVER=smtp.gmail.com
   set SMTP_PORT=587
   ```

#### For Other Email Providers:

Set the appropriate SMTP settings for your email provider:
- **Outlook/Hotmail**: `smtp-mail.outlook.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`
- **Custom SMTP**: Configure according to your provider

### 4. Running the Application

1. **Start the web server**:
   ```bash
   python mep_webapp.py
   ```

2. **Open your web browser** and go to:
   ```
   http://localhost:5000
   ```

3. **The application will display warnings** if:
   - MEP data file is missing
   - Email credentials are not configured

## Usage Guide

### Step 1: Fill in Your Information
- Enter your **first name** and **last name**
- Optionally provide your **email address** (for MEP replies)
- Select your **EU country** from the dropdown

### Step 2: Choose Your MEP
- After selecting your country, available MEPs will load
- Click on an MEP to select them
- MEPs are shown with their political affiliations

### Step 3: Review and Send
- Click **"Preview Letter"** to review the email content
- The letter includes professional content about AI risks and governance
- Click **"Send Email"** to deliver the message
- Confirm the sending action in the popup

### Step 4: Confirmation
- You'll receive a success message when the email is sent
- The form will reset for additional emails if needed

## Technical Details

### Data Structure

The MEP data is stored in `members_by_country.json` with the following structure:
```json
{
  "CountryName": [
    {
      "fullName": ["MEP Name"],
      "country": ["CountryName"],
      "politicalGroup": ["Political Group"],
      "nationalPoliticalGroup": ["National Group"],
      "contact_data": {
        "email": "obfuscated[at]email[dot]format"
      }
    }
  ]
}
```

### Email Processing

1. **Obfuscation Handling**: Converts `[at]` → `@` and `[dot]` → `.`
2. **Reverse Processing**: Emails appear to be reversed in the data
3. **Validation**: Ensures proper email format before sending
4. **Template Generation**: Creates personalized letters with user information

### API Endpoints

- `GET /` - Main application page
- `GET /api/meps/<country>` - Get MEPs for a specific country
- `POST /preview` - Generate email preview
- `POST /send` - Send email to MEP
- `GET /health` - Health check endpoint

## Security Considerations

- **Environment Variables**: Email credentials are stored as environment variables
- **Input Validation**: All user inputs are validated and sanitized
- **SMTP Security**: Uses TLS encryption for email transmission
- **No Data Storage**: User information is not stored permanently

## Troubleshooting

### Common Issues

1. **"MEP data file not found"**
   - Ensure `members_by_country.json` is in the correct directory
   - Check file permissions

2. **"Email credentials not configured"**
   - Set EMAIL_USER and EMAIL_PASSWORD environment variables
   - Verify SMTP settings for your email provider

3. **"Failed to send email"**
   - Check internet connection
   - Verify email credentials are correct
   - Ensure less secure app access is enabled (for Gmail, use App Password)

4. **"No MEPs found"**
   - Some countries may have MEPs without valid email addresses
   - Check the data file for your country's entries

### Email Provider Specific Issues

**Gmail**:
- Use App Passwords instead of regular passwords
- Enable 2-Factor Authentication first

**Outlook/Hotmail**:
- May require "Allow less secure apps" setting
- Check Microsoft account security settings

## Development

### File Structure
```
write_your_mep/
├── mep_webapp.py          # Main Flask application
├── templates/
│   └── mep_contact.html   # Frontend HTML template
├── members_by_country.json # MEP data (required)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

### Customization

You can customize the application by:
- Modifying the letter template in `generate_ai_risk_letter()` function
- Updating the CSS styles in the HTML template
- Adding additional form fields or validation
- Implementing database storage for sent emails

## License

This project is provided as-is for educational and civic engagement purposes.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all setup steps are completed correctly
3. Ensure all required files are present and accessible
