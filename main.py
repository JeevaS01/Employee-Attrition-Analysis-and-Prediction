import streamlit as st
import pandas as pd
import numpy as np
from joblib import load
from sklearn.preprocessing import OrdinalEncoder,LabelEncoder
import pymysql
import plotly.express as px 
from streamlit_lottie import st_lottie
import json

#streamlit UI
def lottie_file(file):
    with open(file,"r", encoding="utf-8") as f:
        return json.load(f)
job=lottie_file("C:/Users/LOQ/Documents/GUVI DS/Mini-Project/Employee Attrition 03/icon/job.json")
metrics=lottie_file("C:/Users/LOQ/Documents/GUVI DS/Mini-Project/Employee Attrition 03/icon/metric.json")
graph=lottie_file("C:/Users/LOQ/Documents/GUVI DS/Mini-Project/Employee Attrition 03/icon/graph.json")
search=lottie_file("C:/Users/LOQ/Documents/GUVI DS/Mini-Project/Employee Attrition 03/icon/searching.json")


model1 = load('model.joblib')
model2 = load('model_2.joblib')

st.set_page_config(layout="wide")

col1, col2= st.columns([1,9])
with col1:
    st_lottie(job, height=150, width=150)
with col2:
    st.title("Employee Attrition Analysis and Prediction")
    st.write("This app analyzes employee attrition data and predicts whether an employee is likely to leave the company based on various factors.")

st.markdown("## Discription of Employee Attrition")
st.write("""Employee turnover poses a significant challenge for organizations, resulting in increased costs, reduced productivity, and team disruptions. Understanding the factors driving attrition and predicting at-risk employees is critical for effective retention strategies. This project aims to analyze employee data, identify key drivers of attrition, and build predictive models to support proactive decision-making in workforce management.""")

#database connection
def create_con():
    try:
        my_con=pymysql.connect(host='127.0.0.1',
                               user='root',
                               password='Jeevanick@91',
                               database='employee',
                               cursorclass=pymysql.cursors.DictCursor)
        return my_con
    except Exception as e:
        st.error(f"Error connecting to database:{e}")
        return None
def fetch_data(query):
    connection=create_con()
    if connection:
        try:
            with connection.cursor() as cur:
                cur.execute(query)
                result=cur.fetchall()
                df=pd.DataFrame(result)
                return df
        finally:
            connection.close()
    else:
        return pd.DataFrame()

#Data Display
data=fetch_data("SELECT * FROM `employee-attrition`")
st.subheader("Employee Attrition Data")
st.dataframe(data,use_container_width=True)

st.markdown("-----")

#metrics
col1, col2= st.columns([1,11])
with col1:
    st_lottie(metrics, height=90, width=90)
with col2:
    #st.markdown("###          ")
    st.markdown("## Employee Attrition Key Metrics")
col1, col2, col3,col4 = st.columns(4)
with col1:
    total_employees = data.shape[0]
    st.metric("Total Employees", total_employees)
with col2:
    attrition_count = data['Attrition'].value_counts().get('Yes', 0)
    st.metric("Total Attritions", attrition_count)
with col3:
    avg_monthly_income = data['MonthlyIncome'].mean()
    st.metric("Avg Monthly Income", f"₹{avg_monthly_income:,.2f}")
with col4:
    avg_years_at_company = data['YearsAtCompany'].mean()
    st.metric("Avg Years at Company", f"{avg_years_at_company:.1f} years")
st.markdown("---")

#data visulization
col1, col2= st.columns([1,11])
with col1:
    st_lottie(graph, height=90, width=90)
with col2:
    st.markdown("## Attrition Analysis Visualizations")
select = st.selectbox("Select Visualization",
                      ["Attrition by Department"," Attrition by Gender",
                       "Attrition by Job Satisfaction","Attrition by OverTime","Attrition by Marital Status",
                       "Attrition by Job Involvement",' Attrition by Monthly Income',
                        "Attrition by Total Working Years","Attrition by Years at Company"
                       ])

if select=="Attrition by Department":
    fig=px.histogram(data,x='Department',color='Attrition',barmode='group', color_discrete_sequence=["#FF4500", "#FF8C00"],
                     title="Attrition by Department")
    st.plotly_chart(fig,use_container_width=True)
elif select==" Attrition by Gender":
    fig=px.histogram(data,x='Gender',color='Attrition',barmode='group', color_discrete_sequence=["#FF4500", "#FF8C00"],
                     title="Attrition by Gender")
    st.plotly_chart(fig,use_container_width=True)   
elif select=="Attrition by Job Satisfaction":
    fig=px.histogram(data,x='JobSatisfaction',color='Attrition',barmode='group', color_discrete_sequence=["#FF4500", "#FF8C00"],
                     title="Attrition by Job Satisfaction")
    st.plotly_chart(fig,use_container_width=True)
elif select=="Attrition by OverTime":
    fig=px.histogram(data,x='OverTime',color='Attrition',barmode='group', color_discrete_sequence=["#FF4500", "#FF8C00"],
                     title="Attrition by OverTime")
    st.plotly_chart(fig,use_container_width=True)
elif select=="Attrition by Marital Status":
    fig=px.histogram(data,x='MaritalStatus',color='Attrition',barmode='group', color_discrete_sequence=["#FF4500", "#FF8C00"],
                     title="Attrition by Marital Status")
    st.plotly_chart(fig,use_container_width=True)
elif select=="Attrition by Job Involvement":
    fig=px.histogram(data,x='JobInvolvement',color='Attrition',barmode='group', color_discrete_sequence=["#FF4500", "#FF8C00"],
                     title="Attrition by Job Involvement")
    st.plotly_chart(fig,use_container_width=True)
elif select==" Attrition by Monthly Income":
    fig=px.histogram(data,x='MonthlyIncome',color='Attrition',barmode='group', color_discrete_sequence=["#FF4500", "#FF8C00"],
                     title="Attrition by Monthly Income")
    st.plotly_chart(fig,use_container_width=True)
elif select=="Attrition by Total Working Years":
    fig=px.histogram(data,x='TotalWorkingYears',color='Attrition',barmode='group', color_discrete_sequence=["#FF4500", "#FF8C00"],
                     title="Attrition by Total Working Years")
    st.plotly_chart(fig,use_container_width=True)
elif select=="Attrition by Years at Company":
    fig=px.histogram(data,x='YearsAtCompany',color='Attrition',barmode='group', color_discrete_sequence=["#FF4500", "#FF8C00"],
                     title="Attrition by Years at Company")
    st.plotly_chart(fig,use_container_width=True)

st.markdown("---")
#Prediction Models
col1, col2= st.columns([1,11])
with col1:
    st_lottie(search, height=90, width=90)
with col2:
    st.markdown("## Employee Attrition Prediction Models")
tag1, tag2= st.tabs(["Predict Employee Attrition","Predict Employee Perfomance Rating"])

with tag1:
    st.subheader("Predict Employee Attrition")
    st.write("Predict whether an employee is likely to leave the company based on various factors using Machine Learning models.")
    with st.form("employee_details"):
        Age=st.slider("Age", 18, 60, 18)
        Department=st.selectbox("Select Department", ['Sales', 'Research & Development', 'Human Resources'])
        Gender=st.selectbox("Select Gender", ['Female','Male'])
        JobInvolvement=st.slider("Job Involvement", 1, 4, 1)
        JobSatisfaction=st.slider("Job Satisfaction", 1, 4, 1)
        MaritalStatus=st.selectbox("Select Marital Status", ['Single', 'Married', 'Divorced'])
        MonthlyIncome=st.number_input("Monthly Income", min_value=1000, max_value=200000, value=1000)
        NumCompaniesWorked=st.slider("Number of Companies Worked", 0, 10, 0)
        OverTime=st.selectbox("OverTime", ['Yes', 'No'])
        TotalWorkingYears=st.slider("Total Working Years", 0, 40, 0)
        YearsAtCompany=st.slider("Years At Company", 0, 40, 0)
        submitted = st.form_submit_button("PREDICT ATTRITION")
    

data= {
    'Age': Age, 
    'Department': Department,
    'Gender': Gender,
    'JobInvolvement': JobInvolvement,   
    'JobSatisfaction': JobSatisfaction,
    'MaritalStatus': MaritalStatus,
    'MonthlyIncome': MonthlyIncome,
    'NumCompaniesWorked': NumCompaniesWorked,
    'OverTime': OverTime,
    'TotalWorkingYears': TotalWorkingYears,
    'YearsAtCompany': YearsAtCompany
}

df=pd.DataFrame([data])

ord=OrdinalEncoder(categories=[['Human Resources','Sales','Research & Development']])
df['Department']=ord.fit_transform(df[['Department']])
ord=OrdinalEncoder(categories=[['Divorced','Married','Single']])
df["MaritalStatus"]=ord.fit_transform(df[["MaritalStatus"]])
ord=OrdinalEncoder(categories=[['No','Yes']])
df["OverTime"]=ord.fit_transform(df[["OverTime"]])
ord=OrdinalEncoder(categories=[['Female','Male']])
df["Gender"]=ord.fit_transform(df[["Gender"]])


if submitted:
    prediction=model1.predict(df)
    if prediction[0]==1:
        st.error("Yes,The employee is likely to leave the company.")
    else:
        st.success("No,The employee is likely to stay with the company.")


with tag2:
    st.subheader("Predict Employee Perfomance Rating")
    st.write("Predict the performance rating of an employee based on various factors using Machine Learning models.")
    with st.form("employee_perfomance"):
        PercentSalaryHike=st.slider("Percent Salary Hike", 11, 25, 11)
        YearsInCurrentRole=st.slider("Years In Current Role", 0, 18, 0)
        Department=st.selectbox("Select Department", ['Sales', 'Research & Development', 'Human Resources'])
        YearsSinceLastPromotion=st.slider("Years Since Last Promotion", 0, 15, 0)
        TotalWorkingYears=st.slider("Total Working Years", 0, 40, 0)
        OverTime=st.selectbox("OverTime", ['Yes', 'No'])
        Gender=st.selectbox("Select Gender", ['Female','Male'])
        RelationshipSatisfaction=st.slider("Relationship Satisfaction", 1, 4, 1)
        EnvironmentSatisfaction=st.slider("Environment Satisfaction", 1, 4, 1)      
        JobInvolvement=st.slider("Job Involvement", 1, 4, 1)
        BusinessTravel=st.selectbox("Business Travel", ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely'])
    
        submitted = st.form_submit_button("PREDICT PERFOMANCE RATING")

   
    data= {
        'PercentSalaryHike': PercentSalaryHike,
        'YearsInCurrentRole': YearsInCurrentRole,   
        'Department': Department,
        'YearsSinceLastPromotion': YearsSinceLastPromotion,
        'TotalWorkingYears': TotalWorkingYears,
        'OverTime': OverTime,
        'Gender': Gender,
        'RelationshipSatisfaction': RelationshipSatisfaction,   
        'EnvironmentSatisfaction': EnvironmentSatisfaction,
        'JobInvolvement': JobInvolvement,
        'BusinessTravel': BusinessTravel}



    df=pd.DataFrame([data])
    ord=OrdinalEncoder(categories=[['Non-Travel', 'Travel_Frequently', 'Travel_Rarely']])
    df['BusinessTravel']=ord.fit_transform(df[['BusinessTravel']])
    ord=OrdinalEncoder(categories=[['Human Resources','Sales','Research & Development']])
    df['Department']=ord.fit_transform(df[['Department']])
    ord=OrdinalEncoder(categories=[['No','Yes']])
    df["OverTime"]=ord.fit_transform(df[["OverTime"]])  
    ord=OrdinalEncoder(categories=[['Female','Male']])
    df["Gender"]=ord.fit_transform(df[["Gender"]])
    

    if submitted:
        prediction=model2.predict(df)
        if prediction[0]==0:
            st.info(f"The predicted performance rating of the employee is (3/5) :'Needs Improvement'")
        elif prediction[0]==1:
            st.info(f"The predicted performance rating of the employee is (4/5) : 'Good'")



        