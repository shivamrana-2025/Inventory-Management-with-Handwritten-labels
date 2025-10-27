import streamlit as st
from inventory_backend import preprocess_image, extract_text, parse_item_info

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

        if not item_name:
            item_name = st.text_input("Enter item name manually:")
        if not quantity:
            quantity = st.number_input("Enter quantity manually:", min_value=1, step=1)
        if not price:
            price = st.number_input("Enter price manually:", min_value=1.0, step=0.5)

        if st.button("<span style='color:yellow'>✅ Add to Inventory</span>"):
            st.session_state.inventory[item_name] = {"quantity": quantity, "price": price}
            st.success(f"{item_name} added to inventory!")

if st.session_state.inventory:
    st.write("## 📦 Current Inventory")
    st.table(st.session_state.inventory)
else:
    st.info("No items in inventory yet.")
