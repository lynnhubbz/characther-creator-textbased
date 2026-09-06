import sys
import subprocess
import os
import atexit
from PySide6 import QtCore, QtWidgets
from PySide6.QtWebEngineWidgets import QWebEngineView


def run_pyside(script_path):
    # Start Streamlit server in headless mode (stops it from opening a browser tab)
    server_process = subprocess.Popen([
        "streamlit", "run", script_path, 
        "--server.headless", "true"
    ])


    # Ensure the server is killed when Python exits
    def cleanup_server():
        server_process.terminate()

    atexit.register(cleanup_server)

    # Initialize PySide6 application
    app = QtWidgets.QApplication(sys.argv)

    # Create a WebEngine view to display the Streamlit app
    view = QWebEngineView()
    view.load(QtCore.QUrl("http://localhost:8501"))
    view.resize(1024, 768)
    view.show()

    # Run the Qt application loop
    sys.exit(app.exec())
