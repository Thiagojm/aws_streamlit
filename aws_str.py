import streamlit as st

def main():
    st.sidebar.header("Login")

    # Username input
    username = st.sidebar.text_input("Username")

    # Password input
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if password == "12345":
            st.success("You are logged in")
            st.write("Welcome to the app!")
        else:
            st.error("Invalid username or password")

    st.title("Streamlit App")
    st.write("This is the main area of the app.")

    # Adding widgets
    st.header("Widgets")
    st.subheader("Checkbox")
    checkbox_state = st.checkbox("Check me!")
    if checkbox_state:
        st.write("Checkbox is checked.")

    st.subheader("Slider")
    slider_value = st.slider("Select a value", 0, 10)
    st.write("Slider value:", slider_value)

    st.subheader("Selectbox")
    options = ["Option 1", "Option 2", "Option 3"]
    selected_option = st.selectbox("Select an option", options)
    st.write("Selected option:", selected_option)

    # Displaying an image
    st.header("Image")
    st.image("src/img/sup_cpu.jpg", caption="Super CPU", use_column_width=True)

if __name__ == "__main__":
    main()
