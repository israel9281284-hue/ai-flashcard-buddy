import streamlit as st
import httpx

# 1. Page Configuration
st.set_page_config(page_title="AI Flashcard Buddy", page_icon="🧠", layout="centered")
st.title("🧠 AI Flashcard Buddy")
st.subheader("Turn confusing STEM topics into easy flashcards!")

# 2. User Input
user_concept = st.text_input("What STEM topic are you studying today?", placeholder="e.g., Photosynthesis, Gravity, Mitosis")

# 3. AI Logic Function
def ask_ai(prompt_type, topic):
    # We use a completely free text generation API endpoint
    url = "https://text.pollinations.ai/"
    
    if prompt_type == "kid":
        system_prompt = f"Explain the STEM concept '{topic}' like I am a 5-year-old child. Use simple words, analogies, and emojis. Keep it short."
    elif prompt_type == "poem":
        system_prompt = f"Write a catchy, short 4-line rhyming poem to help a student memorize the STEM concept '{topic}'."
    elif prompt_type == "quiz":
        system_prompt = f"Create a short 3-question multiple-choice quiz about '{topic}' with options A, B, C. Provide the correct answers at the very bottom."

    try:
        # Sending the request to the free AI server
        response = httpx.get(f"{url}{system_prompt}")
        if response.status_code == 200:
            return response.text
        else:
            return "Oops! The AI buddy is taking a nap. Try clicking the button again!"
    except Exception as e:
        return "Connection error. Please try again!"

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
