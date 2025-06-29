import streamlit as st
import json
import os
import pandas as pd

data_file = 'medical_flower_data.json'

def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)

data = load_data()

st.set_page_config(page_title='Cannabis-Based Medicines Tracker', layout='wide')

st.title('Cannabis-Based Medicines Tracker')

st.markdown("""
Use this tool to track your **cannabis-based medicines**, including manufacturer, cultivar, symptoms you're medicating for, and effectiveness.
""")

manufacturers = [  # FULL LIST FROM YOUR PROVIDED DATA
    '4C Labs Ltd.', 'All Nations Mestiyexw Holdings', 'Althea MMJ UK Ltd', 'Dispensed Pty Ltd.', 'Aurora Europe GmbH',
    'Castle Rock Farms Inc.', 'Big Narstie Medical Ltd', 'Habitat Life Sciences Inc.', 'Ampyl Sciences Ltd', 'MediCann Ltd',
    'Canopy Growth Corp', 'Cellen Biotech Ltd', 'Clearleaf Ltd', 'CP Medical', 'Montu Group Pty Ltd.', 'Crop Circle Dispensary Ltd.',
    'Cookies Creative Productions & Consulting Inc.', 'Curaleaf Holdings Inc', 'Dalgety Ltd', 'Dispensed Labs', 'DOE Medical Ltd.',
    'Doja Medical', 'Prime Pot Inc.', 'ECS Pharma Ltd', 'Endopure Medical Ltd', 'Find', 'Four20 Pharma', 'Glass Pharms Ltd',
    'Grow Lab Organics Ltd', 'Grassroots™', 'Green Joÿ', 'Green Karat', 'Green Organic Dutchman™', 'Grow® Pharma', 'Herdade das Barrocas',
    'Hexacan®', 'Hilltop Leaf', 'Indigo Horizon®', 'Khiron Life Sciences Corp', 'Little Green Pharma', 'Lot420', 'Lumir®', 'Mamedica®',
    'MCCN', 'MedCan', 'Medicus', 'Miracle Valley Canada', 'Muzo™', 'Mystery Mountain™', 'Noidecs', 'Oceanic Releaf', 'Orange Hill Traders',
    'Origine Nature', 'Ostara', 'Papers™', 'Peace Naturals®', 'Phant', 'Plantations Ceres', 'PLF Pharma', 'The Plug Medical Group',
    'Primacann', 'Pure Sunfarms™', 'Qwest', 'Releaf®', 'Roxton Air', 'Rua Bioscience', 'Sherbinskis®', 'Shrubs', 'Sitka Legends',
    'Somaí Pharmaceuticals', 'SUMO', 'Superseed', 'Sundaze®', 'Terpz', 'Therismos', 'Tilray®', 'Tyson 2.0', 'Upstate', 'Wellford', 'Vasco'
]

cultivars = [  # FULL LIST FROM YOUR PROVIDED DATA
    '4C Labs', 'All Nations', 'Althea', 'Altmed', 'Aurora', 'BC Green', 'Big Narstie Medical', 'Cake & Caviar',
    'CannFX', 'CannyCann', 'Canopy Growth', 'Cellen', 'Clearleaf', 'CP Medical', 'Craft Botanics', 'Crop Circle Therapeutics',
    'Cookies®', 'Curaleaf', 'Curo', 'Dalgety', 'Dispensed Labs', 'DOE Medical', 'Doja Medical', 'EastCann', 'ECS Pharma',
    'Endopure', 'Find', 'Four20 Pharma', 'Glass Pharms', 'GLO', 'Grassroots™', 'Green Joÿ', 'Green Karat', 'Green Organic Dutchman™',
    'Grow® Pharma', 'Herdade das Barrocas', 'Hexacan®', 'Hilltop Leaf', 'Horizon', 'Khiron', 'Little Green Pharma', 'Lot420',
    'Lumir®', 'Mamedica®', 'MCCN', 'MedCan', 'Medicus', 'Miracle Valley Canada', 'Muzo™', 'Mystery Mountain™', 'Noidecs',
    'Oceanic Releaf', 'Orange Hill Traders', 'Origine Nature', 'Ostara', 'Papers™', 'Peace Naturals®', 'Phant', 'Plantations Ceres',
    'PLF Pharma', 'The Plug', 'Primacann', 'Pure Sunfarms™', 'Qwest', 'Releaf®', 'Roxton Air', 'Rua Bioscience', 'Sherbinskis®',
    'Shrubs', 'Sitka Legends', 'Somaí', 'SUMO', 'Superseed', 'Sundaze®', 'Terpz', 'Therismos', 'Tilray®', 'Tyson 2.0', 'Upstate',
    'Wellford', 'Vasco'
]

with st.sidebar:
    st.header("Options")
    if st.button('Add New Entry'):
        st.session_state['adding'] = True
    if st.button('Analyse Reviews'):
        st.session_state['analysing'] = True

if st.session_state.get('adding'):
    with st.form('new_entry_form', clear_on_submit=True):
        strain = st.text_input('Strain Name')

        manufacturer = st.selectbox('Manufacturer (Searchable)', options=manufacturers)
        cultivar = st.selectbox('Cultivar (Searchable)', options=cultivars)

        product_type = st.selectbox('Medication Format', [
            'Bud/Flower', 'Sublingual Oil', 'Vape Cartridge', 'Pill/ Capsule',
            'Edible', 'Topical', 'Oral Spray', 'Inhaler', 'Patch'
        ])

        thc = st.number_input('THC %', 0.0, 100.0)
        cbd = st.number_input('CBD %', 0.0, 100.0)
        terpenes = st.text_input('Terpene Profile')
        price = st.number_input('Price (£)', 0.0)
        quantity = st.number_input('Quantity Ordered (g/ml)', 0.0)

        st.markdown("### Primary Symptoms Treated")
        anxiety_level = st.slider('Anxiety Level (1-10)', 1, 10)
        anxiety_notes = st.text_area('Anxiety Notes')
        muscular_pain_level = st.slider('Muscular Pain Level (1-10)', 1, 10)
        muscular_pain_notes = st.text_area('Muscular Pain Notes')
        joint_pain_level = st.slider('Joint Pain Level (1-10)', 1, 10)
        joint_pain_notes = st.text_area('Joint Pain Notes')
        nerve_pain_level = st.slider('Nerve Pain Level (1-10)', 1, 10)
        nerve_pain_notes = st.text_area('Nerve Pain Notes')

        st.markdown("### Secondary Symptoms")
        mood_level = st.slider('Mood Improvement (1-10)', 1, 10)
        mood_notes = st.text_area('Mood Notes')
        appetite_level = st.slider('Appetite (1-10)', 1, 10)
        appetite_notes = st.text_area('Appetite Notes')
        motivation_level = st.slider('Motivation (1-10)', 1, 10)
        motivation_notes = st.text_area('Motivation Notes')

        effectiveness_rating = st.slider('Overall Effectiveness (1-10)', 1, 10)

        notes = st.text_area('General Notes (Reviews/Reddit/Discord)')
        personal_notes = st.text_area('Personal Experience Notes')
        reorder = st.selectbox('Would Reorder?', ['Y', 'N'])

        submitted = st.form_submit_button('Save Entry')
        if submitted:
            data.append({
                'Strain Name': strain,
                'Manufacturer': manufacturer,
                'Cultivar': cultivar,
                'Medication Format': product_type,
                'THC %': thc,
                'CBD %': cbd,
                'Terpene Profile': terpenes,
                'Price (£)': price,
                'Quantity Ordered (g/ml)': quantity,
                'Anxiety Level': anxiety_level,
                'Anxiety Notes': anxiety_notes,
                'Muscular Pain Level': muscular_pain_level,
                'Muscular Pain Notes': muscular_pain_notes,
                'Joint Pain Level': joint_pain_level,
                'Joint Pain Notes': joint_pain_notes,
                'Nerve Pain Level': nerve_pain_level,
                'Nerve Pain Notes': nerve_pain_notes,
                'Mood Level': mood_level,
                'Mood Notes': mood_notes,
                'Appetite Level': appetite_level,
                'Appetite Notes': appetite_notes,
                'Motivation Level': motivation_level,
                'Motivation Notes': motivation_notes,
                'Overall Effectiveness': effectiveness_rating,
                'General Notes': notes,
                'Personal Experience Notes': personal_notes,
                'Would Reorder?': reorder
            })
            save_data(data)
            st.success('Entry saved!')
            st.session_state['adding'] = False
            st.experimental_rerun()

if st.session_state.get('analysing'):
    st.subheader("Analyse Reviews")
    review_text = st.text_area("Paste Reviews Here")
    uploaded_file = st.file_uploader("Or Upload a Text File", type=['txt'])

    if st.button('Analyse'):
        combined_reviews = review_text
        if uploaded_file:
            combined_reviews += uploaded_file.read().decode()

        positive_keywords = ['good', 'effective', 'great', 'helped', 'relief', 'best', 'recommend']
        negative_keywords = ['bad', 'ineffective', 'poor', 'waste', 'worst', "didn't work"]

        positive_hits = sum(combined_reviews.lower().count(word) for word in positive_keywords)
        negative_hits = sum(combined_reviews.lower().count(word) for word in negative_keywords)

        total_hits = positive_hits + negative_hits
        sentiment_score = positive_hits / total_hits if total_hits > 0 else 0.5
        approx_rating = int(sentiment_score * 10)

        st.markdown("### Review Summary")
        st.write(f"Positive Keywords Found: {positive_hits}")
        st.write(f"Negative Keywords Found: {negative_hits}")
        st.write(f"Approximate Overall Rating (1-10): {approx_rating}")

        st.session_state['analysing'] = False

st.subheader('Current Entries')

if data:
    df = pd.DataFrame(data)
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    json_data = json.dumps(data, indent=2).encode('utf-8')

    st.download_button('Download CSV', data=csv, file_name='cannabis_tracker_data.csv', mime='text/csv')
    st.download_button('Download JSON', data=json_data, file_name='cannabis_tracker_data.json', mime='application/json')
else:
    st.info('No entries yet. Add your first record using the sidebar.')
