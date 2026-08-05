# Textbased Characther Creator!

![Static Badge](https://img.shields.io/badge/Converting%20sheets%20to%20codes-6.17%25-blue?style=for-the-badge)
![Static Badge](https://img.shields.io/badge/Detailing%20Guides%20-0%25-blue?style=for-the-badge)


A simple (if you can say) text-based character creator.
This project is just the implementation of various reference i got online of characther creator sheets (*which i forgot where i got it, and will mention it when possible*).

Initially made for my own worldbuilding projects, but found it useful! Previosly made as Excel and Google Form, but i learned programming lately.

Also join Astrocosmos!

## Feature

- **Detailed character form**, or make a simple and compact one!
- **Characters' data are stored in JSON**, and can be bundled with other information such image (and, coming soon, text) in a ZIP!

Planned feature can be seen in [Plans document](/docs/plans.md)

### Privacy

All the things you uploaded to the [] interface are safe and stored in your device cache. 
This is done by the `streamlit`'s code `session_state` written in [one of the script](.src/ui/_streamlit/characthercreator/__init__.py) as shown below

```python
# Store uploaded  character data in session state
if "character" not in st.session_state:
    st.session_state.character = base.CharacterData()

# Store uploaded assets bytes in session state
if "pending_assets" not in st.session_state:
    st.session_state.pending_assets = {}
```

## Usage

if you are familiar with programming, you can use the Jupyter Notebook file in the [`ipynb/` folder](/ipynb/APP.ipynb)

If you want a more friendly interface, you can go to the pinned site here

**Installation**. The executable program version of this project is not yet (or possible will be never) available. For the mean time, use the web-app.

## Miscellaneous

**LICENSE**. currently, This software is licensed under "i'm so tired" software license 1.0 (no resale ver.)

**CONTRIBUTING**.

