import pandas as pd
import numpy as np


def clean_ers_data(state_name: str) -> pd.DataFrame: 
    """
    Cleans ERS data (in 'ers_usda.xlsx') containing commodity receipts by state

    Input:
    - state_name (str): name of the state to be cleaned

    Output:
    - state_data (pd.DataFrame): dataframe containing cleaned commodity data
    """
    # Read in file
    state_data = pd.read_excel('data/ers_usda.xlsx', header=2, sheet_name=state_name)
    # Extract State name
    state_name = states[i]
    # Rename State Column
    state_data = state_data.rename(columns={state_name: 'Commodity_Type'})
    # Drop rows with null values
    state_data = state_data[~state_data['Commodity_Type'].isna()]
    # Reset Index
    state_data = state_data.reset_index(drop=True)
    # Drop columns with all null values (not needed)
    state_data = state_data.dropna(axis=1, how='all')
    
    # Extract column Names
    col_names = state_data['Commodity_Type']
    # Change granularity: each row is a State_year, columns contain comodity data
    state_data = state_data.transpose().iloc[1:, :]
    # set column names
    state_data.columns = col_names
    # Reset index again, after transpose
    state_data = state_data.reset_index()
    # Create Year Variable, clean "2021F"
    state_data = state_data.rename(columns={"index": "Year"})
    state_data['Year'] = state_data['Year'].str.replace("2021F", "2021")
    # Create State Variable
    state_data["State"] = state_name
    # Move state to front
    cols = state_data.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    state_data = state_data[cols]

    print(f"Loaded ERS Commodity data for {state_name}")

    return state_data


if __name__ == "__main__":
    # Initialize states data and dataframe list
    states = pd.read_excel('data/ers_usda.xlsx', sheet_name=0).iloc[:, 1]
    state_dfs = []

    # Read and clean ERS commodity data for each state
    for i in range(len(states)): # 0 for U.S., 1-50 for the 50 states
        # Clean File
        state_data = clean_ers_data(states[i])
        # Append state dataframe to list
        state_dfs.append(state_data)

    # Concatenate ERS dataframes to one large table
    ers_data = pd.concat(state_dfs).reset_index(drop=True)
    # Fill null values with 0: certain states dont have certain commodities
    ers_data = ers_data.fillna(0)
    # Convert non State/Year columns to numeric
    ers_data.iloc[:, 2:] = ers_data.iloc[:, 2:].apply(pd.to_numeric)

    ### COMPUTE ANIMAL AGRICULTURE SHARE WITOUT FEED: 
    # "Animals and Products / All Commodities"
    ers_data["Animal_ag_share_no_feed"] = ers_data["Animals and products"] / ers_data["All commodities"]
    ### COMPUTE ANIMAL AGRICULTURE SHARE WTIH FEED:  
    # ("Animals and Products" + "Feed Crops") / All Commodities"
    ers_data["Animal_ag_share_feed"] = (ers_data["Animals and products"] + ers_data["Feed crops"]) / ers_data["All commodities"]

    print("\nComputed Animal Agriculture Share (with and without feed)")

    # Load NASS data - created manually
    nass_data = pd.read_excel('data/nass_usda.xlsx')
    # Drop columns with all null values (not needed)
    nass_data = nass_data.dropna(axis=1, how='all')

    # Join ERS data with NASS data
    nass_data['Year'] = nass_data['Year'].astype(str) # Convert Year to string for joining
    all_data = ers_data.merge(nass_data, on=['State', 'Year'], how="left")

    print("\nJoined ERA data with NASS data")

    ### COMPUTE NUMBER OF FAMILY FARMERS IN ANIMAL AG WITHOUT FEED
    # ("Animals and Products / All Commodities") * Number of Family Farmers
    all_data['Farmers_in_animal_ag_no_feed'] =  np.rint(all_data['Animal_ag_share_no_feed'] * all_data["Number of Family Farmers"])
    ###  COMPUTE NUMBER OF FAMILY FARMERS IN ANIMAL AG WITHOUT FEED
    # (("Animals and Products" + "Feed Crops") / All Commodities") * Number of Family Farmers
    all_data['Farmers_in_animal_ag_feed'] =  np.rint(all_data['Animal_ag_share_feed'] * all_data["Number of Family Farmers"])

    print("\nComputed Number of Family Farmers in Animal Agriculture (with and without feed)")

    # Reduce dataset to the relevant years and columns
    census_data = all_data[all_data["Year"].isin(["2012", "2017"])][["State", "Year", "Animal_ag_share_no_feed", "Animal_ag_share_feed", 
                                                "Number of Family Farmers", "Farmers_in_animal_ag_no_feed", 
                                                "Farmers_in_animal_ag_feed"]]

    # Export dataset as excel file
    census_data.to_excel('data/family_farmer_estimates.xlsx', index=False)

    print("\nExported rancher dataset as excel file in the data/ directory\n")
