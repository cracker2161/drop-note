from flask import Flask, render_template, request, jsonify
import dropbox
import os

app = Flask(__name__)

DROPBOX_ACCESS_TOKEN = "sl.u.AFgxEHEW0o_aFBdmh25VSMbOS9mo-Rhvpmf4C3DQV__vN7ftaAM_6CYzxuNBqoMIWykLc8S24GzWelA_qQtOKpBVdwXUuEWJV8eesBGUziUJWKn3fe9QyzKLsqA6RTzmaGZktc7CUqEXiSmZrbBvplY5Zm71mDEmq5wCN36OGJf9QpJ1h7azI8s7WPNSZ0jGlOWeYv9xUNNh5qePl8TF_ZxLhqjo3XIwUF3oKPVJy2UNLjbsxGVnxtTQuoJI063QoryTWUPp-HTyQGrSDnxeJxfMsoZGEDE3tN4FO_x4Nzi0CiorUQyEHP-8UE7xzZnSozclgV5Wze736KPx55lnAqHub_MocZBMw4MtXiq4oA5g0vR9yneq1UxtuSknr1rRD0B7dppaSiSI24A51OD0d-eO12Vtd1Vqn79ozCzR4dlnjDfcrNdVCQHLmYqdCwB-AqrSd5pJCcyp6jKKPNTuauPTwgRZN_fFhMM48LnNOhv66IHRbp0-IwLBls672yVa0i3TI5289F6DMPgeSzNSbnKnAfZRV31IlVOga1qBB5DPEtFctrPvA2zwJ6VqRFT7VMPXUqSNbkpp5hBUf4TEKudiOhVqU5YDv0k5ivl5u8uyTSoZl0izZ_M791V0aWdxsH2M3KRKsUC5WSNeQBdzCA_GtFINZA2aJqWUt3lIWjyIIJeKJjoqjJvT7z8EphoKSOhY3ikXA6kMrx3wAYDykNLwzV0jU4PlCBRAhiBuzYE6YKJ6FJN7KwGfBFkdZB0aBknX-TUgzG0rYztapVWOWNIvVVBRQ4UyhRFl8NBw4Lun6raDCW8rRs-jZul9z_TyLL9RzoddDVPw1VG0lsNKiz6JpiAjt_bHmnHfYBIeNGaNYa4y_PSR-2Bx5eTmt27icIAvcZGEa8VfnQXIx0SJdppx4dcd8q4PynNWYBSq25LkPfPHipiIfbAqEEaPdGp3WVWRVzo40F5giQ_l2GZzl2zBT5K1Y3zwVXrfqDE21h6Bxs_va6DUkUoYRUHy_UvosrWORsvSrblPS42PhxzuSOLAZkADZA7w6QTFCsvKNeYk3XBkySoVDu43oefqFn1M669eVUkasmGUm2Sw18cSSbkih5Vt-NnL1e-r0CWKp_o9dpUQ7G8MvD2jb-V2xxIJLHIG_smmAWBgBePfMm986IcomXj0KljTse39YGSdTp456TlNDQb_H_avIuQ9lzwbLZlSyXV-Q34t5vjmDpKW6qMcPmKk90KeX1IvbCE0roPph4qwgE_R02LM6MKiKvve4wTnFMkzRkEY5XQ6Iv_YtQhAFbJ4mvRa-hjoBHpio_tXJ6rsycdYbJ5KjyBmMKdyj8lBNUPl0FWdMMCkOomueSzeS1jsBrgtSxlcLgCNTTr10dNdCMJR3QO5jDPUf2-iGe8TY9cH3hJhy74gU8Dt5lA-diYlLPflcBMmWc3KLD4xPw"
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
