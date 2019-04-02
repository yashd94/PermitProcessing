import numpy as np 
import pandas as pd
import plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf
import colorlover as cl
init_notebook_mode(connected=False)
def color_to_rgba(color, alpha):
    return  "rgba(%s,%s,%s,%s)" % (color+(alpha,))

NYC_Permit_Issuance = pd.read_csv("DOB_Permit_Issuance.csv.gz")
BIS_Permit_Types = pd.read_csv("BIS_Permit_Types.csv", sep='\t')

# Convert dates to a datetime format
NYC_Permit_Issuance['Filing Date'] = pd.to_datetime(NYC_Permit_Issuance['Filing Date'])
NYC_Permit_Issuance['Issuance Date'] = pd.to_datetime(NYC_Permit_Issuance['Issuance Date'])

# Add time bucket indicator

def infer_time_bucket(df):
    
    time_bucket = pd.cut(x=df['Filing Date'].dt.year,
                           bins=[1989, 1994, 1999, 2004, 2009, 2014, 2019],
                           include_lowest=True,
                           labels=['1989-1994', '1994-1999', '1999-2004', '2004-2009', '2009-2014', '2014-2019']).astype(str)
    
    df['Time period'] = time_bucket 

infer_time_bucket(NYC_Permit_Issuance)

# Derive processing times

NYC_Permit_Issuance['Processing Time'] = ""

NYC_Permit_Issuance['Processing Time'] = (NYC_Permit_Issuance['Issuance Date'] - NYC_Permit_Issuance['Filing Date'])

NYC_Permit_Issuance['Processing Time'] = NYC_Permit_Issuance['Processing Time']/np.timedelta64(1,'D')

# Restrict data to Brooklyn Corporations, infer permit types

NYC_Permit_Issuance['Job Type'] = NYC_Permit_Issuance['Job Type'].replace(['A1', 'A2', 'A3'], 'AL')
INIT_FILINGS_TIME = NYC_Permit_Issuance.loc[(NYC_Permit_Issuance['Owner\'s Business Type'].isin(['CORPORATION'])) & (NYC_Permit_Issuance['Processing Time'] > 0) & (NYC_Permit_Issuance['Permit Status'].isin(['ISSUED'])) & (NYC_Permit_Issuance['Filing Status'].isin(['INITIAL']))].groupby(['BOROUGH', 'Time period', 'Job Type']).aggregate({'Processing Time':[np.nanmean], 'BOROUGH':['count']}).reset_index()
INIT_FILINGS_TIME = INIT_FILINGS_TIME.merge(BIS_Permit_Types, on='Job Type')
INIT_FILINGS_TIME.columns = ['BOROUGH', 'Time period', 'Job Type', 'Avg Processing Time', 'Number of permits', 'Description']
job_types_list = INIT_FILINGS_TIME['Description'].unique()

# Separating by borough

INIT_FILINGS_TIME_BRONX = INIT_FILINGS_TIME.loc[INIT_FILINGS_TIME['BOROUGH'].isin(['BRONX'])]
INIT_FILINGS_TIME_MANHATTAN = INIT_FILINGS_TIME.loc[INIT_FILINGS_TIME['BOROUGH'].isin(['MANHATTAN'])]
INIT_FILINGS_TIME_BROOKLYN = INIT_FILINGS_TIME.loc[INIT_FILINGS_TIME['BOROUGH'].isin(['BROOKLYN'])]
INIT_FILINGS_TIME_STATEN = INIT_FILINGS_TIME.loc[INIT_FILINGS_TIME['BOROUGH'].isin(['STATEN ISLAND'])]
INIT_FILINGS_TIME_QUEENS = INIT_FILINGS_TIME.loc[INIT_FILINGS_TIME['BOROUGH'].isin(['QUEENS'])]


# Plotting average processing times

from collections import defaultdict

trace_bronx = defaultdict(list)
trace_man = defaultdict(list)
trace_staten = defaultdict(list)
trace_brooklyn = defaultdict(list)
trace_queens = defaultdict(list)

layout = defaultdict(list)

for i in range(len(job_types_list)):
    
    trace_bronx[i] = go.Scatter(
        x = INIT_FILINGS_TIME_BRONX.loc[INIT_FILINGS_TIME_BRONX['Description'].isin([str(job_types_list[i])])]['Time period'],
        y = INIT_FILINGS_TIME_BRONX.loc[INIT_FILINGS_TIME_BRONX['Description'].isin([str(job_types_list[i])])]['Avg Processing Time'],
        name = str(job_types_list[i]),
        mode = 'lines+markers')
                                        
    trace_man[i] = go.Scatter(
        x = INIT_FILINGS_TIME_MANHATTAN.loc[INIT_FILINGS_TIME_MANHATTAN['Description'].isin([str(job_types_list[i])])]['Time period'],
        y = INIT_FILINGS_TIME_MANHATTAN.loc[INIT_FILINGS_TIME_MANHATTAN['Description'].isin([str(job_types_list[i])])]['Avg Processing Time'],
        name = str(job_types_list[i]),
        mode = 'lines+markers')

    trace_staten[i] = go.Scatter(
        x = INIT_FILINGS_TIME_STATEN.loc[INIT_FILINGS_TIME_STATEN['Description'].isin([str(job_types_list[i])])]['Time period'],
        y = INIT_FILINGS_TIME_STATEN.loc[INIT_FILINGS_TIME_STATEN['Description'].isin([str(job_types_list[i])])]['Avg Processing Time'],
        name = str(job_types_list[i]),
        mode = 'lines+markers')
    
    trace_brooklyn[i] = go.Scatter(
        x = INIT_FILINGS_TIME_BROOKLYN.loc[INIT_FILINGS_TIME_BROOKLYN['Description'].isin([str(job_types_list[i])])]['Time period'],
        y = INIT_FILINGS_TIME_BROOKLYN.loc[INIT_FILINGS_TIME_BROOKLYN['Description'].isin([str(job_types_list[i])])]['Avg Processing Time'],
        name = str(job_types_list[i]),
        mode = 'lines+markers')
    
    trace_queens[i] = go.Scatter(
        x = INIT_FILINGS_TIME_QUEENS.loc[INIT_FILINGS_TIME_QUEENS['Description'].isin([str(job_types_list[i])])]['Time period'],
        y = INIT_FILINGS_TIME_QUEENS.loc[INIT_FILINGS_TIME_QUEENS['Description'].isin([str(job_types_list[i])])]['Avg Processing Time'],
        name = str(job_types_list[i]),
        mode = 'lines+markers')

    
BOROUGHS_LIST = INIT_FILINGS_TIME.BOROUGH.unique()
    
data_bronx = [trace_bronx[0], trace_bronx[1], trace_bronx[2], trace_bronx[3]]
data_man = [trace_man[0], trace_man[1], trace_man[2], trace_man[3]]
data_staten = [trace_staten[0], trace_staten[1], trace_staten[2], trace_staten[3]]
data_queens = [trace_queens[0], trace_queens[1], trace_queens[2], trace_queens[3]]
data_brooklyn = [trace_brooklyn[0], trace_brooklyn[1], trace_brooklyn[2], trace_brooklyn[3]]

for j in range(len(BOROUGHS_LIST)):

    layout[BOROUGHS_LIST[j]] = go.Layout(
        title = BOROUGHS_LIST[j],
        xaxis = dict(title="Time period"),
        yaxis = dict(title="Average processing time in days"))

fig_bronx = go.Figure(data = data_bronx, layout = layout['BRONX'])
fig_man = go.Figure(data = data_man, layout = layout['MANHATTAN'])
fig_staten = go.Figure(data = data_staten, layout = layout['STATEN ISLAND'])
fig_queens = go.Figure(data = data_queens, layout = layout['QUEENS'])
fig_brooklyn = go.Figure(data = data_brooklyn, layout = layout['BROOKLYN'])

iplot(fig_bronx, filename = 'basic-line')
iplot(fig_man, filename = 'basic-line')
iplot(fig_staten, filename = 'basic-line')
iplot(fig_queens, filename = 'basic-line')
iplot(fig_brooklyn, filename = 'basic-line')

# Plotting number of issued permits per category

trace_bronx = defaultdict(list)
trace_man = defaultdict(list)
trace_staten = defaultdict(list)
trace_brooklyn = defaultdict(list)
trace_queens = defaultdict(list)

layout = defaultdict(list)

for i in range(len(job_types_list)):
    
    trace_bronx[i] = go.Scatter(
        x = INIT_FILINGS_TIME_BRONX.loc[INIT_FILINGS_TIME_BRONX['Description'].isin([str(job_types_list[i])])]['Time period'],
        y = INIT_FILINGS_TIME_BRONX.loc[INIT_FILINGS_TIME_BRONX['Description'].isin([str(job_types_list[i])])]['Number of permits'],
        name = str(job_types_list[i]),
        mode = 'lines+markers')
                                        
    trace_man[i] = go.Scatter(
        x = INIT_FILINGS_TIME_MANHATTAN.loc[INIT_FILINGS_TIME_MANHATTAN['Description'].isin([str(job_types_list[i])])]['Time period'],
        y = INIT_FILINGS_TIME_MANHATTAN.loc[INIT_FILINGS_TIME_MANHATTAN['Description'].isin([str(job_types_list[i])])]['Number of permits'],
        name = str(job_types_list[i]),
        mode = 'lines+markers')

    trace_staten[i] = go.Scatter(
        x = INIT_FILINGS_TIME_STATEN.loc[INIT_FILINGS_TIME_STATEN['Description'].isin([str(job_types_list[i])])]['Time period'],
        y = INIT_FILINGS_TIME_STATEN.loc[INIT_FILINGS_TIME_STATEN['Description'].isin([str(job_types_list[i])])]['Number of permits'],
        name = str(job_types_list[i]),
        mode = 'lines+markers')
    
    trace_brooklyn[i] = go.Scatter(
        x = INIT_FILINGS_TIME_BROOKLYN.loc[INIT_FILINGS_TIME_BROOKLYN['Description'].isin([str(job_types_list[i])])]['Time period'],
        y = INIT_FILINGS_TIME_BROOKLYN.loc[INIT_FILINGS_TIME_BROOKLYN['Description'].isin([str(job_types_list[i])])]['Number of permits'],
        name = str(job_types_list[i]),
        mode = 'lines+markers')
    
    trace_queens[i] = go.Scatter(
        x = INIT_FILINGS_TIME_QUEENS.loc[INIT_FILINGS_TIME_QUEENS['Description'].isin([str(job_types_list[i])])]['Time period'],
        y = INIT_FILINGS_TIME_QUEENS.loc[INIT_FILINGS_TIME_QUEENS['Description'].isin([str(job_types_list[i])])]['Number of permits'],
        name = str(job_types_list[i]),
        mode = 'lines+markers')

    
BOROUGHS_LIST = INIT_FILINGS_TIME.BOROUGH.unique()
    
data_bronx = [trace_bronx[0], trace_bronx[1], trace_bronx[2], trace_bronx[3]]
data_man = [trace_man[0], trace_man[1], trace_man[2], trace_man[3]]
data_staten = [trace_staten[0], trace_staten[1], trace_staten[2], trace_staten[3]]
data_queens = [trace_queens[0], trace_queens[1], trace_queens[2], trace_queens[3]]
data_brooklyn = [trace_brooklyn[0], trace_brooklyn[1], trace_brooklyn[2], trace_brooklyn[3]]

for j in range(len(BOROUGHS_LIST)):

    layout[BOROUGHS_LIST[j]] = go.Layout(
        title = BOROUGHS_LIST[j],
        xaxis = dict(title="Time period"),
        yaxis = dict(title="Total number of permits issued"))

fig_bronx = go.Figure(data = data_bronx, layout = layout['BRONX'])
fig_man = go.Figure(data = data_man, layout = layout['MANHATTAN'])
fig_staten = go.Figure(data = data_staten, layout = layout['STATEN ISLAND'])
fig_queens = go.Figure(data = data_queens, layout = layout['QUEENS'])
fig_brooklyn = go.Figure(data = data_brooklyn, layout = layout['BROOKLYN'])

iplot(fig_bronx, filename = 'basic-line')
iplot(fig_man, filename = 'basic-line')
iplot(fig_staten, filename = 'basic-line')
iplot(fig_queens, filename = 'basic-line')
iplot(fig_brooklyn, filename = 'basic-line')

