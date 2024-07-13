import streamlit as st
import pandas as pd
from helpers import *

summer,winter=data_preprocessor()
summer,winter = duplicate_rows_remover(summer,winter)
winter.dropna(subset=['region'],inplace=True)
summer.dropna(subset=['region'],inplace=True)



# st.dataframe(summer)
# st.dataframe(winter)

# st.write('Before')
# st.write(summer.shape)
# st.write(winter.shape)

# summer,winter=duplicate_rows_remover(summer,winter)
# st.write('After')
# st.write(summer.shape)
# st.write(winter.shape)


st.sidebar.title('MENU')
season = st.sidebar.radio("Choose Season : ",("Summer","Winter"))
options = st.sidebar.radio("options",("Medal-Tally","Country-Wise","Year-Wise","Year-Wise_progress"))



## ------MEDAL TALLY------ ##
if season=="Summer" and options=="Medal-Tally":
    st.subheader("Summer Olampic Medal Tally")
    medal_pivot_summer = medal_tally_calculator(summer)
    medal_pivot_summer = medal_pivot_summer.sort_values(by=['Gold','Silver','Bronze'],ascending=False)
    st.dataframe(medal_pivot_summer,width=700)

elif season=="Winter" and options=="Medal-Tally":
    st.subheader("Winter Olampic Medal Tally")
    medal_pivot_winter = medal_tally_calculator(winter)
    medal_pivot_winter = medal_pivot_winter.sort_values(by=['Gold','Silver','Bronze'],ascending=False)
    st.dataframe(medal_pivot_winter,width=700)


##------COUNTRY-WISE------##
def display_country_wise_search(season, medal_pivot):
    st.subheader(f"{season} Country-Wise Search")
    noc = st.selectbox("Select NOC: ", medal_pivot.index.tolist())
    details = country_wise_search(noc, medal_pivot)
    table = pd.DataFrame.from_dict(details, orient="index", columns=["value"])
    st.dataframe(table)

if season == "Summer" and options == "Country-Wise":
    medal_pivot_summer = medal_tally_calculator(summer)
    display_country_wise_search("Summer", medal_pivot_summer)

elif season == "Winter" and options == "Country-Wise":
    medal_pivot_winter = medal_tally_calculator(winter)
    display_country_wise_search("Winter", medal_pivot_winter)



##-------------YEAR-WISE------------##
elif season=="Summer" and options=="Year-Wise":
    st.subheader("Summer Year-Wise Search")

    years = sorted(summer['Year'].unique())
    selected_year = st.selectbox('Select year',years)

    countries = sorted(summer[summer['Year']==selected_year]['region'].unique())
    selected_country = st.selectbox('Select country',countries)

    plot_medals(selected_year,selected_country,summer)

elif season=="Winter" and options=="Year-Wise":
    st.subheader("Winter Year-Wise Search")

    years = sorted(winter['Year'].unique())
    selected_year = st.selectbox('Select year',years)

    countries = sorted(winter[winter['Year']==selected_year]['region'].unique())
    selected_country = st.selectbox('Select country',countries)

    plot_medals(selected_year,selected_country,winter)






##-------------YEAR-WISE ANALYSIS------------##
if season == "Summer" and options == "Year-Wise_progress":
    st.subheader("Overall analysis of a country (Summer)")
    countries = sorted(summer['region'].unique())
    selected_country = st.selectbox('Choose Country : ', countries)
    plot_year_progress(selected_country, summer)  

elif season == "Winter" and options == "Year-Wise_progress":
    st.subheader("Overall analysis of a country (Winter)")
    countries = sorted(winter['region'].unique())
    selected_country = st.selectbox('Choose Country : ', countries)
    plot_year_progress(selected_country, winter)  

else:
    st.subheader("Overall analysis of a country")
    countries = sorted(summer['region'].unique() + winter['region'].unique())
    selected_country = st.selectbox('Choose Country : ', countries)
    plot_year_progress(selected_country, summer if season == "Summer" else winter) 
