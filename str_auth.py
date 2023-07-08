import streamlit_authenticator as stauth


hashed_passwords = stauth.Hasher(["asfs"]).generate()
print(hashed_passwords)