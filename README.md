# Rancher Numbers Project (Good Food Institute)
---

This project uses data from the U.S. Department of Agriculture (USDA) to estimate the number of ranchers / family_farmers in the United States, by state. Specifically, we compute two estimates of this measure:
- Number of family farmers in animal agriculture, including feed commodities
- Number of family farmers in animal agriculture, exclusing feed commodities

The methods section below further outlines how these values were calculated.

## Methods

### ERS Commodity Data

The Economic Research Service (ERS), which is a subdivision of the USDA, provides the Annual cash receipts by commodity, for each state (data available [here](https://data.ers.usda.gov/reports.aspx?ID=17832))

For each state, we computed the share of animal agriculture by (1) including feed crops and (2) excluding feed crops (both numbers are decimals). The explicit formulas are given below:

<p align="center">
    <img src="https://latex.codecogs.com/svg.image?\text{Agriculture&space;share&space;without&space;feed}&space;=&space;\frac{\text{Animals&space;and&space;Products}}{\text{All&space;Commodities}}" title="\text{Agriculture share, without feed} = \frac{\text{Animals and Products}}{\text{All Commodities}}" />
</p>

<p align="center">
    <img src="https://latex.codecogs.com/svg.image?\text{Agriculture&space;share&space;with&space;feed}&space;=&space;\frac{\text{Animals&space;and&space;Products&space;&plus;&space;Feed&space;Crops}}{\text{All&space;Commodities}" title="\text{Agriculture share, with feed} = \frac{\text{Animals and Products + Feed Crops}}{\text{All Commodities}" />
</p>


## NASS Census Data

The National Agricultural Statistice Service (NASS), which is a subdivision of the USDA, provides census data for various farm and crop operations, for each state (data available [here](https://www.nass.usda.gov/Quick_Stats/CDQT/chapter/1/table/1))

For each state, we estimate the number of family farmers by using the "FARM OPERATIONS, ORGANIZATION, TAX PURPOSES, FAMILY & INDIVIDUAL - NUMBER OF OPERATIONS" field in the NASS data. We then multiply this by our previously computed share values to get an estimate for the number of animal farmers in each state.

<p align="center">
    <img src="https://latex.codecogs.com/svg.image?\text{Num&space;Animal&space;Farmers,&space;without&space;feed}&space;=&space;\text{(Ag.&space;Share,&space;without&space;feed)}&space;*&space;\text{(Num&space;Family&space;Farmers)}" title="\text{Num Animal Farmers, without feed} = \text{(Ag. Share, without feed)} * \text{(Num Family Farmers)}" />
</p>

<p align="center">
    <img src="https://latex.codecogs.com/svg.image?\text{Num&space;Animal&space;Farmers,&space;with&space;feed}&space;=&space;\text{(Ag.&space;Share,&space;with&space;feed)}&space;*&space;\text{(Num&space;Family&space;Farmers)}" title="\text{Num Animal Farmers, with feed} = \text{(Ag. Share, with feed)} * \text{(Num Family Farmers)}" />
</p>

## Repository Stucture

`data/`: Folder than contains the following data files
- `ers_usda.xlsx`: 
    - Excel file containing the annual cash commodities by state, for years 2012 - 2020. 
    - Contains 52 sheets (directory sheet, entire US, and one sheet for each state)
        - Rows (Granularity): Category of commodities
        - Columns: Different years
        - Values: Annual Cash Receipt for given comodity
    - Entire file is downloadable from the ERS ([here](https://data.ers.usda.gov/reports.aspx?ID=17832))
- `nass_usda.xlsx`:
    - Excel file containing the Number of Family Farmers for each state
        - Rows (Granularity): (State, Year) combination
        - Columns: State, Year, Number of Family Farmers
    - Data file was created manually by extracting values from NASS ([here](https://www.nass.usda.gov/Quick_Stats/CDQT/chapter/1/table/1))
        - Equated the field "FARM OPERATIONS, ORGANIZATION, TAX PURPOSES, FAMILY & INDIVIDUAL - NUMBER OF OPERATIONS" with the Number of Family Farmers
    - NASS only has Census data from the years 2012 and 2017
- `family_farmer_estimates.xlsx`:
    - Excel file containing the estimates for the number of family farmers involved in animal agriculture (i.e. the file with the relevant estimates)
        - Rows (Granularity): (State, Year) combination
        - Columns: 
            - State
            - Year
            - Agriculture share without feed
            - Agriculture share with feed
            - Number of Family Farmers
            - Number of Animal Farmers without feed
            - Number of Animal Farmers with feed
    - Only contains estimates for the years 2012, 2017, as those are the only years with census data from the NASS

`compute_ranchers.py`: Python file that performs data cleaning and calculations
- Reads in `data\ers_usda.xlsx`, calculates agricultural share (with and without feed) for each state
- Reads in `data\nass_usda.xlsx`, joins this census data with the commdity data from 2012 and 2017
- Calculates the number of animal farmers (with and without feed)
- Writes the estimates to excel file (`data\family_farmer_estimates.xlsx`)

`run.sh`: Bash script that installs necessary libraries (pandas, numpy) and executes `compute_ranchers.py`

---

## Reproducibility

1. Download Python ([here] https://www.python.org/downloads/macos/)
2. Download this repository
3. (Optional) Modify the data files prior to computation (i.e. if method of estimation changes, or new census data becomes available)
4. Open Terminal/Cmd window on machine, navigate to the directory where you have saved the repository, and run the following command

    ```
    bash run.sh
    ```

---

## Contributors:

- Kendall Kikkawa
- Galina Hale
- Bruce Friedrich