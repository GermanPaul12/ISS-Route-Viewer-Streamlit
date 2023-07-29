import streamlit as st
from neo4j import GraphDatabase

# Function to save the email to the Neo4j database
def save_email_to_database(email):
    neo4j_uri = st.secrets["NEO_URI"]
    neo4j_user = st.secrets["NEO_USER"]
    neo4j_password = st.secrets["NEO_PW"]

    with GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password)) as driver:
        with driver.session() as session:
            session.write_transaction(add_email, email)

def add_email(tx, email):
    tx.run("CREATE (e:Email {email: $email})", email=email)

def main():
    st.title("ISS Newsletter Sign-up")
    st.write("Subscribe to our newsletter to receive an email when the ISS is above Mannheim!")

    # Input for the user's email address
    email = st.text_input("Enter your email address:")

    # Button to sign up for the newsletter
    if st.button("Sign Up"):
        if email:
            # Save the email to the Neo4j database
            save_email_to_database(email)
            st.success("Thank you for subscribing! You will be notified when the ISS is above Mannheim.")
        else:
            st.warning("Please enter a valid email address.")

if __name__ == "__main__":
    main()
