from flask import Flask, render_template, request, jsonify
import dropbox
import os

app = Flask(__name__)

# Get credentials from environment variables/secrets
DROPBOX_ACCESS_TOKEN = "sl.u.AFndDggNcPZytwOOid_34CxJ6efcj5hpeaA2cuugLPwM8xWq6MKA3XrJBooQ61YlRqHzpRIHmxDRzVgct4dAQKV2TSlld-7FIfpf6UZ7dujZViFo_lgbv7lAzzTc7JCNI74ouukscBh2kjLGmq1mggbbd45oY7kGTMBvNPx-ChLg1O_8PlZYbphNV5g0lID5JNqa0RaJZ6sFyVZqdTd1u0ujpCaq4PAvdeTceKjjyxeYbX2JTJ5-fMRsxchG1A3e3A3TDdJLQVH-HdWpurMuBRcuBpDz28zi8mJ0kfbnuGehvavagRUqRe1C3OJlm7kMgNu9sedKIMPq1aauNpNLMhC7UNW1j8rOH_I9ucnOLPSIQmsyAs3Sb50DRHAXk3O6y_9Upd53bpXZJDUcZwaIt3kjiqBmeSN7J9YJwdRkEtPSPX2_JfCBQMZnW0lGe4WxCv5bb1MRhqIDUKlzRk7dkioPgGR4O5K1RD2bnjv1t85AJrVm3IGrcdKnoRyspVj6ldBbWsUlvQqO2pJ2cl5RRRO_Z1KIEqJePgiTJSjHFp9qEsx3XWvUyzWKZIzSWROp5SflnFKYhAzkpIIIpDXMTvjIPk1u2k0iCfce78pbjCc_CdJAxjLaX5maVxl4LwJNwgIuYhe4KCpXwHy837NCHKL3eYope8iqqnLicXOCMEn4KUGMMt9tBRXJdqpLCa2sXkTUA6CI253eY5mgMJXwjOqRERZOGac8uVZxhzOmlM7gvmfef8zNjsR0xXjkj2sJHA64t7lRADIZqMvK0aJQ1x1GR72hSjdfybaxCJFCZBuslU-uBBhw5GXMCv2kkoLAhuNGMj5za-3B5mH9icaiv5EDJA_3RSsByBStvrdkPBuxpGhAzkOKTVPrXQHbEqbpldWXe4TJgy8q1uz7xZYBUjJRHGbEh7up21WaKw36_4uIe0R6iWwH2eeAyT3QYdizuc0-hRDn2jTbFgKVFkm058hlWJPTOW7CLVwX6s9RAsmjIwobtliH1XFsaidDHP8kEwBqiKQWh00bON1JTXqMvg2VLgiYzX35AwndiLM-M1eXAkcIh_IYz7MjAbsnYWo8gkWINfHklZJIDhGwAMQvicc8tFkSrCFpv21auPDwdaoZtedmD3rneOWsfU0dE8-lhY1xdZRlPp2nPehpey9p8oililmZmwZc_rNUp6ERs6G_3ek1LtHATGeInUobhDvymXMPic6kaGtraok5NPgXt6dYEZ2MZ5Ut8_QWZ8BsPvZKx0aeTU8NW2iN0OyM0WGkxBMB3z7IygNXipN0GTveuKxIB28PpA-1_9e-l-qIFS9_K2izq9kzxBs_AutdFQHz5ltbpSWWN6jIj5EVj94b7rsVwnyHZA750QTpW_sjrdBcZbIWmdBxAm7nEnptW4bA3xcRVIQMADbsEh61t2WfatKBX3CVgHfIh3yXX6-jJgF9Ig"
APP_KEY = "edl2uiq0plk136y"
APP_SECRET = "np90vhxg46ucesj"

# Check if credentials are present
if not DROPBOX_ACCESS_TOKEN:
    print("WARNING: DROPBOX_ACCESS_TOKEN is not set. Please add it in the Secrets tab.")

# Initialize Dropbox client
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
