import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="AI Flashcard Buddy", page_icon="🧠", layout="centered")
st.title("🧠 AI Flashcard Buddy")
st.subheader("Turn confusing STEM topics into easy flashcards!")

# 2. User Input
user_concept = st.text_input("What STEM topic are you studying today?", placeholder="e.g., Photosynthesis, Gravity, Mitosis")

# 3. Rock-Solid AI Connection Function
def ask_ai(prompt_type, topic):
    if prompt_type == "kid":
        prompt = f"Explain the STEM concept '{topic}' like I am a 5-year-old child. Use simple words, analogies, and emojis. Keep it short."
    elif prompt_type == "poem":
        prompt = f"Write a catchy, short 4-line rhyming poem to help a student memorize the STEM concept '{topic}'."
    elif prompt_type == "quiz":
        prompt = f"Create a short 3-question multiple-choice quiz about '{topic}' with options A, B, C. Provide the correct answers at the very bottom."

    try:
        # Using a reliable public text endpoint
        url = f"https://text.pollinations.ai/{prompt}"
        
        # We send standard browser headers so Streamlit doesn't get blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            return response.text
        else:
            return "The AI buddy is taking a quick break. Tap the button again!"
            
    except Exception as e:
        return "Network glitch! Give it another try."

# 4. Action Button Logic
if st.button("✨ Create My Flashcards"):
    if user_concept.strip() == "":
        st.warning("Please type a word first!")
    else:
        with st.spinner(f"🧠 Brainstorming flashcards for '{user_concept}'..."):
            
            # Generate the three versions
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
