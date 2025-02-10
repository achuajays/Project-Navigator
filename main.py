import streamlit as st
from groq import Groq

# Initialize the Groq client
client = Groq()

# Set up the Streamlit page
st.set_page_config(page_title="Project Navigator", layout="centered")
st.title("Project Ideas Generator for Mastery")
st.write("Enter a topic and select the desired project difficulty and completion time, then get 5 project ideas!")

# Input field for the topic
topic = st.text_input("Topic", placeholder="e.g. Machine Learning")

# Dropdown for hardness level
hardness = st.selectbox("Select Hardness Level", options=["Easy", "Medium", "Hard"])

# Dropdown for the number of days
days = st.selectbox("Select Completion Time (in days)", options=["7", "14", "30", "60"])

if st.button("Generate Projects"):
    if not topic.strip():
        st.error("Please enter a valid topic.")
    else:
        with st.spinner("Generating project ideas..."):
            # Build the prompt for the AI including the new parameters
            prompt = (
                f"Generate a list of 5 projects that I can build to master the topic '{topic}'. "
                f"Each project should be designed to be completed in {days} days and should have a '{hardness}' level of difficulty. "
                "For each project, provide a title and a brief description."
            )
            try:
                # Create a chat completion request using Groq
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt},
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.5,
                    max_completion_tokens=1024,
                    top_p=1,
                    stop=None,
                    stream=False,
                )

                # Extract and display the response
                response = chat_completion.choices[0].message.content
                st.subheader("Project Ideas")
                st.markdown(response)

            except Exception as e:
                st.error(f"An error occurred while generating project ideas: {e}")
