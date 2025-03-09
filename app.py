
from flask import Flask, render_template, request, jsonify, redirect, url_for
import dropbox
import os
import json
from datetime import datetime

app = Flask(__name__)

# Get credentials from environment variables/secrets
DROPBOX_ACCESS_TOKEN = "sl.u.AFndDggNcPZytwOOid_34CxJ6efcj5hpeaA2cuugLPwM8xWq6MKA3XrJBooQ61YlRqHzpRIHmxDRzVgct4dAQKV2TSlld-7FIfpf6UZ7dujZViFo_lgbv7lAzzTc7JCNI74ouukscBh2kjLGmq1mggbbd45oY7kGTMBvNPx-ChLg1O_8PlZYbphNV5g0lID5JNqa0RaJZ6sFyVZqdTd1u0ujpCaq4PAvdeTceKjjyxeYbX2JTJ5-fMRsxchG1A3e3A3TDdJLQVH-HdWpurMuBRcuBpDz28zi8mJ0kfbnuGehvavagRUqRe1C3OJlm7kMgNu9sedKIMPq1aauNpNLMhC7UNW1j8rOH_I9ucnOLPSIQmsyAs3Sb50DRHAXk3O6y_9Upd53bpXZJDUcZwaIt3kjiqBmeSN7J9YJwdRkEtPSPX2_JfCBQMZnW0lGe4WxCv5bb1MRhqIDUKlzRk7dkioPgGR4O5K1RD2bnjv1t85AJrVm3IGrcdKnoRyspVj6ldBbWsUlvQqO2pJ2cl5RRRO_Z1KIEqJePgiTJSjHFp9qEsx3XWvUyzWKZIzSWROp5SflnFKYhAzkpIIIpDXMTvjIPk1u2k0iCfce78pbjCc_CdJAxjLaX5maVxl4LwJNwgIuYhe4KCpXwHy837NCHKL3eYope8iqqnLicXOCMEn4KUGMMt9tBRXJdqpLCa2sXkTUA6CI253eY5mgMJXwjOqRERZOGac8uVZxhzOmlM7gvmfef8zNjsR0xXjkj2sJHA64t7lRADIZqMvK0aJQ1x1GR72hSjdfybaxCJFCZBuslU-uBBhw5GXMCv2kkoLAhuNGMj5za-3B5mH9icaiv5EDJA_3RSsByBStvrdkPBuxpGhAzkOKTVPrXQHbEqbpldWXe4TJgy8q1uz7xZYBUjJRHGbEh7up21WaKw36_4uIe0R6iWwH2eeAyT3QYdizuc0-hRDn2jTbFgKVFkm058hlWJPTOW7CLVwX6s9RAsmjIwobtliH1XFsaidDHP8kEwBqiKQWh00bON1JTXqMvg2VLgiYzX35AwndiLM-M1eXAkcIh_IYz7MjAbsnYWo8gkWINfHklZJIDhGwAMQvicc8tFkSrCFpv21auPDwdaoZtedmD3rneOWsfU0dE8-lhY1xdZRlPp2nPehpey9p8oililmZmwZc_rNUp6ERs6G_3ek1LtHATGeInUobhDvymXMPic6kaGtraok5NPgXt6dYEZ2MZ5Ut8_QWZ8BsPvZKx0aeTU8NW2iN0OyM0WGkxBMB3z7IygNXipN0GTveuKxIB28PpA-1_9e-l-qIFS9_K2izq9kzxBs_AutdFQHz5ltbpSWWN6jIj5EVj94b7rsVwnyHZA750QTpW_sjrdBcZbIWmdBxAm7nEnptW4bA3xcRVIQMADbsEh61t2WfatKBX3CVgHfIh3yXX6-jJgF9Ig"
APP_KEY = "edl2uiq0plk136y"
APP_SECRET = "np90vhxg46ucesj"

# Base directory for files in Dropbox
BASE_DIR = "/public_notepad"
DEFAULT_NOTE_FILE = f"{BASE_DIR}/notes/default.txt"

# Initialize Dropbox client
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

# Supported file extensions and their descriptions
SUPPORTED_EXTENSIONS = {
    ".txt": "Text File",
    ".md": "Markdown File",
    ".html": "HTML File",
    ".css": "CSS File",
    ".js": "JavaScript File",
    ".json": "JSON File",
    ".py": "Python File"
}

# Get the port number from environment variable
port = int(os.environ.get("PORT", 5000))

# Initialize Dropbox structure if it doesn't exist
def init_dropbox_structure():
    try:
        # Create base directory
        try:
            dbx.files_create_folder_v2(BASE_DIR)
            print(f"Created base directory: {BASE_DIR}")
        except dropbox.exceptions.ApiError:
            # Directory likely exists
            pass
            
        # Create notes directory
        try:
            dbx.files_create_folder_v2(f"{BASE_DIR}/notes")
            print(f"Created notes directory: {BASE_DIR}/notes")
        except dropbox.exceptions.ApiError:
            # Directory likely exists
            pass
    except Exception as e:
        print(f"Error initializing Dropbox structure: {str(e)}")

# Helper function to get file extension
def get_file_extension(filename):
    return os.path.splitext(filename)[1].lower()

# Helper function to check if a file exists
def file_exists(path):
    try:
        dbx.files_get_metadata(path)
        return True
    except dropbox.exceptions.ApiError:
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/files')
def files():
    return render_template('files.html')

@app.route('/api/files', methods=['GET'])
def list_files():
    try:
        result = dbx.files_list_folder(f"{BASE_DIR}/notes")
        files = []
        
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                file_info = {
                    'name': entry.name,
                    'path': entry.path_display,
                    'size': entry.size,
                    'modified': entry.server_modified.strftime("%Y-%m-%d %H:%M:%S"),
                    'extension': get_file_extension(entry.name),
                    'type': SUPPORTED_EXTENSIONS.get(get_file_extension(entry.name), "Unknown")
                }
                files.append(file_info)
                
        return jsonify({"status": "success", "files": files})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error listing files: {str(e)}"})

@app.route('/api/files/<path:filename>', methods=['GET'])
def get_file(filename):
    file_path = f"{BASE_DIR}/notes/{filename}"
    try:
        _, response = dbx.files_download(file_path)
        content = response.content.decode()
        return jsonify({"status": "success", "content": content, "filename": filename})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error loading file: {str(e)}"})

@app.route('/api/files', methods=['POST'])
def create_file():
    data = request.get_json()
    filename = data.get('filename', '')
    
    if not filename:
        return jsonify({"status": "error", "message": "Filename is required"})
    
    # Add file extension if not present
    if not any(filename.endswith(ext) for ext in SUPPORTED_EXTENSIONS.keys()):
        filename += ".txt"
    
    file_path = f"{BASE_DIR}/notes/{filename}"
    
    # Check if file already exists
    if file_exists(file_path):
        return jsonify({"status": "error", "message": "File already exists"})
    
    try:
        # Create an empty file
        dbx.files_upload("".encode(), file_path)
        return jsonify({
            "status": "success", 
            "message": "File created successfully",
            "file": {
                "name": filename,
                "path": file_path,
                "size": 0,
                "modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "extension": get_file_extension(filename),
                "type": SUPPORTED_EXTENSIONS.get(get_file_extension(filename), "Unknown")
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error creating file: {str(e)}"})

@app.route('/api/files/<path:filename>', methods=['PUT'])
def save_file(filename):
    data = request.get_json()
    content = data.get('content', '')
    file_path = f"{BASE_DIR}/notes/{filename}"
    
    try:
        dbx.files_upload(
            content.encode(),
            file_path,
            mode=dropbox.files.WriteMode.overwrite
        )
        return jsonify({"status": "success", "message": "File saved successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error saving file: {str(e)}"})

@app.route('/api/files/<path:filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = f"{BASE_DIR}/notes/{filename}"
    
    try:
        dbx.files_delete_v2(file_path)
        return jsonify({"status": "success", "message": "File deleted successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error deleting file: {str(e)}"})

@app.route('/save', methods=['POST'])
def save_note():
    try:
        content = request.form.get('content', '')
        
        # Better error handling for empty content
        if not content:
            return jsonify({"status": "success"})
            
        dbx.files_upload(
            content.encode(),
            DEFAULT_NOTE_FILE,
            mode=dropbox.files.WriteMode.overwrite
        )
        return jsonify({"status": "success"})
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"status": "error", "message": "An unexpected error occurred"})

@app.route('/load')
def load_note():
    try:
        try:
            _, response = dbx.files_download(DEFAULT_NOTE_FILE)
            content = response.content.decode()
            return jsonify({"status": "success", "content": content})
        except dropbox.exceptions.ApiError as e:
            if isinstance(e.error, dropbox.files.DownloadError) and e.error.is_path():
                # File doesn't exist yet, return empty content
                return jsonify({"status": "success", "content": ""})
            raise
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"status": "error", "message": "An unexpected error occurred"})

if __name__ == '__main__':
    # Ensure Dropbox structure exists
    init_dropbox_structure()
    
    # Run the app on 0.0.0.0 to make it accessible externally
    app.run(host='0.0.0.0', port=port, debug=True)
