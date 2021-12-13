import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
from PIL import Image





def readData():
    return pd.read_csv('volcanoes.csv', encoding = 'Latin-1')

def filterMap(filterType, df):
    filter = df[filterType].unique()
    dataSelection = st.selectbox(f"Select a {filterType} to display on the map: ",list(filter))
    DF1 = pd.DataFrame(df, columns=['Volcano Name','Latitude','Longitude', filterType])
    DF1 = DF1.loc[DF1[filterType].isin([dataSelection])]
    DF1 = DF1.rename(columns = {"Latitude":"lat", "Longitude":"lon"})
    return DF1

def Top10(df, num):   #comment out section: ctrl+/
    df1 = pd.DataFrame(df, columns=['Volcano Name', 'Elevation (m)', 'Primary Volcano Type'])
    df1= df1.sort_values(['Elevation (m)'], ascending=False)[:num]
    st.subheader(f"Table of the {num} Tallest Volcanoes")
    st.write(df1)
    table3 = pd.pivot_table(df1,index=['Volcano Name'],aggfunc={'Elevation (m)':np.sum}).sort_values(by=['Elevation (m)'],ascending=False)
    plt.figure()
    plt.rcParams["font.size"] = 8
    st.subheader(f"Bar Chart of the {num} Tallest Volcanoes")
    table3.plot(kind='bar');

    return plt

def pieChart(df, filterType):
    filter = df[filterType].unique()
    lst = [df.loc[df[filterType].isin([f])].shape[0] for f in filter]
    plt.figure()
    plt.rcParams["font.size"] = 23
    plt.pie(lst, labels = filter, autopct='%.1f', radius=6)
    return plt


def heat(df):
    rocks = list(set(df['Dominant Rock Type'].tolist()))
    regions = list(set(df['Region'].tolist()))
    reg2idx = {regions[i]:i for i in range(len(regions))}
    rock2idx = {rocks[i]:i for i in range(len(rocks))}

    matrix = np.zeros((len(rocks), len(regions)))
    for i in range(len(df)):
        rock = df.loc[i, 'Dominant Rock Type']
        region = df.loc[i, 'Region']
        matrix[rock2idx[rock], reg2idx[region]] += 1
    n = int(np.max(matrix))
    matrix = np.log(matrix + 1)
    cmap = sns.color_palette("YlGnBu", n)
    ax = sns.heatmap(matrix, cmap=cmap,  xticklabels = regions, yticklabels = rocks,)
    colorbar = ax.collections[0].colorbar
    r = colorbar.vmax - colorbar.vmin
    colorbar.set_ticklabels([int(np.exp(i)) for i in range(5)])
    plt.show()
    return plt





def allElevs(dfRegion):

    elevs = [row['Elevation (m)'] for i, row in dfRegion.iterrows()]
    regions = [row['Region'] for i, row in dfRegion.iterrows()]
    dict = {}
    for region in regions:
        dict[region] = []

    for i in range(len(elevs)):
        dict[regions[i]].append(elevs[i])
    return dict

def avgElevs(elev):
    dict = {}
    for key in elev.keys():
        dict[key] = np.mean(elev[key])
    return dict

def barChartAvgs(avgs):

    x = avgs.keys()
    y = avgs.values()
    plt.figure()
    plt.rcParams["font.size"] = 8
    plt.bar(x, y)
    plt.xlabel("Volcano Name")
    plt.ylabel("Elevation (m)")
    plt.show()
    st.pyplot(plt)


def main():
    df = readData()
    img = Image.open("volcano.jpg")
    st.image(img, width=600)
    st.title("Volcanoes")
    st.header("Finding Volcanoes by Region")
    #Filter Data by Region
    st.map(filterMap('Region', df))


    #Filter Data by Type
    st.header("Finding Volcanoes by Primary Volcano Type")
    st.map(filterMap('Primary Volcano Type', df))

    #Pie Charts
    st.header("Frequency Statistics")
    filterType = st.radio('Select a data subset', ['Region', 'Dominant Rock Type', 'Tectonic Setting'])
    st.pyplot(pieChart(df, filterType))


    #Bar Charts
    st.subheader("Use the sidebar!")
    num = st.sidebar.slider('Number of Volcanoes',1,10,1)
    st.header(f"{num} Tallest Volcanoes")
    st.pyplot(Top10(df, num))

    st.header("Average Elevation of Volcanoes in Specific Regions")
    dfRegion= df.loc[df['Region'].isin(["Mediterranean and Western Asia", "New Zealand to Fiji", "Indonesia"])]
    elev = allElevs(dfRegion)
    avgs = avgElevs(elev)
    barChartAvgs(avgs)



    #Heat Map
    st.header("Charting the Relationship between Region and Rock Type")
    st.pyplot(heat(df))



main()







