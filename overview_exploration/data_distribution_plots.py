# Plotting the data distribution

dist_df = pd.DataFrame(Brooklyn_Permit_Issuance_Corp_prediction_dataset['Processing Time'])
dist_df['ID'] = ""
dist_df['ID'] = dist_df.index
dist_df.columns = ['Processing Time']

dist_df_counts = dist_df.groupby(['Processing Time']).count().reset_index()

dist_df_counts.head()

# Complete distribution

trace_data_dist = go.Scatter(
        x = dist_df_counts['Processing Time'],
        y = dist_df_counts['ID'],
        mode = 'lines')

data_dist = [trace_data_dist]

layout = go.Layout(
        title = "Distribution of processing times (complete)",
        xaxis = dict(title="Processing time"),
        yaxis = dict(title="Number of permits"))

fig = go.Figure(data = data_dist, layout = layout)
iplot(fig, filename = 'basic-line')


# 0-50 days

trace_data_dist = go.Scatter(
        x = dist_df_counts.loc[(dist_df_counts['Processing Time'] < 50)]['Processing Time'],
        y = dist_df_counts.loc[(dist_df_counts['Processing Time'] < 50)]['ID'],
        mode = 'lines')

data_dist = [trace_data_dist]

layout = go.Layout(
        title = "Distribution of processing times (0-50 days)",
        xaxis = dict(title="Processing time"),
        yaxis = dict(title="Number of permits"))

fig = go.Figure(data = data_dist, layout = layout)
iplot(fig, filename = 'basic-line')

# 50-700 days

trace_data_dist = go.Scatter(
        x = dist_df_counts.loc[(dist_df_counts['Processing Time'] < 700) & (dist_df_counts['Processing Time'] > 50.0)]['Processing Time'],
        y = dist_df_counts.loc[(dist_df_counts['Processing Time'] < 700) & (dist_df_counts['Processing Time'] > 50.0)]['ID'],
        mode = 'lines')

data_dist = [trace_data_dist]

layout = go.Layout(
        title = "Distribution of processing times(50-700 days)",
        xaxis = dict(title="Processing time"),
        yaxis = dict(title="Number of permits"))

fig = go.Figure(data = data_dist, layout = layout)
iplot(fig, filename = 'basic-line')
