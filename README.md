# Vancouver Crime Dashboard
Link to the dashboard: [Vancouver Crime Dashboard](https://crime-dash.onrender.com)

## Motivation
The crime rate in a community is an important factor that citizens consider when making decisions about whether to live or invest. A high crime rate in a city may impact personal safety, property values, and overall quality of life and is influenced by many factors. Understanding where, how and why crime happens is important for fighting and lowering crime rates, hence increasing safety in communities. Since 1930, the FBI has been collecting data on the types, amounts, and impact of crime in the United States through the Uniform Crime Reporting Program. So, our dashboard will aim to figure out the socioeconomic conditions, socio-demographic and community factors influencing crime rates in different US states as well as provide access to crime data in an understandable and intuitive manner.

## Description of the Dashboard

This interactive visualization and exploration tool will contain an interactive map as a landing page that will show the violent crimes committed in the Continental United States of America by State and County.

The following steps illustrate how the user could interact with the dashboard using the link on top or locally:

- Entering the main page of the dashboard, you can see one interactive map showing all communities and their associated crime rate. At the bottom right you can see a scatter plot showing the correlation between two selected factors.

![Two Plots](media/two_plots.mov)

-   'Download Data' aims to give the user the capability of downloading a table with the data as sliced using the filters available On the left there will be a filter menu to slice the data and show specific insights. On the second tab (which will maintain the filters made on the left-hand panel) it will include a bar chart denoting the communities' composition and another bar chart denoting police composition. Below it will include a line chart showing the crime statistics in a time series (for 1995).

In the left-hand filter menu the user will have the liberty of choosing: State, county, time interval (within 1995), community type (based on income and racial composition), police presence (amount of police officers) and police budget allocated. It will also include cards stating "Percentage of Violent Crimes", 'Overall Country Crime Percentage' and 'Police Presence'

### Installation

You can download this file, create a conda environment and activate it as follows.
```
conda env create -f environment.yaml
conda activate van-crime
```
You can view the source code in `src/app.py`.

### Run locally

Make sure you are in the root directory of the repository. Then, run the following command in Terminal:
```
python src/app.py
```
You will be given an URL to use the dashboard.


### Contributing

Contributors: Cici Du, Melisa Maidana, Paniz Fazlali, Shi Yan Wang (DSCI 532 - Group 16).

Interested in contributing? Check out the contributing guidelines.

We would love to know what other datasets we can bring into our dashboard to make it more useful. Please also feel free to offer suggestions on other interactive options you'd like to see.

Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

### License

This dashboard was created by Cici Du, Melisa Maidana, Paniz Fazlali, Shi Yan Wang (DSCI 532 - Group 16).

It is licensed under the terms of the MIT license.