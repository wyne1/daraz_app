import streamlit as st
import pandas as pd

# Set up the page layout
st.set_page_config(page_title='Dashboard', layout='wide')

# Custom styles
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        color: white;
    }
    .score-box {
        border: 2px solid #f63366;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
    }
    .stButton>button {
        margin: 5px 0;
    }
    .stProgress>div>div {
        background-color: #ff4b4b;
    }
    </style>
""", unsafe_allow_html=True)

# Navigation bar
st.sidebar.title('Navigation')
st.sidebar.button('HOME')
st.sidebar.button('Contact Us')

# Load data from CSV files
@st.experimental_memo
def load_data():
    buyer_df = pd.read_csv('buyer_df.csv')
    product_seller_df = pd.read_csv('product_seller_df.csv')
    seller_df = pd.read_csv('seller_df.csv')
    return buyer_df, product_seller_df, seller_df

buyer_df, product_seller_df, seller_df = load_data()

# Input fields and submit button
buyer_id = st.text_input('Buyer ID', '')
product_id = st.text_input('Product ID', '')
submit = st.button('Submit')

# Fetch scores and display
if submit and buyer_id and product_id:
    try:
        buyer_id = int(buyer_id)
        product_id = int(product_id)

        buyer_score = buyer_df[buyer_df['Buyer_ID'] == buyer_id]['Buyer_Score'].iloc[0]
        product_score = product_seller_df[product_seller_df['Product_ID'] == product_id]['Product_Score'].iloc[0]

        seller_id = product_seller_df[product_seller_df['Product_ID'] == product_id]['Seller_ID'].iloc[0]
        seller_score = seller_df[seller_df['Seller_ID'] == seller_id]['Seller_Score'].iloc[0]

        composite_score = round((buyer_score + product_score + seller_score) / 3, 2)
        
        # Display scores in boxes
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='score-box big-font'>Seller Score: {seller_score}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='score-box big-font'>Buyer Score: {buyer_score}</div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='score-box big-font'>Product Score: {product_score}</div>", unsafe_allow_html=True)

        # Large red box with progress bar and value
        progress_bar_value = composite_score  # Assuming Product Score is a percentage
        st.markdown(f"<div style='background-color: #ff4b4b; color: white; padding: 20px; text-align: center; margin-top: 10px;'>", unsafe_allow_html=True)
        st.progress(progress_bar_value / 100)
        st.markdown(f"<div class='big-font'>{progress_bar_value}%</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    except KeyError:
        st.error('Error: ID not found in the dataset.')
    except ValueError:
        st.error('Error: Invalid input. Please enter numeric values for IDs.')
