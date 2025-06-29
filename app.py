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
Use this tool to track your **cannabis-based medicines**, including manufacturer, cultivar, and symptoms you're medicating for.
""")

# Replace these with the full lists you provided
manufacturers = [
    '4C Labs Ltd.', 'All Nations Mestiyexw Holdings', 'Althea MMJ UK Ltd', 'Dispensed Pty Ltd.',
    'Aurora Europe GmbH', 'Castle Rock Farms Inc.', 'Big Narstie Medical Ltd', 'Habitat Life Sciences Inc.',
    # ... rest of your list
]

cultivars = [
    '4C Labs', 'All Nations', 'Althea', 'Altmed', 'Aurora', 'BC Green', 'Big Narstie Medical',
    'Cake & Caviar', 'CannFX', 'CannyCann',
    # ... rest of your list
]

with st.sidebar:
    st.header("Add New Entry")
    if st.button('Start New Entry'):
        st.session_state['adding'] = True

if st.session_state.get('adding'):
    with st.form('new_entry_form', clear_on_submit=True):
        strain = st.text_input('Strain Name')

        manufacturer = st.selectbox('Manufacturer', manufacturers)
        cultivar = st.selectbox('Cultivar', cultivars)

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
        anxiety = st.checkbox('Anxiety')
        muscular_pain = st.checkbox('Muscular Pain')
        joint_pain = st.checkbox('Joint Pain')
        nerve_pain = st.checkbox('Nerve Pain')

        st.markdown("### Secondary Effects")
        mood = st.checkbox('Mood')
        appetite = st.checkbox('Appetite')
        motivation = st.checkbox('Motivation')

        rating = st.slider('Effectiveness Rating (1-10)', 1, 10)
        notes = st.text_area('Notes (Reviews/Reddit/Discord)')
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
                'Anxiety': anxiety,
                'Muscular Pain': muscular_pain,
                'Joint Pain': joint_pain,
                'Nerve Pain': nerve_pain,
                'Mood': mood,
                'Appetite': appetite,
                'Motivation': motivation,
                'Effectiveness Rating (1-10)': rating,
                'Notes': notes,
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
