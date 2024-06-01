import json
import streamlit as st
import table
import model  # Adjust this import as per your actual model module structure
import table2
import time
from azure.communication.email import EmailClient
def agecalculator(age):
    age = int(age)
    if age > 0 and age <= 9:
        return 1
    elif age > 9 and age <= 24:
        return 2
    elif age > 24:
        return 3

# Set page title, icon and layout
st.set_page_config(page_title="Asthma", page_icon="📱", layout="wide")


def emailalert(usetname, age, response, Tiredness, Dry_Cough, Difficulty_in_Breathing, Sore_Throat, Pains, Runny_Nose, Nasal_Congestion):
    
    try:
        connection_string = "endpoint=https://emailservicefordoctor.unitedstates.communication.azure.com/;accesskey=MoSnxVTrnctDeX+TlYzktQelasXZxPQMkSSLyIavDRv90bd6xaSwYvhyKmAaFhpcTEuYUj9TNknrHVWcyFp2ow=="
        client = EmailClient.from_connection_string(connection_string)

        message = {
            "senderAddress": "DoNotReply@4df436e1-3dcd-4506-aef3-235582550c8a.azurecomm.net",
            "recipients":  {
                "to": [{"address": "99210041261@klu.ac.in" }],
            },
            "content": {
                "subject": f"Asthma Symptoms Alert of patient {lusername}",
                "plainText": f"""Patient : {lusername}\nAge: {age}\nGender: {'Male' if gender == 1 else 'Female'}Symptoms : Tiredness: {Tiredness}, Dry Cough: {Dry_Cough}, Difficulty in Breathing: {Difficulty_in_Breathing}, Sore Throat: {Sore_Throat}, Pains: {Pains}, Runny Nose: {Runny_Nose}, Nasal Congestion: {Nasal_Congestion}\nPredicted Severity: {response}\nPlease review the patient's condition and provide further instructions.""",
            }
        }

        poller = client.begin_send(message)
        result = poller.result()

    except Exception as ex:
        st.error(f"An error occurred while sending the email: {ex}")



# Main title for the application
st.markdown("<h1 style='text-align: center;'>Asthma Symptoms Checker</h1>", unsafe_allow_html=True)

lusername = st.sidebar.text_input("Username")
if lusername:
    age, gender = table.entity_retrieve(lusername)

    c1, c2, c3 = st.columns(3)
    with c1:
        Tiredness = st.selectbox("Tiredness", ["<Select>", "Yes", "No"], index=0)
        Dry_Cough = st.selectbox("Dry Cough", ["<Select>", "Yes", "No"], index=0)
        Difficulty_in_Breathing = st.selectbox("Difficulty in Breathing", ["<Select>", "Yes", "No"], index=0)
    with c2:
        Sore_Throat = st.selectbox("Sore Throat", ["<Select>", "Yes", "No"], index=0)
        Pains = st.selectbox("Pains", ["<Select>", "Yes", "No"], index=0)
    with c3:
        Runny_Nose = st.selectbox("Runny Nose", ["<Select>", "Yes", "No"], index=0)
        Nasal_Congestion = st.selectbox("Nasal Congestion", ["<Select>", "Yes", "No"], index=0)

    if "<Select>" not in [Tiredness, Dry_Cough, Difficulty_in_Breathing, Sore_Throat, Pains, Runny_Nose, Nasal_Congestion]:
        data = {
            "input_data": {
                "columns": [
                    "Tiredness", "Dry-Cough", "Difficulty-in-Breathing", "Sore-Throat", "Pains", "Nasal-Congestion", "Runny-Nose", "Age", "Gender"
                ],
                "index": [1],
                "data": [
                    [1 if Tiredness == 'Yes' else 0, 
                     1 if Dry_Cough == 'Yes' else 0,
                     1 if Difficulty_in_Breathing == 'Yes' else 0,
                     1 if Sore_Throat == 'Yes' else 0,
                     1 if Pains == 'Yes' else 0,
                     1 if Nasal_Congestion == 'Yes' else 0,
                     1 if Runny_Nose == 'Yes' else 0,
                     agecalculator(age),
                     1 if gender == 'Male' else 0]
                ]
            }
        }

        # File path where you want to save the JSON file
        file_path = "input.json"

        # Write JSON data to file
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        if st.button("Predict"):

            with st.spinner("Predicting..."):
                response = model.invoke_endpoint()  # Assuming model.py has a function named invoke_endpoint(file_path)
                time.sleep(3)
            response = response.strip('[""]')
            if response == 'Mild':
                st.warning("You have mild symptoms of Asthma.")
                st.info("You need to monitor your symptoms and seek medical attention if they worsen.")
                with st.spinner(text="Sending email alert to your doctor..."):
                    emailalert(lusername, age, response, Tiredness, Dry_Cough, Difficulty_in_Breathing, Sore_Throat, Pains, Runny_Nose, Nasal_Congestion)
                    time.sleep(3)
                    st.success("Email alert sent successfully!")
                
                with st.expander("Remedies for mild symptoms"):
                    st.write("- Take prescribed asthma medication as directed by your doctor.")
                    st.write("- Avoid triggers such as smoke, dust, and pollen.")
                    st.write("- Practice deep breathing exercises and relaxation techniques.")
                    st.write("- Keep your living space clean and free of allergens.")
                    st.write("- Stay hydrated and maintain a healthy diet.")
                    st.write("- Get regular exercise, but avoid strenuous activities that may trigger symptoms.")
                    st.write("- Monitor your symptoms and seek medical attention if they worsen.")
                
                
            elif response == 'Moderate':
                st.info("You have moderate symptoms of Asthma.")
                st.warning("Please consult your doctor for further evaluation and treatment.")
                with st.spinner(text="Sending email alert to your doctor..."):
                    emailalert(lusername, age, response, Tiredness, Dry_Cough, Difficulty_in_Breathing, Sore_Throat, Pains, Runny_Nose, Nasal_Congestion)
                    time.sleep(3)
                    st.success("Email alert sent successfully!")
                with st.expander("Remedies for moderate symptoms"):
                    st.write("- Follow your asthma action plan as prescribed by your doctor.")
                    st.write("- Take prescribed asthma medication to manage symptoms.")
                    st.write("- Avoid triggers that worsen your symptoms.")
                    st.write("- Monitor your peak flow readings and symptoms regularly.")
                    st.write("- Seek medical attention if your symptoms worsen or do not improve.")
            else:
                st.info("You do not have any symptoms of Asthma.")
            table2.entity_update(lusername, response)
    else:
        st.warning("Please select all symptom options.")
else:
    st.warning("Please enter the username to use the Astma symptom tracker.")
