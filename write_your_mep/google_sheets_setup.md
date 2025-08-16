# Google Sheets Integration Setup

This guide will help you set up Google Sheets integration to track user submissions.

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API and Google Drive API

## Step 2: Create Service Account Credentials

1. Go to "IAM & Admin" → "Service Accounts"
2. Click "Create Service Account"
3. Give it a name like "MEP Contact Tracker"
4. Click "Create and Continue"
5. Skip the optional steps and click "Done"
6. Click on the created service account
7. Go to the "Keys" tab
8. Click "Add Key" → "Create new key"
9. Choose "JSON" format
10. Download the JSON file

## Step 3: Create Google Spreadsheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet
3. Name it "MEP Contact Submissions" (or whatever you prefer)
4. Copy the spreadsheet ID from the URL (the long string between `/d/` and `/edit`)
5. Share the spreadsheet with your service account email (found in the JSON file)
   - Give it "Editor" permissions

## Step 4: Configure Environment Variables

### For Local Development:
1. Save the downloaded JSON file as `google_sheets_credentials.json` in the same directory as `mep_webapp.py`
2. Set the spreadsheet ID:
   ```bash
   export GOOGLE_SHEETS_ID="your_spreadsheet_id_here"
   ```

### For Production (Heroku/etc):
Set these environment variables:
```bash
GOOGLE_SHEETS_CREDENTIALS='{"type": "service_account", "project_id": "...", ...}'  # The entire JSON content
GOOGLE_SHEETS_ID="your_spreadsheet_id_here"
```

## Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

## What Gets Recorded

The following data will be recorded for each submission:
- Timestamp
- First Name
- Last Name  
- Email (optional)
- Country
- MEP Name
- MEP Email

## Troubleshooting

- Make sure the service account has access to the spreadsheet
- Check that both Google Sheets API and Google Drive API are enabled
- Verify the credentials JSON is properly formatted
- Check the logs for any error messages

If Google Sheets integration fails, the app will still work normally - it just won't record the submissions.
