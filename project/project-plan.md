# Project Plan

## Title

<!-- Give your project a short title. -->

The impact of air pollution on cancer (and maybe other diseases) in the U.S.

## Main Question

How does air pollution (measured by the AQI) in the five most populous states in the US correlate with the incidence of cancer?

<!-- Think about one main question you want to answer based on the data. -->

## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->

Air pollution is an important problem, because it affects countries all over the world and impacts many people. This project analyzes wether there is a correlation between air pollution and cancer (and maybe more diseases) in the five biggest states in the U.S. The results can give insights into how air pollution might influence the health of people. The air pollution can be measured with the AQI (Air Quality Index) and the cancer incidence can be measured with the crude rate (per 100,000 people). This project will analyze the data from the years 2012 to 2021. The data will be cleaned, transformed (averaged, etc.), visualized and analyzed to find correlations. The results will be presented in a report.

## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource 1: Annual Summary Data of AQI by County (of the US)

- each year has a separate file
- all links to the files are available on this link:
  - URL: https://aqs.epa.gov/aqsweb/airdata/download_files.html
- the links have following structure:
  - https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_[year].zip
  - where year is in the range from 2012 to 2021
- Data Type: Zip, wich includes one CSV file

This data source contains information about air pollution in different areas in the U.S. It shows the information about the AQI (Air Quality Index) for the year for each county of each state of the US. It is available under the [U.S. Public Domain license](https://edg.epa.gov/epa_data_license.html), which is described [here](http://www.usa.gov/publicdomain/label/1.0/).

### Datasource 2: Incidence of Cancer by States in the U.S. per year

- Data URL: https://wonder.cdc.gov/controller/datarequest/D198
- the data can be downloaded by making a post request to the data url and sending the following file as payload:
  - [payload](./US-cancer-statistics-request.xml)
  - the payload makes sure, that the data use restrictions are accepted and that only the five most populous states are selected and grouped by year
  - all years, ages, ethnicities, races, sexes and cancer sites are selected
- Data Type: XML

This data source contains information about count and crude rate of cancer in the U.S. states. It is available with [specific restrictions](https://wonder.cdc.gov/datause.html).

## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Look for more open data sources that might be more recent [#1][i1]
2. Look at the data for more insights [#2][i2]
3. Clean the data out off missing, possibly wrong or unneeded values [#3][i3]
4. Write a data report [#7][i7]
5. Create graphs to visualize the data [#4][i4]
6. Analyze the (visualized) data to find correlations [#5][i5]
7. Write the report and draw conclusions [#6][i6]

[i1]: https://github.com/ninchen23/made-template/issues/1
[i2]: https://github.com/ninchen23/made-template/issues/2
[i3]: https://github.com/ninchen23/made-template/issues/3
[i4]: https://github.com/ninchen23/made-template/issues/4
[i5]: https://github.com/ninchen23/made-template/issues/5
[i6]: https://github.com/ninchen23/made-template/issues/6
[i7]: https://github.com/ninchen23/made-template/issues/7
