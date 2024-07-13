import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

athletes=pd.read_csv('data/athlete_events.csv')
regions=pd.read_csv('data/noc_regions.csv')

def data_preprocessor():
    global athletes,regions
    df=pd.merge(athletes,regions,on='NOC')
    df.drop_duplicates(inplace=True)
    df['Medal'].fillna("No_medal",inplace=True)
    summer=df[df['Season']=='Summer']
    winter=df[df['Season']=='Winter']
    return summer,winter


def duplicate_rows_remover(df1,df2):
    df1 = df1.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event'])
    df2 = df2.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event'])
    return df1,df2


def medal_tally_calculator(df):
    medal_counts = df.groupby(['NOC','Medal']).size().reset_index(name='Counts')
    medal_pivot = medal_counts.pivot(index='NOC', columns='Medal', values='Counts').fillna(0)
    medal_pivot = medal_pivot.astype(int)


    if 'No_medal' in medal_pivot.columns:
        medal_pivot.drop(columns='No_medal', inplace=True)

        medal_pivot['Total_medals'] = medal_pivot[['Bronze','Gold','Silver']].sum(axis=1)
        return medal_pivot



def country_wise_search(noc,pivot_table):
    if noc in pivot_table.index:
        details={
            "Gold": pivot_table.loc[noc,"Gold"],
            "Silver": pivot_table.loc[noc,"Silver"],
            "Bronze": pivot_table.loc[noc,"Bronze"],
            "Total_medals": pivot_table.loc[noc,"Total_medals"]
        }
        return details
    else:
        print("No noc Exist")


def plot_medals(year,country,df):
    medal_counts = df.groupby(['Year','region','Medal']).size().unstack(fill_value=0)
    medal_counts = medal_counts.reset_index()
    medal_counts['total_medals'] = medal_counts['Gold'] + medal_counts['Silver'] + medal_counts['Bronze']

    filtered_df = medal_counts[(medal_counts['Year']==year) & (medal_counts['region']==country)]
    
    gold = filtered_df['Gold'].values[0]
    silver = filtered_df['Silver'].values[0]
    bronze = filtered_df['Bronze'].values[0]
    total_medals = filtered_df['total_medals'].values[0]
    
    fig,ax = plt.subplots()
    medals = ['Gold','Silver','Bronze','total_medals']
    counts = [gold,silver,bronze,total_medals]
    ax.bar(medals,counts,color=['gold','silver','brown','green'])
    st.pyplot(fig)



def year_analysis(country, df):
    medal_counts = df.groupby(['Year', 'region', 'Medal']).size().unstack(fill_value=0)
    medal_counts = medal_counts.reset_index()
    medal_counts['total_medals'] = medal_counts.get('Gold', 0) + medal_counts.get('Silver', 0) + medal_counts.get('Bronze', 0)
    return medal_counts

def plot_year_progress(country, df):
    medal_counts = year_analysis(country, df)
    filtered_df = medal_counts[medal_counts['region'] == country]
    fig, ax = plt.subplots()
    ax.plot(filtered_df['Year'], filtered_df.get('Gold', 0), color='Gold', label='GOLD', marker='o', linestyle='-')
    ax.plot(filtered_df['Year'], filtered_df.get('Silver', 0), color='Silver', label='SILVER', marker='o', linestyle='-')
    ax.plot(filtered_df['Year'], filtered_df.get('Bronze', 0), color='brown', label='BRONZE', marker='o', linestyle='-')
    ax.plot(filtered_df['Year'], filtered_df['total_medals'], color='green', label='TOTAL_MEDAL', marker='o', linestyle='-')
    ax.legend()
    st.pyplot(fig)
