from src.ui._streamlit.entry import *

import importlib
from src.ui._streamlit import entry

st.set_page_config(initial_sidebar_state="locked", layout="wide")

entry.render()
