# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 12:08:20 2020

@author: DELL
"""

import requests
from plotly.offline import plot
from pandas import DataFrame as df
import plotly.graph_objects as go
import time

r= requests.get('https://coronavirus-tracker-api.herokuapp.com/v2/locations')


r= df(r.json()['locations'])

lon= []
lat= []
for x in r['coordinates']:
    lon.append(x['longitude'])
    lat.append(x['latitude'])

r['lat']=df(lat)
r['lon']=df(lon)


for x in r.head():
    print(x)

confirmed=[]
confirmed_size=[]
deaths=[]
deaths_size=[]
recovered=[]
recovered_size=[]

for x in r['latest']:
    confirmed.append(x['confirmed'])
    confirmed_size.append(int(x['confirmed'])/2000)
    deaths.append(x['deaths'])
    deaths_size.append(int(x['deaths'])/200)
    recovered.append(x['recovered'])
    recovered_size.append(int(x['recovered'])/100)
    
    
    
"Creating new df columns on r"

r['confirmed']=df(confirmed)
r['confirmed_size']=df(confirmed_size)
r['deaths']=df(deaths)
r['deaths_size']=df(deaths_size)
r['recovered']=df(recovered)
r['recovered_size']=df(recovered_size)

print(r)

layout = go.Layout(
        height=800,
        mapbox_style="white-bg",
        autosize=True,
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ]
            }
        ]
    )

"""Setup Plotly Graph"""
map_confirmed=go.Scattermapbox(
        customdata=r.loc[:,['confirmed','deaths','recovered']],
        name='Confirmed Cases',
        lon=r['lon'],
        lat=r['lat'],
        text=r['country'],
        hovertemplate=
        "<b>%{text}</b><br><br>"+
        "Confirmed: %{customdata[0]}<br>" +
        "<extra></extra>"
        ,
        mode='markers',
        showlegend=True,
        marker=go.scattermapbox.Marker(size=r['confirmed_size'][0:230],color='yellow',opacity=0.7)
        )
    

map_deaths=go.Scattermapbox(
        name='Deaths',
        customdata=r.loc[:,['confirmed','deaths','recovered']],
        lon=r['lon'],
        lat=r['lat'],
        text=r['country'],
        hovertemplate="<b>%{text}</b><br><br>"+
        "Deaths: %{customdata[1]}<br>" +
        "<extra></extra>"
        ,
        mode='markers',
        showlegend=True,
        marker=go.scattermapbox.Marker(
                size=r['deaths_size'][0:230],
                color='black',
                opacity=0.7
                )
        )


map_recovered=go.Scattermapbox(
        name='Recovered',
        customdata=r.loc[:,['confirmed','deaths','recovered']],
        lon=r['lon'],
        lat=r['lat'],
        text=r['country'],
        hovertemplate="<b>%{text}</b><br><br>"+
        "Recovered: %{customdata[2]}<br>" +
        "<extra></extra>"
        ,
        mode='markers',
        showlegend=True,
        marker=go.scattermapbox.Marker(
                size=r['recovered_size'][0:230],
                color='green',
                opacity=0.7
                )
        )



data=[map_confirmed,map_deaths,map_recovered]
fig=go.Figure(data=data,layout=layout)
plot(fig, auto_open=True)

