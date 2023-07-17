import os
import streamlit as st
import streamlit_authenticator as stauth
import sup_module as sup
import plotly.express as px

def main():
    # Define a class to handle session state
    class SessionState:
        def __init__(self):
            self.messages = []

    # Create or get the session state
    if "session" not in st.session_state:
        st.session_state.session = SessionState()
        
    # Variables
    folder_path = 'rngs/test_rng/'
    local_folder = 'src/temp/'
    bucket_name = st.secrets['BUCKET_NAME']
    s3 = sup.create_s3_client()
    
    ######### Sidebar #########     

    # Make a sidebar
    st.sidebar.markdown(f"Welcome {name}")
    csv_files_list = sup.list_csv_files(s3, bucket_name, folder_path)
    sidebar_selectbox = st.sidebar.selectbox("Choose a file:", csv_files_list)
    authenticator.logout("Logout", "sidebar")
    file_name = os.path.join(sidebar_selectbox + '.csv')
                    

    ####### Home Page #######    
    # Header
    st.header("RNG Data Visualization")
    st.divider()
    col1, col2, col3 = st.columns([3,6,3])
    with col1:
        st.write("")
    with col2:
        st.image("src/img/sup_cpu.jpg")
    with col3:
        st.write("")     
    

    st.divider()
    
    # Show Graph Button
    if st.button("Show Graph"):
        with st.spinner('Runing...'):
            df = sup.read_csv_aws(s3, bucket_name, folder_path, file_name, local_folder)
            bit_count = sup.find_bit_count(file_name)
            interval = sup.find_interval(file_name)
            chart_data = sup.csv_to_df(df, bit_count)
            fig = px.line(chart_data, x='Time', y='Zscore')
            st.divider()
            st.subheader(f"Arquivo: {sidebar_selectbox}, {bit_count} bits per {interval} second(s)")
            st.plotly_chart(fig, use_container_width=True)
            st.text("Tabela de dados:")
            st.dataframe(chart_data, use_container_width=True)
            
        
    
if __name__ == "__main__":
    # Create an instance of the Authenticate class
    authenticator = stauth.Authenticate(
    dict(st.secrets['credentials']),
    st.secrets['cookie']['name'],
    st.secrets['cookie']['key'],
    st.secrets['cookie']['expiry_days'],
    st.secrets['preauthorized']
)

    name, authentication_status, username = authenticator.login("Login", "main")
    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        st.warning("Please enter your username and password")

    if authentication_status:
        main()
    
