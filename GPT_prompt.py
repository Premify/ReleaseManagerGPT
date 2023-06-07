import pandas as pd
import streamlit as st
from collections import defaultdict
from streamlit.components.v1 import html

def open_page(url):
    # Generate a unique timestamp to append to the URL
    timestamp = pd.Timestamp.now().strftime('%Y%m%d%H%M%S')

    open_script= """
        <script type="text/javascript">
            window.open('%s?%s', '_blank').focus();
        </script>
    """ % (url, timestamp)
    html(open_script)


# Function to process the CSV file and generate the release notes
def process_release_notes(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Define the mapping of categories to sections
    mapping = {
        'New feature': 'New features',
        'Improvement': 'Improvements',
        'API': 'Improvements',
        'Bug fix': 'Bug fixes',
        'Removal': 'Removals',
    }

    # Initialize a dictionary to hold the notes
    notes = defaultdict(list)

    # Populate the dictionary with the notes
    for _, row in df.iterrows():
        notes[mapping[row['Benutzerdefinierte Felder (Release Notes Category)']]].append(
            row['Benutzerdefinierte Felder (Release Notes)'])

    # Generate the release notes
    release_notes = "Now I will give you some raw unedited release notes.\n\nIn your revised drafts of the release notes, please avoid using first-person plural phrases such as 'we've fixed', 'we've added', 'we've improved', etc. The revised notes should maintain a neutral tone and focus on the changes themselves, not who implemented them. Describe the changes as facts or actions that have occurred, rather than actions performed by the development team. Also keep the [Module...] part at the beginning of the sentence if available.\n\n"
    release_notes += "Table structure (Make sure to set a heading for each used category heading - the heading should be highlighted in bold.):\n"
    release_notes += "1. Column: Release note => Just copy the given release note text here\n"
    release_notes += "2. Column: Rating => Rate the release note by 0 - 10, according to what you've learned about the writing style and the given examples before\n"
    release_notes += "3. Column: Suggestions => List everything that you would change about it\n"
    release_notes += "4. Columns: Create a new draft for the release note without changing the core message of the release note. You can rewrite the release note by applying what you've learned from the style guide and examples without losing or altering the core message of the text.\n\n"

    for category, items in notes.items():
        release_notes += f"{category}:\n"
        for item in items:
            if pd.isnull(item):
                release_notes += "- MISSING\n"
            else:
                release_notes += f"- {item}\n"
        release_notes += "\n"

    return release_notes

# Streamlit app
def main():
    st.title("Release Notes Prompt Creator")

    # File upload
    csv_file = st.file_uploader("Upload a CSV file")

    if csv_file is not None:
        # Process the uploaded CSV file
        release_notes = process_release_notes(csv_file)

        # Display the release notes in a text area
        st.text_area("Processed Release Notes", value=release_notes, height=400)

        # Button for ChatGPT link
        st.button('Open GPT', on_click=open_page, args=('https://chat.openai.com/share/eda2e5e1-7b44-41d6-b4f1-96bf28c34aaf',))



# Run the Streamlit app
if __name__ == "__main__":
    main()
