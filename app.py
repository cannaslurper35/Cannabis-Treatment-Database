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
Use this tool to track your **cannabis-based medicines**, including strain details, classifications, chemotype, irradiation type, and personal effectiveness notes.
""")

with st.sidebar:
    st.header("Add New Entry")
    if st.button('Start New Entry'):
        st.session_state['adding'] = True

if st.session_state.get('adding'):
    with st.form('new_entry_form', clear_on_submit=True):
        with st.expander('Basic Info', expanded=True):
            strain = st.text_input('Strain Name')
            product_type = st.selectbox('Medication Format', [
                'Bud/Flower', 'Sublingual Oil', 'Vape Cartridge', 'Pill/ Capsule',
                'Edible', 'Topical', 'Oral Spray', 'Inhaler', 'Patch'
            ])
            vendor = st.text_input('Vendor/Source')
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
        
        with st.expander('Effectiveness & Notes'):
            rating = st.slider('Effectiveness Rating (1-5)', 1, 5)
            notes = st.text_area('Notes (Reviews/Reddit/Discord)')
            personal_notes = st.text_area('Personal Experience Notes')
            reorder = st.selectbox('Would Reorder?', ['Y', 'N'])

        submitted = st.form_submit_button('Save Entry')
        if submitted:
            data.append({
                'Strain Name': strain,
                'Medication Format': product_type,
                'Classification': classification,
                'Chemotype': chemotype,
                'Flower Irradiation': irradiation,
                'Flower Format': flower_format,
                'Medication Availability': availability,
                'Vendor/Source': vendor,
                'THC %': thc,
                'CBD %': cbd,
                'Terpene Profile': terpenes,
                'Price (£)': price,
                'Quantity Ordered (g/ml)': quantity,
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
