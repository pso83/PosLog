from app import app
from routes.routes_programmation import register_routes
import webbrowser
import threading

register_routes(app)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5500")

if __name__ == "__main__":
    # Ouvre le navigateur dans un thread séparé après un petit délai
    threading.Timer(1.5, open_browser).start()
    app.run(host="127.0.0.1", port=5500)
