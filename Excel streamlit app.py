import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(page_title='Survey Results')
st.header('Survey Results 2024')
st.subheader('How was the video?')

# Load dataframe
excel_file = 'Survey_Results.xlsx'
sheet_name = 'data'

df = pd.read_excel(excel_file, sheet_name=sheet_name, usecols='A:C', header=2)


df_participants = pd.read_excel(excel_file, sheet_name=sheet_name, usecols='G:H', header=3)
df_participants.dropna(inplace=True)


# streamlit selection
department = df['department'].unique().tolist()
ages = df['age'].unique().tolist()

age_selection = st.slider('age:',
			min_value=min(ages),
			max_value=max(ages),
			value=(min(ages), max(ages)))

department_selection = st.multiselect('deparment:',
					department,
					default=department)

# filter dataframe based on selection
mask = (df['age'].between(*age_selection)) & (df['department'].isin(department_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

# Group Dataframe After Selection
df_grouped = df[mask].groupby(by=['rating']).count()[['age']]
df_grouped = df_grouped.rename(columns={'age': 'Votes'})
df_grouped = df_grouped.reset_index()

# plot bar chart
bar_chart = px.bar(df_grouped, x='rating', y='Votes', text='Votes',
color_discrete_sequence=['#F63366']*len(df_grouped),
template='plotly_white')
st.plotly_chart(bar_chart)

# Display image & dataframe
# column = st.columns(2)
# create an images file on the directory later
# image = Image.open('images/survey.jpg')

st.dataframe(df[mask])

pie_chart = px.pie(df_participants,
		title='Total number of participants',
		values='Count of customer_id',
		names='Row Labels')

st.plotly_chart(pie_chart)
