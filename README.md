# Textbased Characther Creator!

A simple (if you can say) text-based character creator.

## Feature

### Privacy

All the things you uploaded to the [] interface are safe and stored in your device cache. 
This is done by the `streamlit`'s code `session_state` written in [one of the script](.src\ui\_streamlit\characthercreator\__init__.py) as shown below

```python
# Store uploaded  character data in session state
if "character" not in st.session_state:
    st.session_state.character = base.CharacterData()

# Store uploaded assets bytes in session state
if "pending_assets" not in st.session_state:
    st.session_state.pending_assets = {}
```

## Getting Started

## Usage

if you are familiar with programming, you can use the Jupyter Notebook file in the [`ipynb/` folder](/ipynb/APP.ipynb)

You can make the set

## Goals

Update 0

1. [X] show json result for ui
2. [X] Zipping Json + image
   1. [X] Zip directory map preview
3. Detailing input
   1. Apply settings
   2. Multiple short answer input as item list
4. Export option
   1. Introduce import
   2. Options and feature for Long answer as docs/.txt
   3. Tidy it up
   4. add suggestion textto convert the json at <https://markdownme.com/tools/config-converter>

Update 1

0. Documentation
   1. Adding and complete the documents for the whole project <https://markdownme.com/github>
   2. Add logo: script and quill
   3. Add image so user can better imagine it
1. Immersive multichoice input for ui
2. Randomizer Generator

Update 2

4. Translation
5. Worldbuilding tool compat
   1. Chronicler
6. Firgure out plugins
7. embed typst for pdfs