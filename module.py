"""
Name: Nidhi Jitendra Patni
Date: 17-July-2023
Course Number: ITMD 513
Final Project: Chicago Crime Analysis
"""

# Importing necessary libraries
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from tabulate import tabulate

# creating dynamic URL using a function
def createURL(Chart, Column_Name, Year, Start_Date, End_Date, Source_Location_Latitude, Source_Location_Longitude,
              Destination_Location_Latitude, Destination_Location_Longitude):
  Chart = str(Chart)
  Column_Name = str(Column_Name)
  Year = str(Year)
  Start_Date = str(Start_Date)
  End_Date = str(End_Date)
  Source_Location_Latitude = str(Source_Location_Latitude)
  Source_Location_Longitude = str(Source_Location_Longitude)
  Destination_Location_Latitude = str(Destination_Location_Latitude)
  Destination_Location_Longitude = str(Destination_Location_Longitude)
  if Year == "2021":
   baseurl = "https://data.cityofchicago.org/resource/dwme-t96c.json"
  elif Year == "2022":
   baseurl = "https://data.cityofchicago.org/resource/9hwr-2zxp.json"
  else:
   baseurl = "https://data.cityofchicago.org/resource/xguy-4ndq.json"
  date = "?$where=date between '" + Start_Date + "' and '" + End_Date + "'"
  boxurllocation = 'within_box(location, ' + Source_Location_Latitude + ',' + Source_Location_Longitude + ',' + Destination_Location_Latitude + ',' + Destination_Location_Longitude + ')'
  ourl = baseurl + date + ' AND ' + boxurllocation
  text = requests.get(ourl).json()
  df = pd.DataFrame(
  text, columns=['year', 'date', 'block', 'location_description', 'latitude', 'longitude',
                 'arrest', 'primary_type', 'description'])
  df['Date_Simple'] = pd.to_datetime(df['date']).dt.strftime('%m/%d/%Y')
  df['Month'] = pd.to_datetime(df['date']).dt.month_name()
  df['Day'] = pd.to_datetime(df['date']).dt.day_name()
  df = df.dropna()
  df = df.sort_values('date')

  df['latitude'] = df['latitude'].astype(float)
  df['longitude'] = df['longitude'].astype(float)

  if Chart=='barChart':
      return str(createBarChart(df, Column_Name))
  elif Chart=='sideBySideBarChart':
      return str(createSideBySideBarPlot(df, Column_Name, 'arrest'))
  elif Chart=='lineChart':
      return str(createDynamicLineChart(df, Column_Name))
  elif Chart=='scatterPlot':
      return str(createDynamicScatterPlot(df, 'latitude', 'longitude', Column_Name))
  elif Chart=='pieChart':
      return str(createDynamicPieChart(df, Column_Name))
  elif Chart=='heatMap':
      return str(createHeatMap(df))
  elif Chart=='statistics':
      return str(calculateStatistics(df, Column_Name))
  else:
      return 'Type not supported'

# creating dynamic bar chart
def createBarChart(data, x_col):
 plt.figure(figsize=(12, 8))
 count_data = data[x_col].value_counts().reset_index()
 count_data.columns = [x_col, 'Count']
 plt.bar(count_data[x_col], count_data['Count'], label='Count')
 for i, count in enumerate(count_data['Count']):
  plt.text(i, count, str(count), ha='center', va='bottom')
 plt.xticks(rotation=90)
 plt.yticks(range(0, int(max(count_data['Count'])) + 1, 5))
 plt.xlabel(x_col)
 plt.ylabel('Number of incidents')
 plt.title(f'Bar Chart for {x_col} vs Number of incidents')
 plt.legend()
 plt.tight_layout()
 chart_path = 'static/img/chart.png'
 plt.savefig(chart_path)
 return chart_path

# creating dynamic side by side bar plot
def createSideBySideBarPlot(data, x_col, y_col):
  plt.figure(figsize=(12, 8))
  count_data = data.groupby([x_col, y_col]).size().unstack(fill_value=0)
  categories = count_data.index.tolist()
  bar_width = 0.35
  x_pos = np.arange(len(categories))
  count_data = count_data.loc[count_data.sum(axis=1) > 0]
  categories = count_data.index.tolist()
  for i, col in enumerate(count_data.columns):
   plt.bar(x_pos + i * bar_width, count_data[col], width=bar_width, align='center', label=col)
   for j, count in enumerate(count_data[col]):
    if count > 0:
     plt.text(x_pos[j] + i * bar_width, count + 0.5, str(count), ha='center', va='bottom')
  plt.xlabel(x_col)
  plt.ylabel('Count')
  plt.title(f'Side by Side Bar Plot for {x_col} and Arrest vs Number of incidents')
  plt.xticks(x_pos + (bar_width * (len(count_data.columns) - 1)) / 2, categories, rotation=90)
  plt.legend()
  plt.tight_layout()
  chart_path = 'static/img/chart.png'
  plt.savefig(chart_path)
  return chart_path

# creating dynamic line chart
def createDynamicLineChart(data, x_col):
 plt.figure(figsize=(12, 8))
 count_data = data[x_col].value_counts().reset_index()
 count_data.columns = [x_col, 'Count']
 x = count_data[x_col]
 y = count_data['Count']
 plt.plot(x, y, label='Count')
 for i, count in enumerate(count_data['Count']):
  plt.text(i, count, str(count), ha='center', va='bottom')
 plt.xticks(rotation=90)
 plt.xlabel(x_col)
 plt.ylabel('Count')
 plt.title(f'Line Chart for {x_col} vs Number of Incidents')
 plt.legend()
 plt.tight_layout()
 chart_path = 'static/img/chart.png'
 plt.savefig(chart_path)
 return chart_path

# creating dynamic scatter plot
def createDynamicScatterPlot(data, x_col, y_col, category):
 plt.figure(figsize=(12, 8))
 if x_col == 'latitude' or y_col == 'latitude' or y_col == 'longitude' or y_col == 'longitude':
  numerical = pd.DataFrame()
  numerical[x_col] = data[x_col].astype(float)
  numerical[y_col] = data[y_col].astype(float)
  category = category
  sns.scatterplot(data=data, x=numerical[x_col], y=numerical[y_col])
  sns.scatterplot(data=data, x=numerical[x_col], y=numerical[y_col], hue=category, palette='Set1', s=100)
  plt.xticks(rotation=90)
  plt.xlabel(x_col)
  plt.ylabel(y_col)
  plt.legend(bbox_to_anchor=(1.1, 1))
  plt.title(f'Scatter Plot for {y_col} vs {x_col} categorized against {category}')
  plt.tight_layout()
  chart_path = 'static/img/chart.png'
  plt.savefig(chart_path)
  return chart_path

# creating dynamic pie chart
def createDynamicPieChart(data, labels):
 primaryVisualizeDF = data.groupby(labels).size()
 categories = primaryVisualizeDF.index.tolist()
 plt.figure(figsize=(12, 8))
 pie = plt.pie(primaryVisualizeDF, autopct='%1.1f%%', pctdistance=0.85, labeldistance=1.1, labels=categories)
 for text in pie[2]:
  text.set_size('small')
 plt.xlabel(labels, fontsize=10, color='red')
 plt.legend(bbox_to_anchor=(1.1, 1))
 plt.title(f'Pie Chart for {labels} vs Number of Incidents happened')
 plt.tight_layout()
 chart_path = 'static/img/chart.png'
 plt.savefig(chart_path)
 return chart_path

# creating dynamic heat map
def createHeatMap(data1):
 data = data1.copy()
 labelEncoder = LabelEncoder()
 primaryEncoded = labelEncoder.fit_transform(data['primary_type'])
 primaryEncoded
 data['primary_type'] = primaryEncoded
 labelEncoder2 = LabelEncoder()
 locDiscEncoded = labelEncoder2.fit_transform(data['location_description'])
 locDiscEncoded
 data['location_description'] = locDiscEncoded
 labelEncoder3 = LabelEncoder()
 blockEncoded = labelEncoder2.fit_transform(data['block'])
 blockEncoded
 data['block'] = locDiscEncoded
 labelEncoder4 = LabelEncoder()
 monthEncoded = labelEncoder4.fit_transform(data['Month'])
 monthEncoded
 data['Month'] = monthEncoded
 labelEncoder5 = LabelEncoder()
 arrestEncoded = labelEncoder5.fit_transform(data['arrest'])
 arrestEncoded
 data['arrest'] = arrestEncoded
 labelEncoder6 = LabelEncoder()
 DiscEncoded = labelEncoder6.fit_transform(data['description'])
 DiscEncoded
 data['description'] = DiscEncoded
 labelEncoder7 = LabelEncoder()
 dayEncoded = labelEncoder7.fit_transform(data['Day'])
 dayEncoded
 data['Day'] = dayEncoded
 data.drop('date', axis=1, inplace=False)
 corelation = data.corr()
 corelation
 plt.figure(figsize=(12, 8))
 sns.heatmap(corelation, annot=True, cmap='YlOrRd', fmt='.1f')
 plt.tight_layout()
 chart_path = 'static/img/chart.png'
 plt.savefig(chart_path)
 return chart_path

# creating function for statistics
def calculateStatistics(data, col):
    if col == 'latitude' or col == 'longitude':
        numerical = pd.DataFrame()
        numerical[col] = data[col].astype(float)
        numerical_prop = numerical[col].agg(['mean', 'std', 'var', 'count', 'sum'])
        statistics_list = numerical_prop.reset_index().values.tolist()
        table = tabulate(statistics_list, headers=["Statistics", col], tablefmt="grid")
        image_path = "static/img/chart.png"
        text_to_print = "\n"+ col + " Statistics:" + "\n\n" + str(table)
        print_to_image(text_to_print, image_path)
        return image_path
    else:
        categorical_var = data[col]
        category_counts = categorical_var.value_counts()
        statistics_list = category_counts.reset_index().values.tolist()
        table = tabulate(statistics_list, headers=["Statistics", col], tablefmt="grid")
        category_proportions = categorical_var.value_counts(normalize=True) * 100
        statistics_list1 = category_proportions.reset_index().values.tolist()
        table1 = tabulate(statistics_list1, headers=["Statistics", col], tablefmt="grid")
        image_path = "static/img/chart.png"
        text_to_print = "\n"+ col + " Counts:" + "\n" + str(table) + "\n\n" + col + " Proportions:" + "\n" + str(table1)
        print_to_image(text_to_print, image_path)
        return image_path

# function to convert text to image
def print_to_image(text, image_path):
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, text, fontsize=12, ha='center', va='center')
    ax.axis('off')
    plt.savefig(image_path, bbox_inches='tight', pad_inches=0)

