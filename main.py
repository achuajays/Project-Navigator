import streamlit as st
from groq import Groq
import time
import re

# Initialize the Groq client
client = Groq()

# Page configuration with custom theme
st.set_page_config(
    page_title="AI Project Ideas Generator",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS to improve the UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
        background-color: #FF4B4B;
        color: white;
    }
    .project-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Main title with description
st.title("🚀 Project Ideas Generator for Mastery")
st.markdown("""
    Transform your learning journey with personalized project ideas! 
    Enter your desired topic, select the difficulty level and timeframe, 
    and let AI generate tailored project suggestions for you.
""")

# Create two columns for inputs
col1, col2 = st.columns(2)

with col1:
    topic = st.text_input(
        "🎯 Topic",
        placeholder="e.g. Machine Learning",
        help="Enter the main topic you want to learn"
    )

    hardness = st.select_slider(
        "💪 Difficulty Level",
        options=["Beginner", "Easy", "Medium", "Hard", "Expert"],
        value="Medium",
        help="Select the complexity level of projects"
    )

with col2:
    days = st.select_slider(
        "⏱️ Completion Time",
        options=["7", "14", "30", "60", "90"],
        value="30",
        help="Estimated days to complete each project"
    )

    num_projects = st.slider(
        "📚 Number of Projects",
        min_value=1,
        max_value=10,
        value=5,
        help="How many project ideas would you like?"
    )


def format_for_download(markdown_text):
    """Convert markdown headers to plain text with proper formatting"""
    # Remove markdown headers while keeping the text
    clean_text = re.sub(r'^#+\s*', '', markdown_text, flags=re.MULTILINE)

    # Add proper spacing between sections
    clean_text = re.sub(r'\n{3,}', '\n\n', clean_text)

    # Format the text for better readability
    lines = clean_text.split('\n')
    formatted_lines = []

    for line in lines:
        # Add proper indentation for list items
        if line.strip().startswith('- '):
            formatted_lines.append('  ' + line)
        else:
            formatted_lines.append(line)

    return '\n'.join(formatted_lines)


if st.button("🎮 Generate Project Ideas", use_container_width=True):
    if not topic.strip():
        st.error("🚫 Please enter a valid topic to generate project ideas.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i in range(100):
            progress_bar.progress(i + 1)
            status_text.text(f"Generating amazing project ideas... {i + 1}%")
            time.sleep(0.01)

        try:
            prompt = (
                f"Generate {num_projects} unique and creative projects that I can build to master '{topic}'. "
                f"Each project should be designed to be completed in {days} days and should have a '{hardness}' difficulty level. "
                "For each project, provide:\n"
                "1. A catchy title\n"
                "2. A brief but engaging description\n"
                "3. Key learning outcomes\n"
                "4. Main technologies/tools needed\n\n"
                "Format each project nicely with clear sections and make them progressively more challenging. "

            )

            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system",
                     "content": "You are an experienced tech mentor and project ideas generator. Format your response using plain text with clear spacing and organization instead of markdown headers."},
                    {"role": "user", "content": prompt},
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_completion_tokens=1024,
                top_p=1,
                stop=None,
                stream=False,
            )

            progress_bar.empty()
            status_text.empty()

            st.success("🎉 Project ideas generated successfully!")

            response = chat_completion.choices[0].message.content

            # Display formatted markdown version in Streamlit
            st.markdown("---")
            st.subheader("🎯 Your Personalized Project Ideas")
            st.markdown(response)

            # Format the download version without markdown
            download_text = format_for_download(response)

            # Add a download button with cleaned format
            st.download_button(
                label="📥 Download Project Ideas",
                data=download_text,
                file_name=f"{topic}_project_ideas.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("Please try again or contact support if the problem persists.")

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        Made with ❤️ to help you learn better.<br>
        Remember: The best project is the one you'll actually build!
    </div>
""", unsafe_allow_html=True)