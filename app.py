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

# Replace below with your FULL lists
manufacturers = [
    '4C Labs Ltd.', 'All Nations Mestiyexw Holdings', 'Althea MMJ UK Ltd',
    # ... rest of your list
]

cultivars = [
    '4C Labs', 'All Nations', 'Althea',
    # ... rest of your list
]

with st.sidebar:
    st.header("Add New Entry")
    if st.button('Start New Entry'):
        st.session_state['adding'] = True

if st.session_state.get('adding'):
    with st.form('new_entry_form', clear_on_submit=True):
        strain = st.text_input('Strain Name')

        with st.expander('Select Manufacturer'):
            manufacturer = st.selectbox('Manufacturer (Searchable)', options=manufacturers)

        with st.expander('Select Cultivar'):
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
