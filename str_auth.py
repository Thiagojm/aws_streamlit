import streamlit_authenticator as stauth


hashed_passwords = stauth.Hasher(["your_pass", "another_pass"]).generate()
print(hashed_passwords)