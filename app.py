from flask import Flask, render_template, request, jsonify
import dropbox
import os

app = Flask(__name__)

# Get credentials from environment variables/secrets
DROPBOX_ACCESS_TOKEN = os.environ.get("DROPBOX_ACCESS_TOKEN")
APP_KEY = os.environ.get("APP_KEY")
APP_SECRET = os.environ.get("APP_SECRET")

dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
FILE_PATH = "/public_notepad.txt"

# Get the port number from environment variable
port = int(os.environ.get("PORT", 5000))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_note():
    try:
        content = request.form.get('content', '')
        
        # Better error handling for empty content
        if not content:
            return jsonify({"status": "success"})
            
        dbx.files_upload(
            content.encode(),
            FILE_PATH,
            mode=dropbox.files.WriteMode.overwrite
        )
        return jsonify({"status": "success"})
    except dropbox.exceptions.ApiError as e:
        app.logger.error(f"Dropbox API error: {str(e)}")
        return jsonify({"status": "error", "message": "ড্রপবক্স সার্ভারে সমস্যা"})
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"status": "error", "message": "অপ্রত্যাশিত সমস্যা"})

@app.route('/load')
def load_note():
    try:
        try:
            _, response = dbx.files_download(FILE_PATH)
            content = response.content.decode()
            return jsonify({"status": "success", "content": content})
        except dropbox.exceptions.ApiError as e:
            if isinstance(e.error, dropbox.files.DownloadError) and e.error.is_path():
                # File doesn't exist yet, return empty content
                return jsonify({"status": "success", "content": ""})
            raise
    except dropbox.exceptions.ApiError as e:
        app.logger.error(f"Dropbox API error: {str(e)}")
        return jsonify({"status": "error", "message": "ড্রপবক্স সার্ভারে সমস্যা"})
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"status": "error", "message": "অপ্রত্যাশিত সমস্যা"})

if __name__ == '__main__':
    # Run the app on 0.0.0.0 to make it accessible externally
    app.run(host='0.0.0.0', port=port)
