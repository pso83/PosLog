from app import app
import webbrowser
import threading

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5500")

if __name__ == "__main__":
    # Ouvre le navigateur dans un thread séparé après un petit délai
    threading.Timer(1.5, open_browser).start()
    app.run(host="127.0.0.1", port=5500)
