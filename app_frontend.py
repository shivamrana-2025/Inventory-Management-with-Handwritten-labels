# ...existing code...
import streamlit as st
from inventory_backend import preprocess_image, extract_text, parse_item_info

def circled_check_svg(size=20, circle_color="#16a34a", check_color="#ffffff"):
    return f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" style="vertical-align:middle;">
      <circle cx="12" cy="12" r="11" fill="{circle_color}" />
      <path d="M7 12.5l2.5 2.5L17 8" stroke="{check_color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
    </svg>
    '''

if "inventory" not in st.session_state:
    st.session_state.inventory = {}

st.title("🛒 Handwritten Label Inventory Management")
st.markdown("Upload a handwritten label like **'Apple Quantity: 7 Price: 100'** to extract item details automatically.")

uploaded_file = st.file_uploader("📸 Upload Handwritten Label Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Label", use_column_width=True)
    with st.spinner("🧠 Recognizing Handwritten Text..."):
        processed_img = preprocess_image(uploaded_file)
        ocr_text = extract_text(processed_img)
        st.write("### Raw OCR Text:")
        st.info(ocr_text)

        item_name, quantity, price = parse_item_info(ocr_text)
        st.write("### Extracted Details:")
        st.write(f"**Item:** {item_name}")
        st.write(f"**Quantity:** {quantity}")
        st.write(f"**Price:** {price}")

        # Use explicit widget keys so values persist across the page reload triggered by our HTML button
        if not item_name:
            st.text_input("Enter item name manually:", key="manual_item_name")
            item_name = st.session_state.get("manual_item_name", "")
        else:
            st.session_state["manual_item_name"] = item_name

        if not quantity:
            st.number_input("Enter quantity manually:", min_value=1, step=1, key="manual_quantity")
            quantity = st.session_state.get("manual_quantity", 0)
        else:
            st.session_state["manual_quantity"] = quantity

        if not price:
            st.number_input("Enter price manually:", min_value=1.0, step=0.5, key="manual_price")
            price = st.session_state.get("manual_price", 0.0)
        else:
            st.session_state["manual_price"] = price

        # Render a custom HTML button that contains the circled check SVG inside it.
        # The button submits a GET form with ?add=1; we detect that below and add the item.
        svg_html = circled_check_svg(18)
        button_html = f'''
        <form action="" method="get">
          <button type="submit" name="add" value="1"
            style="
              display:inline-flex;
              align-items:center;
              gap:8px;
              padding:6px 12px;
              border-radius:8px;
              border:1px solid #16a34a;
              background:#16a34a;
              color:#ffffff;
              font-weight:600;
              cursor:pointer;
            ">
            {svg_html}
            <span style="vertical-align:middle;">Add to Inventory</span>
          </button>
        </form>
        '''
        st.markdown(button_html, unsafe_allow_html=True)

        # If the HTML button was clicked the URL will include ?add=1 — handle that action here.
        params = st.experimental_get_query_params()
        if "add" in params:
            if not item_name:
                st.warning("Please provide an item name before adding.")
                # clear params to avoid repeated warnings
                st.experimental_set_query_params()
                st.experimental_rerun()
            st.session_state.inventory[item_name] = {"quantity": quantity, "price": price}
            st.success(f"{item_name} added to inventory!")
            # clear query params and rerun to remove the ?add=1 from the URL
            st.experimental_set_query_params()
            st.experimental_rerun()

if st.session_state.inventory:
    st.write("## 📦 Current Inventory")
    st.table(st.session_state.inventory)
else:
    st.info("No items in inventory yet.")
# ...existing code...
```# filepath: /workspaces/Inventory-Management-with-Handwritten-labels/app_frontend.py
# ...existing code...
import streamlit as st
from inventory_backend import preprocess_image, extract_text, parse_item_info

def circled_check_svg(size=20, circle_color="#16a34a", check_color="#ffffff"):
    return f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" style="vertical-align:middle;">
      <circle cx="12" cy="12" r="11" fill="{circle_color}" />
      <path d="M7 12.5l2.5 2.5L17 8" stroke="{check_color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
    </svg>
    '''

if "inventory" not in st.session_state:
    st.session_state.inventory = {}

st.title("🛒 Handwritten Label Inventory Management")
st.markdown("Upload a handwritten label like **'Apple Quantity: 7 Price: 100'** to extract item details automatically.")

uploaded_file = st.file_uploader("📸 Upload Handwritten Label Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Label", use_column_width=True)
    with st.spinner("🧠 Recognizing Handwritten Text..."):
        processed_img = preprocess_image(uploaded_file)
        ocr_text = extract_text(processed_img)
        st.write("### Raw OCR Text:")
        st.info(ocr_text)

        item_name, quantity, price = parse_item_info(ocr_text)
        st.write("### Extracted Details:")
        st.write(f"**Item:** {item_name}")
        st.write(f"**Quantity:** {quantity}")
        st.write(f"**Price:** {price}")

        # Use explicit widget keys so values persist across the page reload triggered by our HTML button
        if not item_name:
            st.text_input("Enter item name manually:", key="manual_item_name")
            item_name = st.session_state.get("manual_item_name", "")
        else:
            st.session_state["manual_item_name"] = item_name

        if not quantity:
            st.number_input("Enter quantity manually:", min_value=1, step=1, key="manual_quantity")
            quantity = st.session_state.get("manual_quantity", 0)
        else:
            st.session_state["manual_quantity"] = quantity

        if not price:
            st.number_input("Enter price manually:", min_value=1.0, step=0.5, key="manual_price")
            price = st.session_state.get("manual_price", 0.0)
        else:
            st.session_state["manual_price"] = price

        # Render a custom HTML button that contains the circled check SVG inside it.
        # The button submits a GET form with ?add=1; we detect that below and add the item.
        svg_html = circled_check_svg(18)
        button_html = f'''
        <form action="" method="get">
          <button type="submit" name="add" value="1"
            style="
              display:inline-flex;
              align-items:center;
              gap:8px;
              padding:6px 12px;
              border-radius:8px;
              border:1px solid #16a34a;
              background:#16a34a;
              color:#ffffff;
              font-weight:600;
              cursor:pointer;
            ">
            {svg_html}
            <span style="vertical-align:middle;">Add to Inventory</span>
          </button>
        </form>
        '''
        st.markdown(button_html, unsafe_allow_html=True)

        # If the HTML button was clicked the URL will include ?add=1 — handle that action here.
        params = st.experimental_get_query_params()
        if "add" in params:
            if not item_name:
                st.warning("Please provide an item name before adding.")
                # clear params to avoid repeated warnings
                st.experimental_set_query_params()
                st.experimental_rerun()
            st.session_state.inventory[item_name] = {"quantity": quantity, "price": price}
            st.success(f"{item_name} added to inventory!")
            # clear query params and rerun to remove the ?add=1 from the URL
            st.experimental_set_query_params()
            st.experimental_rerun()

if st.session_state.inventory:
    st.write("## 📦 Current Inventory")
    st.table(st.session_state.inventory)
else:
    st.info("No items in inventory yet.")
# ...existing code...
