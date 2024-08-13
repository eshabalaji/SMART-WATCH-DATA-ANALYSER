import streamlit as st    #For GUI
from datetime import datetime, timedelta #for date
from scipy.misc import electrocardiogram
import numpy as np  #for arrays
import matplotlib.pyplot as plt #To plot graphs
import smtplib #Simple mail transfer protocol-used to transfer mail
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.title("SMART WATCH DATA ANALYSER")

# Input fields
age = st.number_input("Enter your age", 0, 100)
gender = st.radio("Pick your gender", ["Male", "Female", "Others"])
col, col2 = st.columns(2)
bedtime = col.time_input("Enter your bed time:")
wakeuptime = col2.time_input("Enter your wake up time")

# Convert times to datetime objects
bed_datetime = datetime.combine(datetime.today(), bedtime)
wakeup_datetime = datetime.combine(datetime.today(), wakeuptime)
if wakeup_datetime <= bed_datetime:
    wakeup_datetime += timedelta(days=1)

# Calculate the duration
sleep_duration = wakeup_datetime - bed_datetime
sleep_duration_hours = sleep_duration.total_seconds() / 3600

if sleep_duration_hours< 0:
    st.error('Invalid sleep duration')

col, col2 = st.columns(2)
caffeine = col.number_input("Enter your caffeine consumption (In mL)", 0, 100, value=0)
alcohol = col2.number_input("Enter your alcohol consumption (In mL)", 0, 100, value=0)
col, col1, col2, col3 = st.columns(4)
rem = col.text_input("REM sleep percentage")
deep = col1.text_input("Deep sleep percentage")
light = col2.text_input("Light sleep percentage")
heart = col3.text_input("Enter Heart rate")
awakening = st.slider("Number of times you woke up?", 0, 5, 0)
n = st.slider("Exercise days", 0, 7)

# Convert the input values to integers if possible
try:
    rem = int(rem) if rem else 0
    deep = int(deep)
    light = int(light)
    alcohol = int(alcohol)
    awakening = int(awakening)
    caffeine = int(caffeine)
    heart = int(heart)
except ValueError:
    st.error("Please enter valid numerical values for sleep percentages.")

# Functions to check for sleep apnea
def sleep_apnea(rem, awakening):
    if rem < 20:
        return 'Yes, REM cycle is low'
    elif awakening >= 4:
        return 'Yes, awakenings are more'
    else:
        return "Don't have Sleep apnea"

def suggestions(row, alcohol, caffeine):
    if row != 'No':
        if alcohol > 50 and caffeine > 10:
            return ('The best thing you can do is avoid consuming alcohol in the hours before bed to minimize its effects. '
                    'It’s recommended to avoid drinking caffeine at least 2 hours before bedtime to lessen your chance of having insomnia.')
        elif alcohol > 50:
            return 'The best thing you can do is avoid consuming alcohol in the hours before bed to minimize its effects.'
        elif caffeine > 10:
            return 'It’s recommended to avoid drinking caffeine at least 2 hours before bedtime.'
    return 'None'

#to check heart rate
def check_heart_rate(heart):
    try:
        if heart >= 60 and heart <= 100:

            return f"Heart rate is normal: {heart} BPM"
        elif heart < 60:
            return "Heart rate is low (bradycardia). Consult a doctor."
        else:
            return "Heart rate is high (tachycardia). Consult a doctor."
    except:print('Invalid input')


def ecg_display():
    st.title("ECG Data Visualization")
    
    # Load the ECG data
    try:
        ecg = electrocardiogram()  
    except Exception as e:
        st.error(f"Error loading ECG data: {e}")
        return
    
    # Define the frequency
    frequency = 360
    
    # Calculate the time data
    time_data = np.arange(ecg.size) / frequency
    
    # Create the plot
    fig, ax = plt.subplots()
    ax.plot(time_data, ecg)
    ax.set_xlabel("Time in seconds")
    ax.set_ylabel("ECG in milli Volts")
    
    # Set dynamic limits for better visualization
    ax.set_xlim(time_data[0], time_data[-1])
    ax.set_ylim(min(ecg) - 0.5, max(ecg) + 0.5)
    
    # Display the plot in Streamlit
    st.pyplot(fig)

# Main analysis
row = sleep_apnea(rem, awakening)
res = suggestions(row, alcohol, caffeine)
h = check_heart_rate(heart)

if st.button("Analyse"):
    if rem >= 0 and deep >= 0 and light >= 0 and awakening >= 0 and age != 0 and sleep_duration_hours > 1:
        #row = sleep_apnea(rem, awakening)
        #res = suggestions(row, alcohol, caffeine)
        st.info(f'''
            Age : {age}\n\n
            Gender : {gender}\n\n 
            Heart Rate: {h}\n\n
            Bed time : {bedtime}\n\n 
            Wakeup Time : {wakeuptime}\n\n
            Sleep Apnea : {row}\n\n
            Suggestions : {res}\n\n
        ''')
        ecg_display()
    else:
        st.error("Fields are blank")

# Email functionality
def send_email(sender_email, receiver_email, subject, body, password):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()

st.subheader("Enter email address")
mail = st.text_input("")

if st.button("Mail the Analysis"):
    if '@' in mail:
        sender_email = 'your_mail_id' #enter your mail id 
        receiver_email = mail
        subject = 'Report'
        body = (f'''Age : {age}\n\nGender : {gender}\n\nBed time : {bedtime}
                \n\nWakeup Time : {wakeuptime}
                   
                   \n\nSleep Apnea : {row}
                   \n\nSuggestions : {res}\n\n''')
    #\n\nAverage Sleep Time : {sleep_duration}

        # Sender email password
        sender_password = 'your_password'  # Replace with actual password

        try:
            send_email(sender_email, receiver_email, subject, body, sender_password)
            st.success("Mail Sent")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error('Invalid email address')
