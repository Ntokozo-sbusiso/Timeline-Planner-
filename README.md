Timeline Planner – Standard Operating
Procedure (SOP) / User Guide

1. Purpose
   
The Timeline Planner is a tool designed to generate a detailed bootcamp or curriculum
timeline from a CSV file. It calculates module start and end dates while automatically
skipping weekends, South African public holidays, and a defined December shutdown
period.
This document explains how to prepare input files, upload them, and interpret the output
results.

2. Input Requirements

2.1 Modules CSV File

Your CSV must include the following columns:
    Column Header Data Type / Notes
    Program Start Date YYYY-MM-DD (e.g., 2026-02-02). Only
    needs a value in the first row.
    Dec Shutdown Start YYYY-MM-DD (e.g., 2026-12-18). The last
    workday is the day before this date.
    Dec Shutdown End YYYY-MM-DD (e.g., 2027-01-04). The first
    workday of the new year is this date.
    Block/Module Name The name of the curriculum item (e.g.,
    Module 1 - Onboarding)
    Duration The length of the module (number of units).
    Unit Must be either days (5-day work week) or
    weeks (5 working days per week).
    
2.2 Optional Holidays CSV

● Include a single column named date.
● Dates should be in YYYY-MM-DD format.
● These holidays will also be skipped in the timeline calculation.
4. Using the Timeline Planner

3.1 Access the Tool

1. Open the web application (e.g., http://localhost:5000 for local Flask
deployment).
2. On the home page, select the Modules CSV file to upload.
3. (Optional) Select a Holidays CSV file.
4. Enter the Start Date if not already in the CSV.
5. Click Submit to generate the timeline.
3.2 Understanding the Output
   
The output is displayed as a table on the results page and can also be downloaded as
timeline_output.csv.

Column Description
Module The name of the curriculum block/module.
Start Date Calculated start date of the module (skipping weekends, holidays,
shutdown).
End Date Calculated end date of the module.
Duration
(days)
Total number of working days calculated for the module.
Unit Original time unit provided in the CSV (days or weeks).

3.3 Downloading Results

● Download or find our example CSV to get started, click Download CSV to save a copy of
the CSV file example.
● Open the CSV in Excel, Google Sheets, or any other spreadsheet program for further
analysis or reporting.

4. Error Handling
● Ensure the CSV column headers match exactly as specified.
● Check that dates are in the YYYY-MM-DD format.
● If no data appears, confirm that the CSV is not empty and the start date is valid.

6. Tips for Best Results
   
● Keep module durations realistic and consistent with the bootcamp schedule.
● Use the optional holidays file to account for local events or organizational off-days.
● Verify output dates against known holidays and shutdown periods for accuracy.
