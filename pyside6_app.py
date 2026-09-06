from src.ui.pyside6 import entry

# Start Streamlit server in the background
script_path = "streamlit_app.py"  # Replace with your Streamlit script filename

entry.run_pyside(script_path=script_path)
