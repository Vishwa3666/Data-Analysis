#!/usr/bin/env python
# coding: utf-8

# In[29]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[30]:


ipl = pd.read_csv('ipl_2023_dataset.csv')


# In[31]:


ipl.head()


# In[32]:


ipl.shape


# In[33]:


ipl.info()


# In[34]:


ipl.columns


# In[35]:


ipl.isnull().sum()


# In[36]:


ipl[ipl['Cost in $ (K)'].isnull()]


# In[37]:


ipl['Cost in Rs. (CR)'] = ipl['Cost in Rs. (CR)'].fillna(0)
ipl['Cost in $ (K)'] = ipl['Cost in $ (K)'].fillna(0)


# In[38]:


# unsold players or not participate in 2022
ipl[ipl['2022 Squad'].isnull()]


# In[39]:


ipl['2022 Squad'] = ipl['2022 Squad'].fillna('Not Participated')


# In[40]:


ipl.isnull().sum()


# In[41]:


teams = ipl[ipl['Cost in Rs. (CR)']>0]['2023 Squad'].unique()
teams


# In[42]:


ipl['Status'] = ipl['2023 Squad'].replace(teams, 'sold')


# In[43]:


ipl


# In[44]:


ipl[ipl['Player Name'].duplicated(keep = False)]


# In[45]:


# player praticipated in 2023 auction
ipl.shape[0]


# In[46]:


# types of players participated
types = ipl['Type'].value_counts()
types.reset_index()


# In[47]:


plt.pie(types.values, labels = types.index, labeldistance = 1.2, autopct = '%1.2f%%', shadow = True, startangle = 60)
plt.title('Role of Players Participated', fontsize = 15)
plt.plot()


# In[48]:


plt.figure(figsize=(10,5))
fig = sns.countplot(data=ipl, x='Status', palette=['Orange', 'Pink'])
plt.xlabel('Sold or Unsold')
plt.ylabel('Number of Players')
plt.title('Sold vs Unsold', fontsize=15)
plt.plot()

# below code to display the data labels for each of the bars
for p in fig.patches:
    fig.annotate(format(p.get_height(), '.0f'), 
                 (p.get_x() + p.get_width()/2., p.get_height()), 
                 ha='center', va='center', xytext=(0, 4), 
                 textcoords='offset points')




# In[49]:


ipl.groupby('Status')['Player Name'].count()


# In[50]:


# Total number of players bought by each team

plt.figure(figsize=(20,10))
fig = sns.countplot(data=ipl[ipl['2023 Squad'] != 'Unsold'], 
                    x='2023 Squad')
plt.xlabel('Team Names')
plt.ylabel('Number of Players')
plt.title('Players Bought by Each Team', fontsize=12)
plt.xticks(rotation=70)
plt.plot()

for p in fig.patches:
    fig.annotate(format(p.get_height(), '.0f'), 
                 (p.get_x() + p.get_width()/2., p.get_height()), 
                 ha='center', va='center', xytext=(0, 4), 
                 textcoords='offset points')




# In[51]:


ipl['Retention'] = ipl['Base Price']


# In[55]:


ipl['Retention'].replace(['20000000','4000000','2000000','10000000','7500000','5000000','3000000','1500000'],'From Auction', inplace = True)


# In[56]:


# Total players retained and bought
ipl.groupby(['2023 Squad','Retention'])['Retention'].count()[:-1]


# In[60]:


plt.figure(figsize = (20,10))
fig = sns.countplot(ipl[ipl['2023 Squad']!='Unsold'],x = '2023 Squad',hue = ipl['Type'])
plt.title('Players in Each Team')
plt.xlabel('Team Names')
plt.ylabel('Number of Player')
plt.xticks(rotation = 50)


# In[62]:


# Highest amount spent on a single player by each team
ipl[ipl['Retention'] == 'From Auction'].groupby(['2023 Squad'])['Cost in Rs. (CR)'].max()[:-1].sort_values(ascending = False)


# In[63]:


# Player retained at maximum price
# IN dataset they didnt mention retained players cost
ipl[ipl['Retention'] == 'Retained'].sort_values(by = 'Cost in Rs. (CR)', ascending = False).head(1)


# In[64]:


# Top 5 Bowlers picked
ipl[(ipl['Retention'] == 'From Auction') & (ipl['Type'] == 'BOWLER')].sort_values(by = 'Cost in Rs. (CR)', ascending = False)


# In[66]:


# Top 5 Batsman picked
ipl[(ipl['Retention'] == 'From Auction') & (ipl['Type'] == 'BATSMAN')].sort_values(by = 'Cost in Rs. (CR)', ascending = False)


# In[67]:


# Top 5 all rounders picked
ipl[(ipl['Retention'] == 'From Auction') & (ipl['Type'] == 'ALL-ROUNDER')].sort_values(by = 'Cost in Rs. (CR)', ascending = False)


# In[68]:


ipl = ipl.rename(columns = {'2022 Squad':'Prev_team'})


# In[73]:


unsold_players = ipl[(ipl.Prev_team != 'Not Participated') 
                     & (ipl['2023 Squad'] == 'Unsold')][['Player Name','Prev_team']]


# In[74]:


print(unsold_players)


# In[ ]:




