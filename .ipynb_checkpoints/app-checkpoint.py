import streamlit as st
import pandas as pd

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def add_image(image_path, width=None, sidebar=True):
    from PIL import Image
    image = Image.open(image_path)

    # Resize image if width is specified
    if width is not None:
        # Calculate new height to maintain aspect ratio
        aspect_ratio = image.width / image.height
        new_height = int(width / aspect_ratio)
        image = image.resize((width, new_height))
    
    # Display image in the sidebar or main page
    if sidebar:
        st.sidebar.image(image)
    else:
        st.image(image)

def load_data():
    buyer_df = pd.read_csv('buyer_df.csv')
    product_seller_df = pd.read_csv('product_seller_df.csv')
    seller_df = pd.read_csv('seller_df.csv')

    conditions_df = pd.read_csv('conditions_df.csv')
    
    return buyer_df, product_seller_df, seller_df, conditions_df

def main():
    st.set_page_config(page_title='Daraz QCC System', layout='wide')
    st.markdown("""
        <style>
            .tech-titans-title {
                color: #ff4500; /* Orange color */
                font-size: 2rem; /* Big size */
                font-weight: bold; /* Bold font */
                text-align: center; /* Centered text */
                margin: 0rem 0; /* Margin for spacing */
            }
        </style>
        """, unsafe_allow_html=True)

    # Display the team name with the custom style
    st.markdown('<div class="tech-titans-title">TECH TITANS</div>', unsafe_allow_html=True)
    st.markdown('<div class="tech-titans-title">Automatic QCC System</div>', unsafe_allow_html=True)
    # Load local CSS
    local_css('style.css')

    # Display the company logo

    add_image('daraz-logo-new.png', width=200)  # Set the width to your preference
    # st.sidebar.image('daraz-logo-new.png', use_column_width=True)

    # Navigation bar
    st.sidebar.button('Homepage')
    # st.sidebar.button('Contact Us')

    # Load data from CSV files
    buyer_df, product_seller_df, seller_df, conditions_df = load_data()

    # Input fields and submit button
    buyer_id = st.text_input('Buyer ID', '')
    product_id = st.text_input('Product ID', '')
    submit = st.button('Submit')

    # Fetch scores and display
    if submit and buyer_id and product_id:
        try:
            buyer_id = int(buyer_id)
            product_id = int(product_id)

            #buyer_score = buyer_df[buyer_df['Buyer_ID'] == buyer_id]['Buyer_Score'].iloc[0]
            #product_score = product_seller_df[product_seller_df['Product_ID'] == product_id]['Product_Score'].iloc[0]

            #seller_id = product_seller_df[product_seller_df['Product_ID'] == product_id]['Seller_ID'].iloc[0]
            #seller_score = seller_df[seller_df['Seller_ID'] == seller_id]['Seller_Score'].iloc[0]

            # Calculate the composite score

            buyer_score = conditions_df[(conditions_df['user id'] == buyer_id) & (conditions_df['item id'] == product_id)]['Buyer'].iloc[0]
            seller_score = conditions_df[(conditions_df['user id'] == buyer_id) & (conditions_df['item id'] == product_id)]['Seller'].iloc[0]
            product_score = conditions_df[(conditions_df['user id'] == buyer_id) & (conditions_df['item id'] == product_id)]['Product'].iloc[0]
            pl_score = conditions_df[(conditions_df['user id'] == buyer_id) & (conditions_df['item id'] == product_id)]['3PL'].iloc[0]

            output_action = conditions_df[(conditions_df['user id'] == buyer_id) & (conditions_df['item id'] == product_id)]['Output'].iloc[0]
            
            composite_score = (buyer_score + product_score + seller_score) / 3

            # Display scores in boxes
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"<div class='score-box'>Seller Score: {seller_score}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div class='score-box'>Buyer Score: {buyer_score}</div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div class='score-box'>Product Score: {product_score}</div>", unsafe_allow_html=True)
            with col4:
                st.markdown(f"<div class='score-box'>3PL Score: {pl_score}</div>", unsafe_allow_html=True)

            
            # Large red box with progress bar and value
            progress_bar_value = composite_score  # This assumes the composite score is a percentage
            st.markdown(f"<div class='large-red-box'><div class='big-font'>{output_action}</div>", unsafe_allow_html=True)
            # st.markdown(f"<div class='large-red-box'><div class='big-font'>{output_action}</div>", unsafe_allow_html=True)
            st.progress(100)
            st.markdown("</div>", unsafe_allow_html=True)
            
            columns_of_interest = ['item id' ,'Category', 'Item Delivery status', 'Item Price', 'RR']  # Replace with your actual column names
            row_to_display = conditions_df.loc[(conditions_df['user id'] == buyer_id) & (conditions_df['item id'] == product_id), columns_of_interest]  # Replace 'some_index' with the actual index or condition

            # Display the row under the progress bar
            st.write("Data for selected row:")
            st.dataframe(row_to_display, use_container_width=True)
            

        

        

        except KeyError:
            st.error('Error: ID not found in the dataset.')
        except ValueError:
            st.error('Error: Invalid input. Please enter numeric values for IDs.')

if __name__ == "__main__":
    main()
