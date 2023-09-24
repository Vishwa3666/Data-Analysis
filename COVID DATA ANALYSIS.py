#!/usr/bin/env python
# coding: utf-8

# In[2]:


pip install plotly


# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime


# In[2]:


covid_df = pd.read_csv("covid_19_india.csv")


# In[3]:


covid_df.head(10)


# In[4]:


covid_df.info()


# In[5]:


covid_df.describe()


# In[6]:


vaccine_df = pd.read_csv("covid_vaccine_statewise.csv")


# In[7]:


vaccine_df.head(7)


# In[8]:


covid_df.drop(["Sno","Time","ConfirmedIndianNational","ConfirmedForeignNational"],inplace=True,axis=1)


# In[9]:


covid_df.head()


# In[10]:


covid_df['Date'] = pd.to_datetime(covid_df['Date'], format = '%Y-%m-%d')


# In[11]:


# active case
# confirmed-(cure+death)
covid_df['Active_Cases'] = covid_df['Confirmed']-(covid_df['Cured'] + covid_df['Deaths'])
covid_df.head()


# In[12]:


# confirmed deaths and cured cases for each of the states or union territory(pivot_table)
statewise = pd.pivot_table(covid_df , values = ["Confirmed","Deaths","Cured"], index = "State/UnionTerritory", aggfunc = max)


# In[13]:


print(statewise)


# In[14]:


# recovery rate
statewise["Recovery Rate"] = statewise["Cured"]*100/statewise["Confirmed"]


# In[15]:


# mortality rate
statewise["Mortality Rate"] = statewise["Deaths"]*100/statewise["Confirmed"]


# In[16]:


statewise = statewise.sort_values(by = "Confirmed" , ascending= False)


# In[17]:


statewise.style.background_gradient(cmap = "cubehelix")


# In[18]:


# top 10 active cases states
top_10_active_cases = covid_df.groupby(by = 'State/UnionTerritory').max()[['Active_Cases','Date']].sort_values(by = ['Active_Cases'],ascending = False).reset_index()
fig = plt.figure(figsize = (16,9))
plt.title("Top 10 states with most active cases in india",size=25)
ax = sns.barplot(data = top_10_active_cases.iloc[:10], y = "Active_Cases", x = "State/UnionTerritory", linewidth=2,edgecolor='red')
plt.xlabel("States")
plt.ylabel("Total active cases")
plt.show()


# In[19]:


# Top states with highest deaths

top_10_deaths = covid_df.groupby(by = 'State/UnionTerritory').max()[['Deaths','Date']].sort_values(by = ['Deaths'],ascending = False).reset_index()
fig = plt.figure(figsize=(18,5))
plt.title("Top 10 states with most deaths",size=25)
ax = sns.barplot(data = top_10_deaths.iloc[:12], y = "Deaths", x = "State/UnionTerritory",linewidth = 2, edgecolor = 'black')
plt.xlabel("States")
plt.ylabel("Total Death Cases")
plt.show()


# In[20]:


# Growth trend

fig = plt.figure(figsize = (12,6))
ax = sns.lineplot(data=covid_df[covid_df['State/UnionTerritory'].isin(['Maharashtra','Karnataka','Kerela','Tamil Nadu','Uttar Pradesh'])], x='Date', y='Active_Cases', hue='State/UnionTerritory')
ax.set_title("Top 5 Affected States in India",size = 16)


# In[21]:


vaccine_df.head()


# In[22]:


vaccine_df.rename(columns = {'Updated On' : 'Vaccine_date'}, inplace = True)


# In[23]:


vaccine_df.info()


# In[24]:


vaccine_df.isnull().sum()


# In[26]:


Vaccination = vaccine_df.drop(columns = ['Sputnik V (Doses Administered)','AEFI','18-44 Years (Doses Administered)','45-60 Years (Doses Administered)','60+ Years (Doses Administered)'],axis = 1)


# In[28]:


Vaccination.head()


# In[29]:


# Male vs Female Vaccination
male = Vaccination["Male(Individuals Vaccinated)"].sum()
female = Vaccination["Female(Individuals Vaccinated)"].sum()
px.pie(names=["Male","Female"], values=[male, female], title = "Male and Female Vaccination")


# In[30]:


# Remove rows where state is India
vaccine = vaccine_df[vaccine_df.State!='India']
vaccine


# In[31]:


vaccine.rename(columns = {"Total Individuals Vaccinated": "Total"},inplace = True)
vaccine.head()


# In[32]:


# Most vaccinated state

max_vac = vaccine.groupby('State')['Total'].sum().to_frame('Total')
max_vac = max_vac.sort_values('Total', ascending = False)[:5]
max_vac


# In[41]:


fig = plt.figure(figsize =(10,5))
plt.title("Top 5 Vaccinated States in India", size = 20)
x = sns.barplot(data = max_vac.iloc[:10], y = max_vac.Total, x = max_vac.index, linewidth = 2, edgecolor = 'black')
plt.xlabel("States")
plt.ylabel("Vaccination")
plt.show()


# In[ ]:




