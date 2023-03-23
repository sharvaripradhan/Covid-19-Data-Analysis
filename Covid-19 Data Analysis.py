from re import X
import pandas as pd
import streamlit as st
import datetime as dt
from urllib.request import urlopen
import json
import plotly_express as px

#File paths
file1='C:/Users/Sharvari Pradhan/Downloads/assignment2Data/assignment2Data/covid_confirmed_usafacts.csv'
file2='C:/Users/Sharvari Pradhan/Downloads/assignment2Data/assignment2Data/covid_deaths_usafacts.csv'
file3='C:/Users/Sharvari Pradhan/Downloads/assignment2Data/assignment2Data/covid_county_population_usafacts.csv'

#Creating dataframes
df1=pd.read_csv(file1)
df2=pd.read_csv(file2)
df3=pd.read_csv(file3)



#Part-1-Weekly new cases for Covid-19

res1=pd.melt(df1, id_vars=df1.iloc[:,0:4], value_vars=df1.iloc[:,4:],
                var_name='Date',value_name='Positive cases')
res1['Date']=pd.to_datetime(res1['Date'])
res1=res1.groupby(['Date']).sum().reset_index()
res1 = res1.loc[res1['countyFIPS'] != 0]
res1['Positive cases']=res1['Positive cases'].diff()
res1['dayOfWeek'] = res1['Date'].dt.day_name()
for i in reversed(res1['dayOfWeek']):
    if i=='Saturday':
        break
    else:
        res1=res1.drop(res1.index[-1], axis=0 )


for i in res1['dayOfWeek']:
    if i=='Sunday':
        res1=res1.groupby([pd.Grouper(key='Date', axis=0, freq='W-Sun')]).sum().reset_index()

# res1['Date']=res1['Date']-dt.timedelta(days=7)

# res1=res1.groupby([pd.Grouper(key='Date', axis=0, freq='W-Sun')]).sum().reset_index()
res1=res1[(res1.Date!='2020-01-19T00:00:00') & (res1.Date!='2022-02-06T00:00:00')]

# st.write(res1)

fig_1 = px.line(res1,x=res1['Date'],y= res1['Positive cases'], title = 'Q1) Weekly New Cases due to Covid-19')

st.title('Covid-19 Analytics')

st.plotly_chart(fig_1)





#Part-2-Weekly deaths due to covid-19
res2=pd.melt(df2, id_vars=df2.iloc[:,0:4], value_vars=df2.iloc[:,4:],
                var_name='Date',value_name='Weekly Deaths')
res2['Date']=pd.to_datetime(res2['Date'])

res2=res2.groupby(['Date'])['Weekly Deaths'].sum().reset_index()


res2['Weekly Deaths']=res2['Weekly Deaths'].diff()
# res2['Date']=res2['Date']-dt.timedelta(days=7)
# res2=res2.groupby([pd.Grouper(key='Date', axis=0,freq='W-Sun')])['Weekly Deaths'].sum().reset_index()

res2['dayOfWeek'] = res2['Date'].dt.day_name()
for i in reversed(res2['dayOfWeek']):
    if i=='Saturday':
        break
    else:
        res2=res2.drop(res2.index[-1], axis=0 )


for i in res2['dayOfWeek']:
    if i=='Sunday':
        res2=res2.groupby([pd.Grouper(key='Date', axis=0, freq='W-Sun')]).sum().reset_index()



res2=res2[(res2.Date!='2020-01-19T00:00:00') & (res2.Date!='2022-02-06T00:00:00')]

# st.write(res2)

fig_2 = px.line(res2,x=res2['Date'],y= res2['Weekly Deaths'], title = 'Q2) Weekly Deaths due to Covid-19')

st.plotly_chart(fig_2)



#Part-3-Plot for new cases in each county

df3=df3[['countyFIPS','population']]
res3=pd.melt(df1, id_vars=df1.iloc[:,0:4], value_vars=df1.iloc[:,4:],
                var_name='Date',value_name='Positive cases')

res3['Date']=pd.to_datetime(res3['Date'])
res3=res3.groupby(['countyFIPS','Date']).sum().reset_index()
res3 = res3.loc[res3['countyFIPS'] != 0]

res3=res3.merge(df3,on='countyFIPS')

res3['Positive cases']=(res3['Positive cases']*100000)/res3['population']
res3['Positive cases']=res3['Positive cases'].diff()


res3['Date']=res3['Date']-dt.timedelta(days=7)

res3=res3.groupby(['countyFIPS',pd.Grouper(key='Date', axis=0, freq='W-Sun')])['Positive cases'].sum().reset_index().sort_values(by='Date')


res3=res3[(res3.Date!='2020-01-19T00:00:00') & (res3.Date!='2022-02-06T00:00:00')]

res3['countyFIPS']=res3['countyFIPS'].astype(str)

res3['countyFIPS'] = res3['countyFIPS'].apply(lambda x: x.zfill(5))



st.markdown('#')




st.write('Q3) New cases in each County (per 100,000 people)')

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

fig3=px.choropleth(res3, geojson=counties, locations='countyFIPS',
                            color='Positive cases',
                           color_continuous_scale="Viridis",
                           range_color=(-20, 200),
                           scope="usa",
                           labels={'Positive cases':'New Covid-19 Cases per 100,000 People'},
                           title='New cases in each County (per 100,000 people)')
fig3.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.write(fig3)



#Part-4-Plot for deaths in each county
q4=pd.melt(df2, id_vars=df2.iloc[:,0:4], value_vars=df2.iloc[:,4:],
                var_name='Date',value_name='Death cases')


q4['Date']=pd.to_datetime(q4['Date'])
q4=q4.groupby(['countyFIPS','Date']).sum().reset_index()
q4 = q4.loc[q4['countyFIPS'] != 0]

q4=q4.merge(df3,on='countyFIPS')

q4['Death cases']=(q4['Death cases']*100000)/q4['population']
q4['Death cases']=q4['Death cases'].diff()


q4['Date']=q4['Date']-dt.timedelta(days=7)


q4=q4.groupby(['countyFIPS',pd.Grouper(key='Date', axis=0, freq='W-Sun')])['Death cases'].sum().reset_index().sort_values(by='Date')

q4=q4[(q4.Date!='2020-01-19T00:00:00') & (q4.Date!='2022-02-06T00:00:00')]
#selecting one week
# f=q4['Date']=='2020-12-27T00:00:00'
# d1=q4.where(f)


q4['countyFIPS']=q4['countyFIPS'].astype(str)
q4['countyFIPS'] = q4['countyFIPS'].apply(lambda x: x.zfill(5))


# d1['countyFIPS']=d1['countyFIPS'].astype(str)
# d1['countyFIPS'] = d1['countyFIPS'].apply(lambda x: x.zfill(5))




#Choropleth PLOT

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# # week=week.astype({"countyFIPS":str})    
st.write('Death cases in each County (per 100,000 people)')

fig4=px.choropleth(q4, geojson=counties, locations='countyFIPS',
                            color='Death cases',
                           color_continuous_scale="Viridis",
                           range_color=(0, 50),
                           scope="usa",
                           labels={'Death cases':'Death cases per 100,000 people'},
                           title='Q4) Death cases in each County (per 100,000 people)')
fig4.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.write(fig4)

#Plot of part-3 using slider

week=res3.groupby(['countyFIPS',pd.Grouper(key='Date', axis=0, freq='W-Sun')])['Positive cases'].sum().reset_index().sort_values(by='Date')

val=st.select_slider('select week', options=week['Date'])

filter=res3['Date']==val
res5=res3.where(filter)

st.write('Q5)')
st.write('Use slider to change values')


with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


fig5=px.choropleth(res5, geojson=counties, locations='countyFIPS',
                            color='Positive cases',
                           color_continuous_scale="Viridis",
                           range_color=(-20, 200),
                           scope="usa",
                           labels={'Positive cases':'new cases per 100,000'})
fig5.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.write(fig5)


#Plot of part-4 using slider

week2=q4.groupby(['countyFIPS',pd.Grouper(key='Date', axis=0, freq='W-Sun')])['Death cases'].sum().reset_index().sort_values(by='Date')

val2=st.select_slider('select week for deaths', options=week2['Date'])

filter=q4['Date']==val2
d2=q4.where(filter)

st.write('Use slider to change values')

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# # week=week.astype({"countyFIPS":str})


fig=px.choropleth(d2, geojson=counties, locations='countyFIPS',
                            color='Death cases',
                           color_continuous_scale="Viridis",
                           range_color=(-20, 20),
                           scope="usa",
                           labels={'Death cases':'Death cases per 100,000'})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.write(fig)

#Animation of weekly new positive cases for covid-19

res3['Date'] = res3.Date.apply(lambda x: x.date()).apply(str)

st.write('Q6)')

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)



fig6=px.choropleth(res3, geojson=counties, locations='countyFIPS',
                            color='Positive cases',
                           color_continuous_scale="Viridis",
                           range_color=(-20, 200),
                           animation_group='countyFIPS',
                           animation_frame="Date",
                           scope="usa",
                           labels={'Positive cases':'new cases per 100,000'})
fig6.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.write(fig6)



#Animation of weekly death cases
q4['Date'] = q4.Date.apply(lambda x: x.date()).apply(str)
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# # week=week.astype({"countyFIPS":str})

fig7=px.choropleth(q4, geojson=counties, locations='countyFIPS',
                            color='Death cases',
                           color_continuous_scale="Viridis",
                           range_color=(0, 50),
                           animation_group='countyFIPS',
                           animation_frame="Date",
                           scope="usa",
                           labels={'Death cases':'Death cases per 100,000 people'},
                           title='Death cases in each County (per 100,000 people)')
fig7.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.write(fig7)
