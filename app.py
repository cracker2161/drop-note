from flask import Flask, render_template, request, jsonify
import dropbox
import os

app = Flask(__name__)

DROPBOX_ACCESS_TOKEN = "sl.u.AFkRl4YyW-LQKSP8-bHu3YHO-TE2dcHDYPXiw36ftno2PZMYJogYTyZAHWksgDxU2T3lvqj49-hRup5ZkwnfqIioCRPy6wx1Qy29_j4AXO11GLtMfbujDFA4TdboqeCxHVULKAz3SxgxQUNGPjBsQrvwHrIKqFI5CmlRigBuwNYSB0TJwV4enOhlUlIlNdRrG9bKEjZkX2F5yX-8LPe8xpERqfqYZKWR8SiQKYMRWTK_br9i9y1nghGqy2kjAD86XjwF1BvntXfqE3R03PdKNfpHdwIjibkh4AIzxGm6erse_CLOEJd6q42Zzujq-8jYJgmwujaTxhEiTJJxWZfcnO_p0Gyq2gthxXI4AeMOfL9ADJ2Z0fyFcc3kfnXSu7hr26FNLc9kWjZEohLP4lS8foyGobscVbkTeZ3jjLEZdjknOJN9N5Y6MuObfKupSMrLQzKFW-Yj1D2i0BL621a68RBlU9yVRpAqOZUjcOwwYQ0WmbtZnqCNFYWMsCbvvXI7HNBUD9vClRybk-s_KAI-sVFExi1zPKSSrK7qKnx3o0H3JNQm5Qkqas_UrlKYt1-pm7H9oCQNi8cmetSYgc7V-Knn9ia1TOqZFncPe5R5IF24kLbzDG-iiTi_5ieYG3vWK259Rx-CWlEoR12860rx-OEXsIjuecETpnECtFmPEi5Bk92oU9cN4a-1HUQqytB-vZ2tFnSlIq9-owDSLo6YAEjMx3frLQAA3osey0fNuVsMor8wxF7AVlVwZw-lDt58eGUggfwQlm39EhlcqbbcYhi4CB9vjRz0Lg1zSPyU7TnUgJPq3QF9akNzBv68bVhauhYO25iG6wsX7J4wt6aR_Kp01HsRMYGAT0i24TYtaSeaDLoTAXFHxfGcCu2HKkYQ_UFO1hJMpPgEII7JZDINWfIJ7R6mBkvWtweK0T0r4cjhWWgojvTSQnQP55e9uIA0BJ6ej1ZxFKuWpsDqjivrqKEonhYV6EPzl42S3VKc2AXqetmAUOZathVcU22PfrY7Ns_XDpsYCifHQo7xcodFheLfoFXhce_HUrdEVSenqMoH8MxhOPTSV-Svq5oNG9uKVPjKebbN3nYoOxeVZ_dUmrfmV2pZ5chO6RfU_Og9_CsbBnKUSYZWlEV1_uQCyCshJO1uUh3ToXE2GmsQmCUzwfKTEZWb4D0m_HfCyR5ERLnJuCKOWtBKTMGcLvz4gnNNNARsrvRDFKkOfGyV8TRbv24N8ErKYOwDeFK6KnDdJCjcmvqx0k-HfEd54jsd7y727x6zaNDj_LKrcpICL1aBTStKDZke9bUGNd7PvSJKVwifQMDgkNXeNmWyXI44aW5xF7cWPytIOLxYQd4v41LRbPJwXt3KkrG9LppVvu2sjxDiK4OGxSj5XNvzZF78Gk5V3K3_Uc0w90AwutBYpkrPlxiXgDgPicX3djsfSPuDyRJY2w"
APP_KEY = "drbgse46n55ttxu"
APP_SECRET = "fgrp31yx25seo55"

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
        content = request.form.get('content')
        dbx.files_upload(
            content.encode(),
            FILE_PATH,
            mode=dropbox.files.WriteMode.overwrite
        )
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/load')
def load_note():
    try:
        _, response = dbx.files_download(FILE_PATH)
        content = response.content.decode()
        return jsonify({"status": "success", "content": content})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    # Run the app on 0.0.0.0 to make it accessible externally
    app.run(host='0.0.0.0', port=port)
