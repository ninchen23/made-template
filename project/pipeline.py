from typing import Literal
import pandas as pd
import requests
from zipfile import ZipFile
from io import BytesIO
import xml.etree.ElementTree as ET
from retry import retry



@retry(tries=3, delay=2)
def download_zip_with_csv(url: str) -> pd.DataFrame:
    try:
        response = requests.get(url)
        if 200 <= response.status_code < 300:
            print("Download of zip successful")
            file = response.content
            with ZipFile(BytesIO(file)) as zip:
                files = zip.namelist()
                with zip.open(files[0]) as file:
                    df = pd.read_csv(file)
                    return df
        else:
            raise Exception(f"Download of zip failed with status code {response.status_code}: {response.text}")
    except Exception as e:
        raise Exception(f"Error: {e}")

@retry(tries=3, delay=2)
def download_cancer_rates_xml() -> str:
    url = "https://wonder.cdc.gov/controller/datarequest/D198"
    try:
        with open("US-cancer-statistics-request.xml", "r") as request_param:
            xml_content = request_param.read()
        payload = {
            'request_xml': xml_content,
            'accept_datause_restrictions': True
        }
        # import pdb; pdb.set_trace()

        response = requests.post(url, data=payload)

        if 200 <= response.status_code < 300:
            print("Download of txt successful")
            xml_response = response.text
            return xml_response
        else:
            raise Exception(f"Download of cancer rates failed with status code {response.status_code}: {response.text}")
    except Exception as e:
        raise Exception(f"Error: {e}")
    

def aggregate_aqi_data(df: pd.DataFrame) -> pd.DataFrame:
    try:
        # only keep rows where county is one of the 5 most populous states
        df = df[df['State'].isin(['California', 'Texas', 'Florida', 'New York', 'Pennsylvania'])].copy()

        # calculate percentage of days with good/moderate/... days
        df['good_days_percentage'] = df['Good Days'] / df['Days with AQI'] * 100
        df['moderate_days_percentage'] = df['Moderate Days'] / df['Days with AQI'] * 100
        df['unhealthy_sensitive_days_percentage'] = df['Unhealthy for Sensitive Groups Days'] / df['Days with AQI'] * 100
        df['unhealthy_days_percentage'] = df['Unhealthy Days'] / df['Days with AQI'] * 100
        df['very_unhealthy_days_percentage'] = df['Very Unhealthy Days'] / df['Days with AQI'] * 100
        df['hazardous_days_percentage'] = df['Hazardous Days'] / df['Days with AQI'] * 100

        # save per state (with mean computed)
        summary = df.groupby('State').agg({
            'good_days_percentage': 'mean',
            'moderate_days_percentage': 'mean',
            'unhealthy_sensitive_days_percentage': 'mean',
            'unhealthy_days_percentage': 'mean',
            'very_unhealthy_days_percentage': 'mean',
            'hazardous_days_percentage': 'mean',
            'Max AQI': ['max', 'median'],
            'Year': 'min' # doesn't matter, always the same
        }).reset_index()

        # print(summary)
        # import pdb; pdb.set_trace()
        print("aggregation of aqi data successful")
        return summary
    except Exception as e:
        raise Exception (f"Error while aggregating AQI data: {e}")

def process_cancer_rates_xml(xml: str) -> pd.DataFrame:
    try:
        root = ET.fromstring(xml)
        data_table = root.find(".//data-table")

        # process header
        # header = text.strip().split("\n")[0]
        # needed_indices = []
        # for i, column in enumerate(header.split("\t")):
        #     if column in ["States", "Year", "Count", "Population", "Crude Rate"]:
        #         needed_indices.append(i)

        # process data
        data = []
        # for line in text.strip().split("\n")[1:]:
        #     print(line)
        #     row = line.split("\t")
        #     if row[0] == "Total":
        #         continue
        #     elif row[3] not in ["2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021"]:
        #         continue
        #     elif row[0] == "---":
        #         break
            
        #     # only keep needed columns
        #     modified_row = []
        #     for i, value in enumerate(row):
        #         if i in needed_indices:
        #             modified_row.append(value)
        #     data.append(modified_row)

        for row in data_table.findall("r"): # r is a row
            row_data = {}
            cells = row.findall("c")

            if cells[1].attrib.get('l', None) is None:
                if cells[1].attrib.get('c', None) == "1":
                    continue # year is 1 if the row shows the total for all years
                elif cells[0].attrib.get('c', None) == "2":
                    continue # skip the row with the total for all
            else:
                row_data['State'] = cells[0].attrib.get('l', None)
                row_data['Year'] = int(cells[1].attrib.get('l', None))
                row_data['Count'] = float(cells[2].attrib['v'].replace(",", ""))
                row_data['Population'] = float(cells[3].attrib['v'].replace(",", ""))
                row_data['Crude Rate'] = float(cells[4].attrib['v'].replace(",", ""))

                data.append(row_data)

        # import pdb; pdb.set_trace()
        df = pd.DataFrame(data, columns=["State", "Year", "Count", "Population", "Crude Rate"])

        print("Successfully processed cancer rates XML")
        return df
    except ET.ParseError as e:
        raise Exception(f"Error with ElementTree while processing cancer rates XML: {e}")
    except Exception as e:
        raise Exception (f"Error while processing cancer rates XML: {e}")

def transform_cancer_rates(df: pd.DataFrame) -> pd.DataFrame:
    try:
        # only keep rows where year is between 2012 and 2021
        df2 = df[df['Year'] >= 2006]
        df2 = df2[df2['Year'] <= 2021]

        # only keep the crude rate (how many people per 100,000)
        df2 = df2.drop(columns=['Count', 'Population'])

        # import pdb; pdb.set_trace()
        print("Successfully transformed cancer rates")
        return df2
    except Exception as e:
        raise Exception(f"Error while transforming cancer rates: {e}")


def save_to_sqlite_database(df: pd.DataFrame, table_name: str, db_url: str='sqlite:///../data/data.sqlite', if_exists: Literal['replace', 'append']='append') -> None:
    try:
        df.to_sql(table_name, db_url, if_exists=if_exists, index=False)
        print("Data saved to sqlite successfully.")
    except Exception as e:
        raise Exception(f"Error while saving data to sqlite: {e}\n Data pipeline is stopped now.")



### download and transform the data for air pollution
air_pollution_urls = [
    "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2021.zip",
    "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2020.zip",
    "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2019.zip",
    "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2018.zip",
    "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2017.zip",
    "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2016.zip",
    "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2015.zip",
    "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2014.zip",
    "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2013.zip",
    "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2012.zip",
    "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2011.zip",
    "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2010.zip",
    "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2009.zip",
    "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2008.zip",
    "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2007.zip",
    "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2006.zip"
]

first = True
counter_of_failed_processings = 0
for url in air_pollution_urls:
    try:
        df = download_zip_with_csv(url)
        df = aggregate_aqi_data(df)
        if first:
            first = False
            save_to_sqlite_database(df, 'aqi', if_exists='replace')
        else:
            save_to_sqlite_database(df, 'aqi')#'aqi_' + url[-8:-4])
    except Exception as e:
        print(f"Failed to download, process or save AQI data with url {url}: {e}")
        counter_of_failed_processings += 1
        if counter_of_failed_processings >= (len(air_pollution_urls) - 10):
            raise Exception("Too many failed downloads or processings of AQI datasets. Data pipeline is stopped now.")



### download and transform the data for cancer rates
try:
    xml_data = download_cancer_rates_xml()
    df = process_cancer_rates_xml(xml_data)
    df = transform_cancer_rates(df)
    save_to_sqlite_database(df, 'cancer_rates', if_exists='replace')
except Exception as e:
    raise Exception(f"Failed to download, process or save cancer rates data with error: {e}. Data pipeline is stopped now.")