# Aufgabe: unit tests for extract, transform, load
# ein oder zwei system tests für die ganze data pipeline (überprüfen, dass daten korrekt gespeichert sind)

# test isolated pipeline steps (replace by test doubles)
# mock data -> test specific edge cases that may not exists in real data    
#      copy production data or parts of it
# test whole pipeline

# test that database is created
# test that tables exist
# test that correct columns exist
# test that after two times load still data only is there once
# test for null and zero data



# from numpy import NaN
import pipeline
import sqlite3
import os

import pandas as pd
from pandas.testing import assert_frame_equal

### Unit tests for pipeline functions

# mock data is part of the real dataset from 2021
def test_aggregate_aqi_data():
    # arrange
    df = pd.DataFrame({
        # one relevant state, one irrelevant state
        'State': ['California', 'California', 'California', 'Alabama', 'Alabama', 'Alabama'],
        'County': ['Calusa', 'Del Norte', 'Los Angeles', 'Baldwin', 'Clay', 'Elmore'],
        'Year': [2021, 2021, 2021, 2021, 2021, 2021],
        'Days with AQI': [365, 323, 365, 280, 110, 241],
        'Good Days': [111, 259, 9, 248, 87, 238],
        'Moderate Days': [238, 64, 259, 32, 23, 3],	
        'Unhealthy for Sensitive Groups Days': [9, 0, 70, 0, 0, 0],
        'Unhealthy Days': [6, 0, 26, 0, 0, 0],
        'Very Unhealthy Days': [1, 0, 1, 0, 0, 0],
        'Hazardous Days': [0, 0, 0, 0, 0, 0],
        'Max AQI': [225, 72, 281, 63, 70, 87],
        # columns that will be dropped, so the data isn't relevant
        '90th Percentile AQI': [0, 0, 0, 0, 0, 0],
        'Median AQI': [0, 0, 0, 0, 0, 0],
        'Days CO': [0, 0, 0, 0, 0, 0],
        'Days NO2': [0, 0, 0, 0, 0, 0],
        'Days Ozone': [0, 0, 0, 0, 0, 0],
        'Days PM2.5': [0, 0, 0, 0, 0, 0],
        'Days PM10': [0, 0, 0, 0, 0, 0]
    })

    # act
    aggregated_aqi_df = pipeline.aggregate_aqi_data(df)

    # assert
    # test that only California is in the result
    # test that only the relevant columns are in the result
    # test that the data was computed correctly
    expected_df = pd.DataFrame({
        ('State', ''): ['California'],
        ('good_days_percentage', 'mean'): [(111/365 + 259/323 + 9/365) / 3 * 100],
        ('moderate_days_percentage', 'mean'): [(238/365 + 64/323 + 259/365) / 3 * 100],
        ('unhealthy_sensitive_days_percentage', 'mean'): [(9/365 + 0/323 + 70/365) / 3 * 100],
        ('unhealthy_days_percentage', 'mean'): [(6/365 + 0/323 + 26/365) / 3 * 100],
        ('very_unhealthy_days_percentage', 'mean'): [(1/365 + 0/323 + 1/365) / 3 * 100],
        ('hazardous_days_percentage', 'mean'): [0.0],
        ('Max AQI', 'max'): [281],
        ('Max AQI', 'median'): [225.0],
        ('Year', 'min'): [2021]
    })
    assert_frame_equal(aggregated_aqi_df, expected_df)

# mock data is part of the real dataset, most of the metadata is not relevant and therefore not included as it would not change the output
def test_process_cancer_rates_xml():
    # arrange
    xml = """<?xml version="1.0"?>
    <page>
    <platform>prod</platform>
    <title>United States and Puerto Rico Cancer Statistics, 1999-2021 Incidence Results Form</title>
    <data-table show-all-labels="true">
    <r><c l="New York" cd="36" cf="f"/><c l="2019"/><c v="126,512"/><c v="20,221,642"/><c v="625.626741884"/></r>
    <r><c l="New York" cd="36" cf="f"/><c l="2020"/><c v="111,774"/><c v="20,108,296"/><c v="555.860128576"/></r>
    <r><c l="New York" cd="36" cf="f"/><c l="2021"/><c v="125,409"/><c v="19,857,492"/><c v="631.545010820"/></r>
    <r><c l="New York" cd="36" cf="f"/><c c="1"/><c dt="2,590,172"/><c dt="449,858,764"/><c dt="575.774489079"/></r>
    <r><c l="Texas" cd="48" cf="f"/><c l="2019"/><c v="133,219"/><c v="28,855,292"/><c v="461.679611490"/></r>
    <r><c l="Texas" cd="48" cf="f"/><c l="2020"/><c v="124,527"/><c v="29,232,474"/><c v="425.988576950"/></r>
    <r><c l="Texas" cd="48" cf="f"/><c l="2021"/><c v="133,284"/><c v="29,558,864"/><c v="450.910427410"/></r>
    <r><c l="Texas" cd="48" cf="f"/><c c="1"/><c dt="2,457,636"/><c dt="577,857,112"/><c dt="425.301679077"/></r>
    <r><c c="2"/><c dt="13,529,718"/><c dt="2,608,584,682"/><c dt="518.661253106"/></r>
    </data-table>
    </page>
    """

    # act
    cancer_rates_df = pipeline.process_cancer_rates_xml(xml)

    # assert
    # test that only the relevant columns are in the result
    # test that the data was extracted correctly and unnecessary data was dropped
    expected_df = pd.DataFrame({
        'State': ['New York', 'New York', 'New York', 'Texas', 'Texas', 'Texas'],
        'Year': [2019, 2020, 2021, 2019, 2020, 2021],
        'Count': [126512.0, 111774.0, 125409.0, 133219.0, 124527.0, 133284.0],
        'Population': [20221642.0, 20108296.0, 19857492.0, 28855292.0, 29232474.0, 29558864.0],
        'Crude Rate': [625.626741884, 555.860128576, 631.545010820, 461.679611490, 425.988576950, 450.910427410]
    })
    assert_frame_equal(cancer_rates_df, expected_df)

# mock data is the expected data after processing (see expected_df in test_process_cancer_rates_xml)
# plus some additional data (to test that it is dropped)
def test_transform_cancer_rates():
    # arrange
    cancer_rates_df = pd.DataFrame({
        'State': ['New York', 'New York', 'New York', 'New York', 'Texas', 'Texas', 'Texas', 'Texas'],
        'Year': [2019, 2020, 2021, 2022, 2005, 2019, 2020, 2021],
        'Count': [126512.0, 111774.0, 125409.0, 100000.0, 100000.0, 133219.0, 124527.0, 133284.0],
        'Population': [20221642.0, 20108296.0, 19857492.0, 20000000.0, 20000000.0, 28855292.0, 29232474.0, 29558864.0],
        'Crude Rate': [625.626741884, 555.860128576, 631.545010820, 500.0, 500.0, 461.679611490, 425.988576950, 450.910427410]
    })

    # act
    transformed_cancer_rates_df = pipeline.transform_cancer_rates(cancer_rates_df)

    # assert
    expected_df = pd.DataFrame({
        'State': ['New York', 'New York', 'New York', 'Texas', 'Texas', 'Texas'],
        'Year': [2019, 2020, 2021, 2019, 2020, 2021],
        'Crude Rate': [625.626741884, 555.860128576, 631.545010820, 461.679611490, 425.988576950, 450.910427410]
    })
    assert_frame_equal(transformed_cancer_rates_df, expected_df)

# mock data is the expected data after processing (see expected_df in test_transform_cancer_rates and in test_aggregate_aqi_data)
def test_save_to_sqlite_database():
    # arrange
    cancer_rates_df = pd.DataFrame({
        'State': ['New York', 'New York', 'New York', 'Texas', 'Texas', 'Texas'],
        'Year': [2019, 2020, 2021, 2019, 2020, 2021],
        'Crude Rate': [625.626741884, 555.860128576, 631.545010820, 461.679611490, 425.988576950, 450.910427410]
    })
    aqi_df = pd.DataFrame({
        ('State', ''): ['California'],
        ('good_days_percentage', 'mean'): [(111/365 + 259/323 + 9/365) / 3 * 100],
        ('moderate_days_percentage', 'mean'): [(238/365 + 64/323 + 259/365) / 3 * 100],
        ('unhealthy_sensitive_days_percentage', 'mean'): [(9/365 + 0/323 + 70/365) / 3 * 100],
        ('unhealthy_days_percentage', 'mean'): [(6/365 + 0/323 + 26/365) / 3 * 100],
        ('very_unhealthy_days_percentage', 'mean'): [(1/365 + 0/323 + 1/365) / 3 * 100],
        ('hazardous_days_percentage', 'mean'): [0.0],
        ('Max AQI', 'max'): [281],
        ('Max AQI', 'median'): [225.0],
        ('Year', 'min'): [2021]
    })

    try:
        # act
        pipeline.save_to_sqlite_database(cancer_rates_df, 'cancer_rates', 'sqlite:///test.sqlite')
        pipeline.save_to_sqlite_database(aqi_df, 'aqi', 'sqlite:///test.sqlite')

        # assert
        connection = sqlite3.connect('test.sqlite')
        cursor = connection.cursor()
        # test for cancer_rates table
        # test that table exists and has the correct columns and contains the correct data
        cursor.execute("SELECT * FROM cancer_rates")
        result = cursor.fetchall()
        expected_result = [('New York', 2019, 625.626741884), ('New York', 2020, 555.860128576), ('New York', 2021, 631.54501082), ('Texas', 2019, 461.67961149), ('Texas', 2020, 425.98857695), ('Texas', 2021, 450.91042741)]
        assert result == expected_result

        # test for aqi table
        # test that table exists and has the correct columns and contains the correct data
        cursor.execute("SELECT * FROM aqi")
        result = cursor.fetchall()
        expected_result = [('California', (111/365 + 259/323 + 9/365) / 3 * 100, (238/365 + 64/323 + 259/365) / 3 * 100, (9/365 + 0/323 + 70/365) / 3 * 100, (6/365 + 0/323 + 26/365) / 3 * 100, (1/365 + 0/323 + 1/365) / 3 * 100, 0.0, 281, 225.0, 2021)]
        assert result == expected_result

    finally:
        connection.close()
        # cleanup
        os.remove('test.sqlite')


### System tests for the whole pipeline

def test_pipeline_with_mock_data():
    # arrange
    aqi_df = pd.DataFrame({
        # one relevant state, one irrelevant state
        'State': ['California', 'California', 'California', 'Alabama', 'Alabama', 'Alabama'],
        'County': ['Calusa', 'Del Norte', 'Los Angeles', 'Baldwin', 'Clay', 'Elmore'],
        'Year': [2021, 2021, 2021, 2021, 2021, 2021],
        'Days with AQI': [365, 323, 365, 280, 110, 241],
        'Good Days': [111, 259, 9, 248, 87, 238],
        'Moderate Days': [238, 64, 259, 32, 23, 3],	
        'Unhealthy for Sensitive Groups Days': [9, 0, 70, 0, 0, 0],
        'Unhealthy Days': [6, 0, 26, 0, 0, 0],
        'Very Unhealthy Days': [1, 0, 1, 0, 0, 0],
        'Hazardous Days': [0, 0, 0, 0, 0, 0],
        'Max AQI': [225, 72, 281, 63, 70, 87],
        # columns that will be dropped, so the data isn't relevant
        '90th Percentile AQI': [0, 0, 0, 0, 0, 0],
        'Median AQI': [0, 0, 0, 0, 0, 0],
        'Days CO': [0, 0, 0, 0, 0, 0],
        'Days NO2': [0, 0, 0, 0, 0, 0],
        'Days Ozone': [0, 0, 0, 0, 0, 0],
        'Days PM2.5': [0, 0, 0, 0, 0, 0],
        'Days PM10': [0, 0, 0, 0, 0, 0]
    })
    
    xml = """<?xml version="1.0"?>
    <page>
    <platform>prod</platform>
    <title>United States and Puerto Rico Cancer Statistics, 1999-2021 Incidence Results Form</title>
    <data-table show-all-labels="true">
    <r><c l="New York" cd="36" cf="f"/><c l="2019"/><c v="126,512"/><c v="20,221,642"/><c v="625.626741884"/></r>
    <r><c l="New York" cd="36" cf="f"/><c l="2020"/><c v="111,774"/><c v="20,108,296"/><c v="555.860128576"/></r>
    <r><c l="New York" cd="36" cf="f"/><c l="2021"/><c v="125,409"/><c v="19,857,492"/><c v="631.545010820"/></r>
    <r><c l="New York" cd="36" cf="f"/><c c="1"/><c dt="2,590,172"/><c dt="449,858,764"/><c dt="575.774489079"/></r>
    <r><c l="Texas" cd="48" cf="f"/><c l="2019"/><c v="133,219"/><c v="28,855,292"/><c v="461.679611490"/></r>
    <r><c l="Texas" cd="48" cf="f"/><c l="2020"/><c v="124,527"/><c v="29,232,474"/><c v="425.988576950"/></r>
    <r><c l="Texas" cd="48" cf="f"/><c l="2021"/><c v="133,284"/><c v="29,558,864"/><c v="450.910427410"/></r>
    <r><c l="Texas" cd="48" cf="f"/><c c="1"/><c dt="2,457,636"/><c dt="577,857,112"/><c dt="425.301679077"/></r>
    <r><c c="2"/><c dt="13,529,718"/><c dt="2,608,584,682"/><c dt="518.661253106"/></r>
    </data-table>
    </page>
    """

    try:
        # act
        aggregated_aqi_df = pipeline.aggregate_aqi_data(aqi_df)
        cancer_rates_df = pipeline.process_cancer_rates_xml(xml)
        transformed_cancer_rates_df = pipeline.transform_cancer_rates(cancer_rates_df)
        pipeline.save_to_sqlite_database(aggregated_aqi_df, 'aqi', 'sqlite:///test.sqlite')
        pipeline.save_to_sqlite_database(transformed_cancer_rates_df, 'cancer_rates', 'sqlite:///test.sqlite')

        # assert
        connection = sqlite3.connect('test.sqlite')
        cursor = connection.cursor()

        # check cancer_rates table
        cursor.execute("PRAGMA table_info(cancer_rates)")
        columns = [info[1] for info in cursor.fetchall()]
        expected_columns = ['State', 'Year', 'Crude Rate']
        assert columns == expected_columns

        # check aqi table
        cursor.execute("PRAGMA table_info(aqi)")
        columns = [info[1] for info in cursor.fetchall()]
        expected_columns = ["('State', '')", "('good_days_percentage', 'mean')", "('moderate_days_percentage', 'mean')", "('unhealthy_sensitive_days_percentage', 'mean')", "('unhealthy_days_percentage', 'mean')", "('very_unhealthy_days_percentage', 'mean')", "('hazardous_days_percentage', 'mean')", "('Max AQI', 'max')", "('Max AQI', 'median')", "('Year', 'min')"]
        assert columns == expected_columns

        # check number of rows in cancer_rates table
        cursor.execute("SELECT COUNT(*) FROM cancer_rates")
        result = cursor.fetchone()
        assert result[0] == 6

        # check number of rows in aqi table
        cursor.execute("SELECT COUNT(*) FROM aqi")
        result = cursor.fetchone()
        assert result[0] == 1
    finally:
        connection.close()
        # cleanup
        os.remove('test.sqlite')
    
def test_pipeline_with_real_data():
    try:
        os.remove('../data/data.sqlite')
    except FileNotFoundError:
        pass

    # arrange and act
    pipeline.main()

    # assert
    connection = sqlite3.connect('../data/data.sqlite')
    cursor = connection.cursor()

    # check cancer_rates table
    cursor.execute("PRAGMA table_info(cancer_rates)")
    columns = [info[1] for info in cursor.fetchall()]
    expected_columns = ['State', 'Year', 'Crude Rate']
    assert columns == expected_columns

    # check aqi table
    cursor.execute("PRAGMA table_info(aqi)")
    columns = [info[1] for info in cursor.fetchall()]
    expected_columns = ["('State', '')", "('good_days_percentage', 'mean')", "('moderate_days_percentage', 'mean')", "('unhealthy_sensitive_days_percentage', 'mean')", "('unhealthy_days_percentage', 'mean')", "('very_unhealthy_days_percentage', 'mean')", "('hazardous_days_percentage', 'mean')", "('Max AQI', 'max')", "('Max AQI', 'median')", "('Year', 'min')"]
    assert columns == expected_columns

    # check number of rows in cancer_rates table (16 rows for each of the 5 states)
    cursor.execute("SELECT COUNT(*) FROM cancer_rates")
    result = cursor.fetchone()
    assert result[0] == 80

    # check number of rows in aqi table (16 rows for each of the 5 states)
    cursor.execute("SELECT COUNT(*) FROM aqi")
    result = cursor.fetchone()
    assert result[0] == 80

    connection.close()
