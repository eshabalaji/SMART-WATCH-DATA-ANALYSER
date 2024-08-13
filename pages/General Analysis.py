import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.title("General Sleep Data Analysis")
#Reading data from csv file
data=pd.read_csv('./Sleep_Efficiency.csv')
data.fillna(0, inplace=True)
st.write(data)

# Plotting setup
plt.figure(figsize=(12, 10))

# Gender Distribution
plt.subplot(2, 2, 1)
sns.countplot(x='Gender', data=data)
plt.title('Gender Distribution')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.tight_layout()

# Age Distribution
plt.subplot(2, 2, 2)
sns.histplot(data['Age'], kde=True)
plt.title('Age Distribution')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.tight_layout()

# Sleep Duration Distribution
plt.subplot(2, 2, 3)
sns.histplot(data['Sleep duration'], kde=True)
plt.title('Sleep Duration Distribution')
plt.xlabel('Sleep Duration')
plt.ylabel('Frequency')
plt.tight_layout()

# Exercise Frequency Distribution
plt.subplot(2, 2, 4)
sns.histplot(data['Exercise frequency'], kde=True)
plt.title('Exercise Frequency Distribution')
plt.xlabel('Exercise Frequency')
plt.ylabel('Frequency')
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(plt)

average_sleep_duration = round(data['Sleep duration'].mean(), 2)

#gender wise sleep analysis
mean_sleep_duration = data.groupby('Gender')['Sleep duration'].mean().round(2)

mean_sleep_female = mean_sleep_duration['Female']
mean_sleep_male = mean_sleep_duration['Male']

# Print the results

st.info(f"Average sleep duration of people is {average_sleep_duration} hours \n\nFrom the above plot, we can infer that the average sleep duration of men and women is around:\n\nFemale: {mean_sleep_female} hrs\n\nMale: {mean_sleep_male} hrs \n\n ### Therefore, women sleep longer than men.")

# Fill missing values in 'Sleep apnea prediction' column with empty string
data['Suggestions'] = data['Suggestions'].fillna('')

# Define the function for sleep apnea prediction based on other criteria
def sleep_apnea(row):
    if row['REM sleep percentage'] < 20:
        return 'Yes, REM cycle is low'
    elif row['Awakenings'] >= 4:
        return 'Yes, awakenings are more'
    else:
        return 'No'

# Apply the function to create a new column 'Sleep apnea'
data['Sleep apnea'] = data.apply(sleep_apnea, axis=1)

# Define the function for sleep apnea prediction based on conditions
def suggestions(row):
    if row['Sleep apnea'] != 'No':
        if row['Alcohol consumption'] > 0 and row['Caffeine consumption'] > 0:
            return ' The best thing you can do is avoid consuming alcohol in the hours before bed to minimize its effects.\nIt’s recommended to avoid drinking caffeine at least 2 hours before bedtime to lessen your chance of having insomnia.'
        elif row['Alcohol consumption'] > 0:
            return 'The best thing you can do is avoid consuming alcohol in the hours before bed to minimize its effects.'
        elif row['Caffeine consumption'] > 0:
            return 'It’s recommended to avoid drinking caffeine at least 2 hours before bedtime'
    return 'None'

# Apply the function to create/update 'Sleep apnea prediction' column
data['Suggestions'] = data.apply(suggestions, axis=1)

# Display the updated DataFrame in Streamlit
st.title("Sleep Apnea Prediction Data")
st.write(data)

# Create a grouped DataFrame
count_by_gender = data.groupby('Gender')['Suggestions'].value_counts().unstack().fillna(0)

# Plotting with matplotlib
plt.figure(figsize=(8, 8))
count_by_gender.plot(kind='bar', stacked=True)
plt.title('Count of Sleep Apnea by Gender')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.legend(title='Sleep Apnea')
plt.xticks(rotation=0)

# Display the plot in Streamlit
st.pyplot(plt)

#data.to_csv("./destination.csv", index=True)
st.write('''
Analyzing smartwatch sleep data, such as sleep awakenings and cycles, 
allows for early prediction of sleep apnea. This early detection enables 
timely intervention and the implementation of safety measures,
like SOS alerts for significant drops in heart rate, to prevent 
health complications during sleep.
''')

if st.button("Download the CSV file"):
    st.success('Downloaded Successfully')