from flask import Flask
app = Flask(__name__)

import imgmm.views


if __name__ == "__main__":
    # load_imgs()
    # Prevent multiple browser windows being opened because of code reloading
    # when Flask debug is active
    if "WERKZEUG_RUN_MAIN" not in os.environ:
        threading.Timer(1, lambda: webbrowser.open(APP_URL)).start()
    app.run()
