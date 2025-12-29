# How to Update Your Gemini API Keys

## Why You Need This

Your current API keys have been flagged as "leaked" by Google. This typically happens when:
- Keys are committed to public GitHub repositories
- Keys are shared in public forums
- Keys are exposed in screenshots or logs

## Getting New API Keys

### Step 1: Visit Google AI Studio
Go to: **https://aistudio.google.com/app/apikey**

### Step 2: Sign In
Use your Google account

### Step 3: Create API Key
1. Click **"Create API Key"** button
2. Select your Google Cloud project (or create a new one if needed)
3. Click **"Create API key in new project"** or **"Create API key in existing project"**
4. **Copy the key** immediately (you won't see it again!)

### Step 4: Create Multiple Keys (Optional but Recommended)
For better daily limits, create 2-3 keys:
1. Repeat Step 3 for each key
2. Keep them in a safe place (password manager, secure notes)

## Updating Your Configuration

### Method 1: Edit config.py Manually

1. Open config.py:
```bash
notepad config.py
```

2. Find the `GEMINI_API_KEYS` section (around line 22)

3. Replace with your new keys:
```python
GEMINI_API_KEYS = [
    'YOUR_NEW_KEY_1_HERE',
    'YOUR_NEW_KEY_2_HERE',  # Optional second key
    'YOUR_NEW_KEY_3_HERE',  # Optional third key
]
```

4. Save the file (Ctrl+S)

### Method 2: Use the Quick Update Script (Coming soon)

We can create a script to safely update keys without editing code directly.

## Testing Your New Keys

After updating, test the conversion:

```bash
python convert_my_resume.py
```

If successful, you'll see:
```
[SUCCESS] Your resume has been converted to JSON
```

## Key Management Best Practices

### ✅ Do:
- Store keys in environment variables (not in code)
- Use separate keys for development and production
- Create multiple keys for rotation
- Keep keys in a password manager
- Delete old/compromised keys

### ❌ Don't:
- Commit keys to GitHub
- Share keys in public forums
- Post screenshots showing keys
- Use the same key across multiple projects
- Leave keys in code comments

## Daily Limits

Each Gemini API key has:
- **1,500 requests per day** (free tier)
- **15 requests per minute**

With 2 keys: **3,000 requests/day**
With 3 keys: **4,500 requests/day**

## Current Configuration

Your system is configured to use these keys (from config.py):

```python
API_DAILY_LIMIT = 800  # Maximum requests per day per key
API_WARNING_THRESHOLD = 0.85  # Warn when usage reaches 85%
```

The system will:
- Automatically rotate between keys
- Track usage per key
- Warn you at 85% usage
- Switch to next key when limit reached

## Quick Fix Steps

1. **Get new key**: https://aistudio.google.com/app/apikey
2. **Open config**: `notepad config.py`
3. **Replace keys** around line 22-26
4. **Save** (Ctrl+S)
5. **Test**: `python convert_my_resume.py`

## Example Configuration

```python
# config.py (lines 20-28)

# API Keys - Support for multiple keys with rotation
GEMINI_API_KEYS = [
    'AIzaSyC_Your_New_Key_1_Here_xxxxxxxxxxxxx',  # Primary key
    'AIzaSyC_Your_New_Key_2_Here_xxxxxxxxxxxxx',  # Secondary key (optional)
    'AIzaSyC_Your_New_Key_3_Here_xxxxxxxxxxxxx',  # Tertiary key (optional)
]
```

## After You Update

Once you have new keys working:

1. **Delete old keys** from Google AI Studio to prevent misuse
2. **Test the system**:
   ```bash
   python convert_my_resume.py
   ```
3. **Verify output**:
   ```bash
   notepad data\resumes\Devin_C._Debit_resume.json
   ```

## Troubleshooting

### "API key was reported as leaked"
- You need to create a **brand new** API key
- Delete the leaked key from Google AI Studio
- Update config.py with the new key

### "API key not valid"
- Check for extra spaces or quotes
- Make sure you copied the entire key
- Try creating a new key

### "All API keys exhausted"
- You've hit the daily limit (800 requests per key)
- Wait 24 hours for reset
- Or add more API keys to config.py

## Need Help?

If you're stuck:
1. Make sure you're signed into the correct Google account
2. Check if you have billing enabled (free tier works, but some projects require it)
3. Try creating the key in a new Google Cloud project
4. Verify the key is for **Gemini API** (not other Google APIs)

---

**Once you update your API keys, your resume converter will work perfectly!**
