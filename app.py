from db.database import DataContent, Base, Stocks
from db.recorded_data import Records
import streamlit as st
import time

data_content = DataContent()
records = Records()
column_order = ('id', 'barcode', 'item_name', 'item_price', 'quantity', 'price', 'register_by', 'registration_date')
column_name = {
    "id": "ID",
    "barcode": "Barcode",
    "item_name": "Item Name",
    "item_price": "Item Price",
    "quantity": "Quantity",
    "price": "Price",
    "register_by": "Registered By",
    "registration_date": "Registration Date"
}

st.set_page_config("SQL Inventory System", layout="wide")
st.markdown(
    '<h1>SQL Inventory System ⛁ </h1>',
    unsafe_allow_html=True
)

def clear_box():
    st.session_state.barcode = ""
    st.session_state.item = ""
    st.session_state.qty = ""
    st.session_state.price = ""
    st.session_state.sell_price = ""
    st.session_state.register = ""

def clear_field():
    st.session_state.show_form = False

container = st.container(border=True)

db_container = st.container(border=True)
with db_container:
    if st.button("DB"):
        if data_content.check_exist_table():
            st.dataframe(data_content.get_all_data(),
                        hide_index=True,
                        column_order=column_order,
                        column_config=column_name)
        
    if st.button("eXe"):
        data_content.delete_table()
    
with container:
    option_buttons = st.columns(2)
    with option_buttons[0]:
        add_button = st.button("Add Item ➕", width="stretch")
    
    with option_buttons[1]:
        search_button = st.button("Search Item 🔍", width="stretch")

    if "show_form" not in st.session_state:
        st.session_state.show_form = False

    if "search" not in st.session_state:
        st.session_state.search = False

    if add_button:
        st.session_state.search = False
        st.session_state.show_form = True

    if search_button:
        st.session_state.show_form = False
        st.session_state.search = True

    if st.session_state.search:
        search_barcode = st.text_input("Enter Barcode", key="search_b",  help="text-input")

        if st.button("Search", key="search_details"):
            if search_barcode:
                st.session_state.search_result = data_content.get_data(search_barcode)
            else:
                st.warning("Input barcode to search")

        if "search_result" in st.session_state and not st.session_state.search_result.empty:
            st.write(st.session_state.search_result)
            
            col1, col2 = st.columns([0.2, 0.8])
            with col1:
                if st.button("Delete Data", key="delete_data"):
                    st.success(f"Deleted: {search_barcode}")
                    time.sleep(1)
                    del st.session_state.search_result
                    records.get_record_data(search_barcode)
                    data_content.delete_data(search_barcode)

        elif "search_result" in st.session_state:
            st.info("No data found for this barcode")
        
    if st.session_state.show_form:
        input_1, input_2, input_3, input_4, input_5, input_6 = st.columns(6)
        with input_1:
            barcode = st.text_input("Barcode", key="barcode", help="text-input")
        with input_2:
            item_name = st.text_input("Item Name", key="item", help="text-input")
        with input_3:
            quantity = st.text_input("Quantity", key="qty", help="numbers")
        with input_4:
            item_price = st.text_input("Item Price", key="price", help="numbers")
        with input_5:
            selling_price = st.text_input("Selling Price", key="sell_price", help="numbers")
        with input_6:
            registrator = st.text_input("Register By", key="register", help="name")

        if st.button("Add to Inventory", width="stretch"):
            if not barcode or not item_name or not quantity or not item_price or not selling_price or not registrator:
                st.error("Invalid input. Please check inputted data")
            else:
                try:
                    st.success(f"{barcode} is successfully added")
                    time.sleep(2)
                    data_content.add_content(barcode=barcode, item=item_name, quantity=quantity,
                                            price=item_price, selling_price=selling_price,
                                            registrator=registrator)
                except ValueError:
                    st.error("Invalid input. Please check inputted data")
                else:
                    clear_field()

        if st.button("Clear Data", on_click=clear_box, width="stretch"):
            st.info("Data Cleared")