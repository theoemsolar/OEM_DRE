import streamlit as st
from .send_summary import send_summary
from streamlit_autorefresh import st_autorefresh


def send_email_automatically(dashboard_df, om_data, expenses_data):
    menage_emails()
    test_send(dashboard_df, om_data, expenses_data)


def test_send(dashboard_df, om_data, expenses_data):
    if st.button("Enviar"):
        send_for_email_list(dashboard_df, om_data, expenses_data)


def send_for_email_list(dashboard_df, om_data, expenses_data):
    for person in st.session_state.email_users:
        st.write(f"sending to {person}...")
        try:
            send_summary(person, dashboard_df, om_data, expenses_data)
            st.write(f"email enviado com sucesso para {person}")
        except:
            st.write(f"falha ao enviar email para {person}")


def menage_emails():
    st.title("Gerenciador de Emails")

    st.subheader("Emails cadastrados:")
    for email in st.session_state.email_users:
        col1, col2 = st.columns([0.8, 0.2])
        col1.write(email)
        if col2.button("❌", key=email):
            st.session_state.email_users.remove(email)
            st.rerun()

    with st.form("Email Form"):
        new_email = st.text_input("Adicionar novo email")
        if st.form_submit_button("Salvar"):
            if new_email and new_email not in st.session_state.email_users:
                st.session_state.email_users.append(new_email)
                st.rerun()
            else:
                st.warning("Email inválido ou já cadastrado!")
