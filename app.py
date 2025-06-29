
import streamlit as st
import json
import os
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
st.title('Cannabis-Based Medicines Tracker')
if st.button('Add New Entry'):
    st.session_state['adding'] = True
if st.session_state.get('adding'):
    strain = st.text_input('Strain Name')
    product_type = st.selectbox('Product Type', ['Flower', 'Oil', 'Cart', 'Pastelle'])
    vendor = st.text_input('Vendor/Source')
    thc = st.number_input('THC %', 0.0, 100.0)
    cbd = st.number_input('CBD %', 0.0, 100.0)
    terpenes = st.text_input('Terpene Profile')
    price = st.number_input('Price (£)', 0.0)
    quantity = st.number_input('Quantity Ordered (g/ml)', 0.0)
    rating = st.slider('Effectiveness Rating (1-5)', 1, 5)
    notes = st.text_area('Notes (Reviews/Reddit/Discord)')
    personal_notes = st.text_area('Personal Experience Notes')
    reorder = st.selectbox('Would Reorder?', ['Y', 'N'])
    if st.button('Save'):
        data.append({
            'Strain Name': strain,
            'Product Type': product_type,
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
        st.session_state['adding'] = False
        st.experimental_rerun()
st.subheader('Current Entries')
for item in data:
    st.write(item)