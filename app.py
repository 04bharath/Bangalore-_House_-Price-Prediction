import pickle as pk
import pandas as pd
import streamlit as st
from pathlib import Path
import os
from PIL import Image

# Load model and data
try:
    model_path = Path('C:/Users/Bharath Kumar/OneDrive/ドキュメント/House_prediction/House_prediction_model.pkl')
    data_path = Path('C:/Users/Bharath Kumar/OneDrive/ドキュメント/House_prediction/Cleaned_data.csv')
    model = pk.load(open(model_path, 'rb'))
    data = pd.read_csv(data_path)
except FileNotFoundError:
    st.error("Model or data file not found. Please check the paths.")
    st.stop()

# App config
st.sidebar.header("📍 Area Information")

image_folder = "C:/Users/Bharath Kumar/OneDrive/Pictures/area_images"

if os.path.exists(image_folder):
    image_files = [file for file in os.listdir(image_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if image_files:
        image_names = [os.path.splitext(file)[0].replace('_', ' ').title() for file in image_files]
        selected_name = st.sidebar.selectbox("Select Area", image_names)
        selected_file = image_files[image_names.index(selected_name)]
        image_path = os.path.join(image_folder, selected_file)
        try:
            img = Image.open(image_path)
            st.sidebar.image(img, use_column_width=True, caption=selected_name)
        except Exception:
            st.sidebar.warning("Couldn't load the selected image.")
    else:
        st.sidebar.info("No images found in 'area_images' folder.")
else:
    st.sidebar.warning("The folder 'area_images' was not found.")

st.sidebar.markdown("""
**Popular Localities:**
- Indiranagar: Urban hub with vibrant nightlife  
- Whitefield: Tech corridor, modern apartments  
- BTM Layout: Budget-friendly, well-connected  
- Electronic City: IT hubs, affordable housing  
- 8th Phase JP Nagar: Quiet residential area with growing infrastructure
- Balagere: Emerging suburb, close to Varthur and Whitefield
- Banashankari Stage VI: Peaceful, green, and family-friendly
- Bannerghatta Road: Lively stretch with malls, hospitals, and schools
- Begur Road: Affordable homes with proximity to IT hubs
- Bommanahalli: Budget housing, near BTM and Silk Board
- Budigere: Upcoming residential zone with plotted developments
- Chandapura: Affordable housing, near Electronic City
- Devanahalli: Airport hub, hotspot for future growth
- EPIP Zone: IT and business district in Whitefiel
- Electronic City Phase II: Major IT companies, better road
- Electronics City Phase 1: Tech parks, startups, and hostels
- Harlur: Premium apartments, near Sarjapur Road
- Hebbal: Well-connected, lake views, flyover access
- Hennur: Green neighborhood, new residential projects
- Hennur Road: Fast-growing with good access to the airport
- Hoodi: Near ITPL, mix of commercial and residential space
- Hormavu: Budget apartments, schools, and quiet lanes
- Hosa Road: Affordable flats, near Electronic City
- Hoskote: Plotted development hotspot, highway access
- Hosur Road: Industrial and residential stretch to TN border
- Hulimavu: Developing suburb, close to Bannerghatta Road
- ITPL: Established IT zone with high-rise apartments
- Iblur Village: Central junction, near Outer Ring Road
- JP Nagar: Premium residential zone with great amenities
- Jakkur: Green cover, known for Jakkur Aerodrome
- Jalahalli: Industrial + serene, with good metro access
- Jalahalli East: Quiet defense area, tree-lined streets
- KR Puram: Railway connectivity, gateway to Whitefield
- Kadugodi: Residential hub near ITPL with metro access
- Kammasandra: Quiet enclave, close to Hosur Road
- Kanakapura: Green stretch with plotted layouts
- Kanakpura Road: Fast-developing with metro connectivity
- Kengeri Satellite Town: Affordable housing and metro link
- Magadi Road: Old Bangalore charm, good metro access
- Mysore Road: Busy corridor with commercial developments
- Old Madras Road: Commercial stretch, access to East Bangalore
- Panathur: Tech-accessible, near Outer Ring Road
- Rachenahalli: Lake-side living, growing infrastructure
- Rajaji Nagar: Well-established, mix of old and new
- Sarjapur: Suburban area with upcoming infrastructure
- Sarjapur Road: IT corridor, premium residential projects
- Sonnenahalli: Quiet and affordable, near airport road
- Talaghattapura: Residential locality with green surroundings
- Thanisandra: Rapidly urbanizing with premium apartments
- Tumkur Road: Industrial corridor with affordable plots
- Uttarahalli: Traditional locality, good schools
- Varthur Road: Close to Whitefield, bustling with new apartments
- Whitefield: IT corridor, malls, and cosmopolitan vibe
- Yelahanka: Clean, spacious, and close to the airport
- Yeshwanthpur: Metro-connected, major transit hub                   
""")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your Bangalore House Price Assistant. 🏡\n\nI can help estimate property prices in Bangalore. To get started, could you tell me which location you're interested in?"}
    ]

if 'input_features' not in st.session_state:
    st.session_state.input_features = {
        'location': None,
        'total_sqft': None,
        'bedrooms': None,
        'bath': None,
        'balcony': None
    }

# Functions
def format_price(price):
    price = float(price) * 100000
    if price >= 10000000:
        return f"₹{price/10000000:,.2f} crores"
    elif price >= 100000:
        return f"₹{price/100000:,.2f} lakhs"
    else:
        return f"₹{price:,.2f}"

def predict_price():
    input_df = pd.DataFrame([[st.session_state.input_features['location'],
                               st.session_state.input_features['total_sqft'],
                               st.session_state.input_features['bath'],
                               st.session_state.input_features['balcony'],
                               st.session_state.input_features['bedrooms']]],
                             columns=['location', 'total_sqft', 'bath', 'balcony', 'bedrooms'])
    output = model.predict(input_df)
    return format_price(abs(output[0]))

# Chat interface
st.title("🏡 Bangalore House Price Predictor Chatbot")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Determine missing info
    missing_info = []
    if not st.session_state.input_features['location']:
        missing_info.append('location')
    elif not st.session_state.input_features['total_sqft']:
        missing_info.append('total_sqft')
    elif not st.session_state.input_features['bedrooms']:
        missing_info.append('bedrooms')
    elif not st.session_state.input_features['bath']:
        missing_info.append('bath')
    elif not st.session_state.input_features['balcony']:
        missing_info.append('balcony')

    if missing_info:
        current_question = missing_info[0]

        if current_question == 'location':
            mentioned_locations = [loc for loc in data['location'].unique() if loc.lower() in prompt.lower()]
            if mentioned_locations:
                st.session_state.input_features['location'] = mentioned_locations[0]
                assistant_response = f"Great! You're interested in {mentioned_locations[0]}. What's the total square footage of the property? 📏"
            else:
                assistant_response = "I couldn't identify that location. Please select from these areas:\n\n" + \
                                     ", ".join(sorted(data['location'].unique())) + \
                                     "\n\nWhich location are you interested in?"

        elif current_question == 'total_sqft':
            try:
                numbers = [int(s) for s in prompt.split() if s.isdigit()]
                if numbers:
                    sqft = numbers[0]
                    if 300 <= sqft <= 10000:
                        st.session_state.input_features['total_sqft'] = sqft
                        assistant_response = f"Got it! {sqft} sqft. How many bedrooms does the property have? 🛏️"
                    else:
                        assistant_response = "Please enter a reasonable square footage (300–10,000 sqft)."
                else:
                    assistant_response = "Please enter the total square footage as a number (e.g., 1500)."
            except:
                assistant_response = "Please enter the total square footage as a number (e.g., 1500)."

        elif current_question == 'bedrooms':
            try:
                numbers = [int(s) for s in prompt.split() if s.isdigit()]
                if numbers:
                    beds = numbers[0]
                    if 1 <= beds <= 10:
                        st.session_state.input_features['bedrooms'] = beds
                        assistant_response = f"{beds} bedrooms noted. How many bathrooms? 🚿"
                    else:
                        assistant_response = "Please enter a reasonable number of bedrooms (1–10)."
                else:
                    assistant_response = "Please enter the number of bedrooms as a number (e.g., 2)."
            except:
                assistant_response = "Please enter the number of bedrooms as a number (e.g., 2)."

        elif current_question == 'bath':
            try:
                numbers = [int(s) for s in prompt.split() if s.isdigit()]
                if numbers:
                    baths = numbers[0]
                    if 1 <= baths <= 10:
                        st.session_state.input_features['bath'] = baths
                        assistant_response = f"{baths} bathrooms noted. Finally, how many balconies does the property have? 🌿"
                    else:
                        assistant_response = "Please enter a reasonable number of bathrooms (1–10)."
                else:
                    assistant_response = "Please enter the number of bathrooms as a number (e.g., 2)."
            except:
                assistant_response = "Please enter the number of bathrooms as a number (e.g., 2)."

        elif current_question == 'balcony':
            try:
                numbers = [int(s) for s in prompt.split() if s.isdigit()]
                if numbers:
                    balconies = numbers[0]
                    if 0 <= balconies <= 5:
                        st.session_state.input_features['balcony'] = balconies

                        # All info collected
                        price = predict_price()
                        inputs = st.session_state.input_features
                        assistant_response = f"""
Thanks! Here's the summary of your input:

- 📍 **Location**: {inputs['location']}
- 📏 **Total Sqft**: {inputs['total_sqft']}
- 🛏️ **Bedrooms**: {inputs['bedrooms']}
- 🚿 **Bathrooms**: {inputs['bath']}
- 🌿 **Balconies**: {inputs['balcony']}

💰 **Estimated Price: {price}**

Would you like to check another property? (Type 'yes' or 'no')
"""
                    else:
                        assistant_response = "Please enter a reasonable number of balconies (0–5)."
                else:
                    assistant_response = "Please enter the number of balconies as a number (e.g., 1)."
            except:
                assistant_response = "Please enter the number of balconies as a number (e.g., 1)."
    else:
        # Already collected everything
        if "yes" in prompt.lower():
            st.session_state.input_features = {k: None for k in st.session_state.input_features}
            assistant_response = "Great! Let's estimate another property. Which location are you interested in?"
        elif "no" in prompt.lower() or "thanks" in prompt.lower():
            assistant_response = "You're welcome! Feel free to come back anytime. Have a great day! 😊"
        else:
            assistant_response = "I'm not sure I understand. Would you like to check another property? (yes/no)"

    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

# Reset button
if st.button("🔄 Start New Conversation"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your Bangalore House Price Assistant. 🏡\n\nI can help estimate property prices in Bangalore. To get started, could you tell me which location you're interested in?"}
    ]
    st.session_state.input_features = {k: None for k in st.session_state.input_features}
    st.rerun()
