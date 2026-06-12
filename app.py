import streamlit as st
import urllib.request
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="AI Flashcard Buddy", page_icon="🧠", layout="centered")
st.title("🧠 AI Flashcard Buddy")
st.subheader("Turn confusing STEM topics into easy flashcards!")

# 2. User Input
user_concept = st.text_input("What STEM topic are you studying today?", placeholder="e.g., Photosynthesis, Gravity, Mitosis")

# 3. Upgraded Robust AI Logic Function
def ask_ai(prompt_type, topic):
    base_url = "https://text.pollinations.ai/"
    
    if prompt_type == "kid":
        system_prompt = f"Explain the STEM concept '{topic}' like I am a 5-year-old child. Use simple words, analogies, and emojis. Keep it short."
    elif prompt_type == "poem":
        system_prompt = f"Write a catchy, short 4-line rhyming poem to help a student memorize the STEM concept '{topic}'."
    elif prompt_type == "quiz":
        system_prompt = f"Create a short 3-question multiple-choice quiz about '{topic}' with options A, B, C. Provide the correct answers at the very bottom."

    try:
        # Safely encode the prompt so spaces and special characters are valid url characters
        encoded_prompt = urllib.parse.quote(system_prompt)
        full_url = f"{base_url}{encoded_prompt}"
        
        # We add clear headers so the AI endpoint accepts the web request from Streamlit's server
        req = urllib.request.Request(
            full_url, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
        )
        
        # Open connection and grab response
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
            
    except Exception as e:
        # If something drops, we give a friendly message
        return "The AI buddy is a bit busy right now. Please try clicking the button again!"

# 4. Action Button Logic
if st.button("✨ Create My Flashcards"):
    if user_concept.strip() == "":
        st.warning("Please type a word first!")
    else:
        with st.spinner(f"🧠 Brainstorming flashcards for '{user_concept}'..."):
            
            # Generate the three versions from the AI
            kid_version = ask_ai("kid", user_concept)
            poem_version = ask_ai("poem", user_concept)
            quiz_version = ask_ai("quiz", user_concept)
            
            # Display results in beautiful interactive tabs
            tab1, tab2, tab3 = st.tabs(["👶 5-Year-Old Mode", "🎵 Memory Poem", "❓ Quick Quiz"])
            
            with tab1:
                st.markdown(f"### 👶 Explaining {user_concept} simply:")
                st.write(kid_version)
            with tab2:
                st.markdown("### 🎵 Catchy Memory Poem:")
                st.write(poem_version)
            with tab3:
                st.markdown("### ❓ Test Your Knowledge:")
                st.write(quiz_version)
