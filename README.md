# Individual and Family-Owned Animal Farmers
---
## Overview

This project provides estimates of the number of individuals and family-owned farmers involved in animal agriculture by U.S. state in 2012 and 2017. The data used com from multiple sources: the Economic Research Service of the U.S. Department of Agriculture ([ERS data](https://data.ers.usda.gov/reports.aspx?ID=17832)) the Natural Agricultural Statistics Service of the U.S.D.A. ([NASS data](https://www.nass.usda.gov/Quick_Stats/CDQT/chapter/1/table/1)) and the U.S. Census Bureau Current Population Surveys ([2018 CPS](https://www.census.gov/data/tables/time-series/demo/voting-and-registration/p20-583.html), [2012 CPS](https://www.census.gov/data/tables/2012/demo/voting-and-registration/p20-568.html)). We two estimates of this measure: including and excluding feed commodities.

We made the following proportionality assumptions due to the lack of specific data:
- Ratio of animal agriculture revenue in total agriculture revenue in the state is proportional to that ratio among individual and family farmers.
- Proportion of individual and family farmers that vote is the same as average in the state.
- We count each individual and family farm as ONE person.  If you believe that the right number is N>1, multiply all reported numbers for family farmers by N.

To make the analysis easily digestable, we produce a [dashboard](https://gentle-bastion-68761.herokuapp.com/) to easily interact with the data, and two excel files that contain the animal farmer estimates, that can be used for future analysis.

## Methods

**Note on Equation Rendering**: If the equations in the below section do not load properly on your browser, try opening this repository in Google Chrome, add install the [xhub extension](https://chrome.google.com/webstore/detail/xhub/anidddebgkllnnnnjfkmjcaallemhjee).

### ERS Commodity Data

The Economic Research Service (ERS), which is a subdivision of the USDA, reports annual cash receipts by commodity, for each state ([ERS data](https://data.ers.usda.gov/reports.aspx?ID=17832)).

For each state, we computed the share of animal agriculture by (1) including feed crops and (2) excluding feed crops (both numbers are decimals). The explicit formulas are given below:

```math
\text{Animal Agricultural Share, Excluding Feed Commodities (AAXSF)} = \frac{\text{Animals and Products}}{\text{All Commodities}}
```

```math
\parbox[t]{7cm}{Animal Agricultural Share, \\ Excluding Feed Commodities (AAXSF)} = \frac{\text{Animals and Products}}{\text{All Commodities}}
```

```math
\text{Animal Agricultural Share}, \\ \text{Including Feed Commodities (AASF)} = \frac{\text{Animals and Products + Feed Crops}}{\text{All Commodities}}
```

### NASS Census Data

The National Agricultural Statistice Service (NASS), which is a subdivision of the USDA, provides census data for various farm and crop operations, for each state ([NASS data](https://www.nass.usda.gov/Quick_Stats/CDQT/chapter/1/table/1)).

For each state, we estimate the number of individual and family farmers (IFF) by using the "FARM OPERATIONS, ORGANIZATION, TAX PURPOSES, FAMILY & INDIVIDUAL - NUMBER OF OPERATIONS" field in the NASS data. We then multiply this by our previously computed share values to get an estimate for the number of animal farmers in each state.

```math
\text{Individual and Family Farmers, Excluding Feed Commodities (IFAFXF)} = \text{AAXXF} * \text{IFF}
```

```math
\text{Individual and Family Farmers, Including Feed Commodities (IFAFF)} = \text{AASF} * \text{IFF}
```

The NASS only provides data from 2017 and 2012, so our analysis only estimates the raw number of family farmers by state, without and with feed, respectively, in those years.

### Census Bureau CPS Data

To better understand these farmer estimates in context, we compared them to the total populations and the voting populations in each state. The U.S. Census Bureau, Current Population Survey collects data every two years on population and voting totals. Therefore, for our comparison, we used the 2012 CPS data directly, and we used the 2018 CPS data as a proxy for the 2017 totals, since the NASS only has data from 2017 ([2018 CPS](https://www.census.gov/data/tables/time-series/demo/voting-and-registration/p20-583.html), [2012 CPS](https://www.census.gov/data/tables/2012/demo/voting-and-registration/p20-568.html)).

To compare the farmer estimates to the total population, we compute farmer estimates, normalized by population size, according to the equations below.

```math
\text{Share of Individual and Family Farmers \\ in State Population, Excluding Feed Commodities (IFAFXFSP)} = \frac{\text{IFAFXF}}{\text{Total Population}}
```

```math
\text{Share of Individual and Family Farmers in State Population, Including Feed Commodities (IFAFFSP)} = \frac{\text{IFAFF}}{\text{Total Population}}
```

To compare the farmer estimates to the total number of registered voters, we compute farmer estimates, normalized by registered voters, according to the equation below.

```math
\text{Share of Individual and Family Farmers in State Population, Excluding Feed Commodities (IFAFXFRV)} = \frac{\text{IFAFXF}}{\text{Total Registered Voters}}
```

```math
\text{Share of Individual and Family Farmers in State Population, Including Feed Commodities (IFAFFRV)} = \frac{\text{IFAFF}}{\text{Total Registered Voters}}
```

The aforementioned [dashboard](https://gentle-bastion-68761.herokuapp.com/) provides an interactive way to analyze these metrics. All of the maps above (and more) are viewable on the dashboard.

### Data Summary

The table below summarizes all of the metrics that are viewable on the dashboard (computed and raw), and the abbreviations used to refer to them.

| Metric | Abbreviation | Calculation | Data Source(s) | Notes |
:-------------: | :--: | :----: | :----: | :------: |
| Animal Agricultural Share, Excluding Feed Commodities | AASXF | $`\frac{\text{Animals and Products + Feed Crops}}{\text{All Commodities}}`$ | ERS |  |
| Animal Agricultural Share, Including Feed Commodities | AASF | $`\frac{\text{Animals and Products + Feed Crops}}{\text{All Commodities}}`$ | ERS | |
| Number of Individual and Family Farmers | IFF | "FARM OPERATIONS, ORGANIZATION, TAX PURPOSES, FAMILY & INDIVIDUAL - NUMBER OF OPERATIONS" | NASS | Raw Field in NASS data |
| Individual and Family Farmers, Excluding Feed Commodities | IFAFXF | $`\text{AASXF} * \text{IFF}`$ | ERS, NASS | | 
| Individual and Family Farmers, Including Feed Commodities | IFAFF | $`\text{AASF} * \text{IFF}`$ | ERS, NASS | | 
| Total Population | | | CPS | Raw value from CPS data |
| Total Registered Voters | | | CPS | Raw value from CPS data |
| Share of Individual and Family Farmers in State Population, Excluding Feed Commodities | IFAFXFSP | $`\frac{\text{IFAFXF}}{\text{Total Population}}`$ | ERS, NASS, CPS | Understood as "Number of IFF's, exlcuding feed, per person" |
| Share of Individual and Family Farmers in State Population, Including Feed Commodities | IFAFFSP | $`\frac{\text{IFAFF}}{\text{Total Population}}`$ | ERS, NASS, CPS | Understood as "Number of IFF's, including feed, per person" |
| Share of Individual and Family Farmers in State Population, Excluding Feed Commodities | IFAFXFRV | $`\frac{\text{IFAFXF}}{\text{Total Registered Voters}}`$ | ERS, NASS, CPS | Understood as "Number of IFF's, exlcuding feed, per registered voter" |
| Share of Individual and Family Farmers in State Population, Including Feed Commodities | IFAFFRV | $`\frac{\text{IFAFF}}{\text{Total Registered Voters}}`$ | ERS, NASS, CPS | Understood as "Number of IFF's, including feed, per registered voter" |


## Repository Stucture

### Files for Computing Estimates

#### `data/`
Folder than contains the following data files (all of the data is publicly available).

- `ers_usda.xlsx`: 
    - Excel file containing the annual cash commodities by state, for years 2012 - 2020. 
    - Contains 52 sheets (directory sheet, entire US, and one sheet for each state)
        - **Rows (Granularity)**: Category of commodities
        - **Columns**: Different years
        - **Values**: Annual Cash Receipt for given comodity
    - Entire file is downloadable from the ERS ([here](https://data.ers.usda.gov/reports.aspx?ID=17832))
- `nass_usda.xlsx`:
    - Excel file containing the Number of Family Farmers for each state
        - **Rows (Granularity)**: (State, Year) combination
        - **Columns**: State, Year, Number_of_Family_Farmers
    - Data file was created manually by extracting values from NASS ([here](https://www.nass.usda.gov/Quick_Stats/CDQT/chapter/1/table/1))
        - Equated the field "FARM OPERATIONS, ORGANIZATION, TAX PURPOSES, FAMILY & INDIVIDUAL - NUMBER OF OPERATIONS" with the Number of Family Farmers
    - NASS only has Census data from the years 2012 and 2017
- `census_population_and_voting.xlsx`:
    - Excel File containting state-level population and voter estimates from 2018, 2012
        - **Rows (Granularity)**: (State, Year) combination
        - **Columns**: State, Year, Total_population, Total_Citizen_Population, Total_Registered, Percent_Registered_Total, Total_Registered_Margin_of_Error, Percent_Registered_Citizen, Citizen_Registered_Margin_of_Error, Total_Voted, Percent_Voted_Total, Total_Voted_Margin_of_Error, Percent_Voted_Citizen, Citizen_Voted_Margin_of_Error
        - **Note**: voter and population totals are in thousands
    - The table was manually tweaked to ease the burden of reading and processing the data, but the raw data is available from the U.S. Census Bureau, Current Population Survey, November 2018, and the U.S. Census Bureau, Current Population Survey, November 2012.
        - The 2018 data can be found ([here](https://www.census.gov/data/tables/time-series/demo/voting-and-registration/p20-583.html)), in table 4a
        - The 2012 data can be found ([here](https://www.census.gov/data/tables/2012/demo/voting-and-registration/p20-568.html)), in table 4a
    - The U.S. Census Bureau only has data available every 2 years, so the 2018 data is used as an estimate for the 2017 voter and population numbers
- `family_farmer_estimates_state_level.xlsx`:
    - Excel file containing the estimates for the number of family farmers involved in animal agriculture (**this is the first with the relevant estimates**).
        - **Rows (Granularity)**: State
        - **Columns**: 
            - State
            - **For each of 2017, 2012**: Animal_ag_share_no_feed, Animal_ag_share_feed, Number_of_Family_Farmers, Farmers_in_animal_ag_no_feed, Farmers_in_animal_ag_feed
            - **For each of 2018, 2012**: Total_Population, Total_Citizen_Population, Total_Registered, Percent_Registered_Total, Total_Registered_Margin_of_Error, Percent_Registered_Citizen, Citizen_Registered_Margin_of_Error, Total_Voted, Percent_Voted_Total, Total_Voted_Margin_of_Error, Percent_Voted_Citizen, Citizen_Voted_Margin_of_Error
        - **Note**: voter and population totals are multiplied by 1000 to reflect the true raw values.
    - Only contains estimates for the years 2012, 2017, as those are the only years with census data from the NASS.
    - Only contains population and voting figures for the years 2012, 2018, as those are the years closest to the relevant NASS years (2017, 2012).
- `family_farmer_estimates_state_year_level.xlsx`:
    - Excel file containing the estimates for the number of family farmers involved in animal agriculture (**this is the second file with the relevant estimates**).
    - This file differs from `family_farmer_estimates_state_level.xlsx` in that there are two rows for each state, for both 2017 and 2012 (including this year column allows for additional analysis and plotting).
        - **Rows (Granularity)**: (State, Year) combination
        - **Columns**: 
            - State
            - Year
            - Animal_ag_share_no_feed, Animal_ag_share_feed, Number_of_Family_Farmers, Farmers_in_animal_ag_no_feed, Farmers_in_animal_ag_feed
            - Total_Population, Total_Citizen_Population, Total_Registered, Percent_Registered_Total, Total_Registered_Margin_of_Error, Percent_Registered_Citizen, Citizen_Registered_Margin_of_Error, Total_Voted, Percent_Voted_Total, Total_Voted_Margin_of_Error, Percent_Voted_Citizen, Citizen_Voted_Margin_of_Error
        - **Note**: voter and population totals are multiplied by 1000 to reflect the true raw values.
    - Only contains estimates for the years 2012, 2017, as those are the only years with census data from the NASS.
    - Only contains population and voting figures for the years 2012, 2018, as those are the years closest to the relevant NASS years (2017, 2012).

#### `compute_animal_farmers.py`
Python file that performs data cleaning and calculations

- Reads in `data\ers_usda.xlsx`, calculates agricultural share (with and without feed) for each state
- Reads in `data\nass_usda.xlsx`, joins this census data with the commdity data from 2017 and 2012
- Calculates the number of animal farmers (with and without feed)
- Reads in `data\census_population_and_voting.xlsx`, joins this census data from 2018 and 2012 with the joined data (created in above steps)
- Writes the estimates to excel files (`data\family_farmer_estimates_state_year_level.xlsx`, `data\family_farmer_estimates_state_level.xlsx`)

#### `run.sh`
Bash script that installs necessary libraries (pandas, numpy, openpyxl) and executes `compute_animal_farmers.py`

### Files related to the Web App Dashboard

#### `app.py`
Python file that creates the interative [dashboard](https://gentle-bastion-68761.herokuapp.com/) for comparing and visualizing different metrics across different states.

#### `dictionaries.py`
File that contains python dictionaries that map column names to cleaner titles, legend labels, and their calculations, for the plots on the dashboard. If you would like to change the labels that are used to describe various metrics on the dashboard (i.e. information that changes upon selecting a drop-down option), refer to this file.

#### App Deployment
- `Dockerfile`, `.dockerignore`, `requirements.txt`: files needed to create a Docker image and container for the web app.
- `Procfile`: file needed to deploy the app on Heroku.

---

## Reproducibility

### Computing Estimates

1. Download ([Python](https://www.python.org))
2. Download this repository
3. (Optional) Modify the data files prior to computation (i.e. if method of estimation changes, or new census data becomes available)
4. Open Terminal/Cmd window on machine, navigate to the directory where you have saved the repository, and run the following command (performs [pandas](https://pandas.pydata.org/), [numpy](https://numpy.org/), and [openpyxl](https://openpyxl.readthedocs.io/en/stable/) downloads)

    ```
    bash run.sh
    ```

### Creating and Deploying the Webapp

The interactive dashboard was created using the [pandas](https://pandas.pydata.org/) and [plotly](https://plotly.com/) python libraries, the [dash framework](https://dash.plotly.com/) (from plotly), [Docker](https://www.docker.com/) for containerized development, and [Heroku](https://heroku.com/) for deployment.

---

## Contributions:

- **Developer**: Kendall Kikkawa
- **Researcher**: Galina Hale
- **Collaborator**: Bruce Friedrich
- This project was also conducted with collaboration from the [Good Food Institute](https://gfi.org/).
