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
Use this tool to track your **cannabis-based medicines**, including strain details, manufacturer, chemotype, and personal effectiveness notes.
""")

manufacturers = [
    '4C Labs Ltd.', 'All Nations Mestiyexw Holdings', 'Althea MMJ UK Ltd', 'Dispensed Pty Ltd.',
    'Aurora Europe GmbH', 'Castle Rock Farms Inc.', 'Big Narstie Medical Ltd', 'Habitat Life Sciences Inc.',
    'Ampyl Sciences Ltd', 'MediCann Ltd', 'Canopy Growth Corp', 'Cellen Biotech Ltd',
    'Clearleaf Ltd', 'CP Medical', 'Montu Group Pty Ltd.', 'Crop Circle Dispensary Ltd.',
    'Cookies Creative Productions & Consulting Inc.', 'Curaleaf Holdings Inc', 'Dalgety Ltd',
    'DOE Medical Ltd.', 'Doja Medical', 'Prime Pot Inc.', 'ECS Pharma Ltd', 'Endopure Medical Ltd',
    'Glass Pharms Ltd', 'Grow Lab Organics Ltd', 'GreenJoy Inc.', 'BZAM Ltd', 'Grow Group PLC',
    # ... (you can add more here from your list)
]

cultivars = [
    '4C Labs', 'All Nations', 'Althea', 'Altmed', 'Aurora', 'BC Green', 'Big Narstie Medical',
    'Cake & Caviar', 'CannFX', 'CannyCann', 'Canopy Growth', 'Cellen', 'Clearleaf', 'CP Medical',
    'Craft Botanics', 'Crop Circle Therapeutics', 'Cookies', 'Curaleaf', 'Curo', 'Dalgety',
    'Dispensed Labs', 'Dank of England Medical', 'Doja', 'EastCann', 'ECS Pharma', 'Endopure',
    'Find', 'Four20 Pharma', 'Glass Pharms', 'GLO', 'Grassroots', 'Green Joÿ',
    # ... (you can add more here from your list)
]

primary_symptoms = [
    'Anxiety', 'Muscular Pain', 'Joint Pain', 'Nerve Pain', 'Sleep Issues', 'Depression'
]

secondary_symptoms = [
    'Appetite', 'Mood', 'Motivation', 'Focus', 'Energy'
]

with st.sidebar:
    st.header("Add New Entry")
    if st.button('Start New Entry'):
        st.session_state['adding'] = True

if st.session_state.get('adding'):
    with st.form('new_entry_form', clear_on_submit=True):
        with st.expander('Basic Info', expanded=True):
            strain = st.text_input('Strain Name')
            cultivar = st.selectbox('Cultivar', cultivars)
            manufacturer = st.selectbox('Manufacturer', manufacturers)
            product_type = st.selectbox('Medication Format', [
                'Bud/Flower', 'Sublingual Oil', 'Vape Cartridge', 'Pill/ Capsule',
                'Edible', 'Topical', 'Oral Spray', 'Inhaler', 'Patch'
            ])
            availability = st.selectbox('Medication Availability', [
                'Available', 'Discontinued', 'Out of Stock', 'Unreleased',
                'Limited Access', 'Not Currently Imported'
            ])
        
        with st.expander('Classification & Composition'):
            classification = st.selectbox('Classification', [
                'Hybrid', 'Indica Hybrid', 'Sativa Hybrid', 'Sativa', 'Indica'
            ])
            chemotype = st.selectbox('Chemotype', [
                'Type I: High THC', 'Type II: THC/CBD Mix', 'Type III: High CBD'
            ])
            irradiation = st.selectbox('Flower Irradiation', [
                'Non-Irradiated', 'Gamma-Irradiated (Gamma Ray)', 'Beta-Irradiated (Electron Beam)',
                'REV™ Irradiated (Microwave)', 'Unknown'
            ])
            flower_format = st.selectbox('Flower Format', [
                'Trimmed Whole Buds', 'Pre-Ground Buds'
            ])
        
        with st.expander('Chemical Profile & Cost'):
            thc = st.number_input('THC %', 0.0, 100.0)
            cbd = st.number_input('CBD %', 0.0, 100.0)
            terpenes = st.text_input('Terpene Profile')
            price = st.number_input('Price (£)', 0.0)
            quantity = st.number_input('Quantity Ordered (g/ml)', 0.0)
        
        with st.expander('Symptoms & Effectiveness'):
            primary = st.multiselect('Primary Symptoms Treated', primary_symptoms)
            secondary = st.multiselect('Secondary Effects', secondary_symptoms)
            rating = st.slider('Effectiveness Rating (1-5)', 1, 5)
            notes = st.text_area('Notes (Reviews/Reddit/Discord)')
            personal_notes = st.text_area('Personal Experience Notes')
            reorder = st.selectbox('Would Reorder?', ['Y', 'N'])

        submitted = st.form_submit_button('Save Entry')
        if submitted:
            data.append({
                'Strain Name': strain,
                'Cultivar': cultivar,
                'Manufacturer': manufacturer,
                'Medication Format': product_type,
                'Classification': classification,
                'Chemotype': chemotype,
                'Flower Irradiation': irradiation,
                'Flower Format': flower_format,
                'Medication Availability': availability,
                'THC %': thc,
                'CBD %': cbd,
                'Terpene Profile': terpenes,
                'Price (£)': price,
                'Quantity Ordered (g/ml)': quantity,
                'Primary Symptoms': primary,
                'Secondary Effects': secondary,
                'Effectiveness Rating (1-5)': rating,
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
