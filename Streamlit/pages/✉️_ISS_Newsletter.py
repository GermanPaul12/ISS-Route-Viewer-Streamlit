import streamlit as st
from neo4j import GraphDatabase
import yagmail

neo4j_uri = st.secrets["NEO_URI"]
neo4j_user = st.secrets["NEO_USER"]
neo4j_password = st.secrets["NEO_PW"]
GMAIL_PW = st.secrets["GMAIL_PW"]
GMAIL_MAIL = st.secrets["GMAIL_MAIL"]


def read_emails():
    with GraphDatabase.driver(neo4j_uri,
                                auth=(neo4j_user, neo4j_password)) as driver:
        with driver.session() as session:
            result = session.read_transaction(get_emails)
            return result

def get_emails(tx):
    result = tx.run("MATCH (e:Email) RETURN e.email AS email")
    return [record["email"] for record in result]

# Function to save the email to the Neo4j database
def save_email_to_database(email):
    with GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password)) as driver:
                
        with driver.session() as session:
            session.write_transaction(add_email, email)

    sender = yagmail.SMTP(GMAIL_MAIL, GMAIL_PW)
     # Create the HTML content for the email
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    </head>
    <body style="font-family: 'Arial', sans-serif; color: #333333; margin: 0; padding: 0; background-color: rgba(192, 192, 192, 0.9); background-image: url('https://raw.githubusercontent.com/GermanPaul12/ISS-Route-Viewer-Streamlit/main/Data/iss.jpg'); background-size: cover; background-repeat: no-repeat;">
        <div style="background-color: rgba(0, 0, 0, 0.8); color: white; padding: 20px; text-align: center; font-size: 24px;">Hey there,</div>
        <div style="background-color: rgba(255, 255, 255, 0.8); padding: 20px;">
            <p style="font-size: 16px;">Thanks for signing up to the newsletter.</p>
            <p style="font-size: 16px;">You will be notified when the ISS is above Mannheim.</p>
            <p style="font-size: 16px; font-weight: bold;">Best regards</p>
            <p style="font-size: 16px;">German</p>
            <p style="font-size: 12px; color: #888888;">(ISS Mannheim Newsletter)</p>
        </div>
        <div style="background-color: rgba(255, 255, 255, 0.8); color: #333333; padding: 10px; text-align: center; font-size: 12px;">
            <p style="margin: 0; color: #888888;">Remove yourself from the Newsletter: <a href="https://iss-route.streamlit.app/ISS_Newsletter" style="color: #007BFF; text-decoration: none;">Unsubscribe</a></p>
        </div>
    </body>
    </html>
    """
    sender.send(to=email,
                subject="The ISS Mannheim Newsletter 📍",
                #contents=
                #"Hey there,\n\nThanks for signing up to the newsletter.\nYou will be notified when the ISS is above Mannheim.\nBest regards\nGerman \n(ISS Mannheim Newsletter)\n\nRemove yourself from the Newsletter: https://iss-route.streamlit.app/ISS_Newsletter\n"+html_content
                contents=html_content
                )
    
def add_email(tx, email):
    tx.run("CREATE (e:Email {email: $email})", email=email)

# Function to remove an email from the Neo4j database
def remove_email(email):
    with GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password)) as driver:
        with driver.session() as session:
            session.write_transaction(delete_email, email)

def delete_email(tx, email):
    tx.run("MATCH (e:Email {email: $email}) DELETE e", email=email)

def main():
    st.title("ISS Newsletter Sign-up")
    st.write("Subscribe to our newsletter to receive an email when the ISS is above Mannheim!")

    # Input for the user's email address
    email = st.text_input("Enter your email address:")

    # Button to sign up for the newsletter
    if st.button("Sign Up"):
        if email:
            if email not in read_emails():
                # Save the email to the Neo4j database
                save_email_to_database(email)
                st.success("Thank you for subscribing! You will be notified when the ISS is above Mannheim.")
            else:
                st.warning("This email is already registered.")    
        else:
            st.warning("Please enter a valid email address.")
            
    # Option to remove an email
    st.header("Remove Email")
    remove_email_input = st.text_input("Enter email to remove:")

    # Button to remove the email
    if st.button("Remove Email"):
        if remove_email_input:
            if remove_email_input not in read_emails():
                st.warning("This email is not in the database.")
            else:
                remove_email(remove_email_input)
                st.success(f"Email '{remove_email_input}' has been removed from the database.")
        else:
            st.warning("Please enter an email to remove.")       

if __name__ == "__main__":
    main()
