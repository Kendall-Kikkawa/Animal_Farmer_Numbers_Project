###### DICTIONARIES TO MAKE NICER TITLES AND LEGENDS ON THE APP #######

## Dictionary to map columns to cleaner version of the metric
titles_Dict = { 'Animal_ag_share_no_feed': 'Animal Agriculture Share, Excluding Feed Commodities (AASXF)',
                'Animal_ag_share_feed': 'Animal Agriclutre Share, Including Feed Commodities (AASF)',
                'Number_of_Family_Farmers': 'Number of Individual and Family Farmers (IFF)',
                'Farmers_in_animal_ag_no_feed': 'Individual and Family Animal Farmers, Excluding Feed Commodities (IFAFXF)',
                'Farmers_in_animal_ag_feed': 'Individual and Family Animal Farmers, Including Feed Commodities (IFAFF)',
                'Total_Population': 'Total Population',
                'Total_Registered': 'Total Registered Voters',
                'farmers_no_feed_per_person': 'Share of Individual and Family Animal Farmers in State Population, Excluding Feed Commodities (IFAFXFSP)',
                'farmers_feed_per_person': 'Share of Individual and Family Animal Farmers in State Population, Including Feed Commodities (IFAFXFTRV)',
                'farmers_no_feed_per_voter': 'Share of Individual and Family Animal Farmers in Total Registered Voters, Excluding Feed Commodities (IFAFFSP)',
                'farmers_feed_per_voter': 'Share of Individual and Family Animal Farmers in Total Registered Voters, Including Feed Commodities (IFAFFTRV)'
                }

## Dictionary to map columns to the legend title used in the figure
legends_Dict = {'Animal_ag_share_no_feed': 'Share (%)',
                'Animal_ag_share_feed': 'Share (%)',
                'Number_of_Family_Farmers': '# of Farmers',
                'Farmers_in_animal_ag_no_feed': '# of Farmers',
                'Farmers_in_animal_ag_feed': '# of Farmers',
                'Total_Population': '# of People',
                'Total_Registered': '# of Voters',
                'farmers_no_feed_per_person': '# Farmers / Person',
                'farmers_feed_per_person': '# Farmers / Person',
                'farmers_no_feed_per_voter': '# Farmers / Voter',
                'farmers_feed_per_voter': '# Farmers / Voter'
                }

## Dictionary to map columns to the calculation used to compute them
dataSources_Dict = {'Animal_ag_share_no_feed': 'ERS',
                    'Animal_ag_share_feed': 'ERS',
                    'Number_of_Family_Farmers': 'NASS',
                    'Farmers_in_animal_ag_no_feed': 'ERS, NASS',
                    'Farmers_in_animal_ag_feed': 'ERS, NASS',
                    'Total_Population': 'CPS',
                    'Total_Registered': 'CPS',
                    'farmers_no_feed_per_person': 'ERS, NASS, CPS',
                    'farmers_feed_per_person': 'ERS, NASS, CPS',
                    'farmers_no_feed_per_voter': 'ERS, NASS, CPS',
                    'farmers_feed_per_voter': 'ERS, NASS, CPS',
                    }

## Dictionary to map columns to the calculation used to compute them
calculations_Dict = {'Animal_ag_share_no_feed': '''AASXF = (Animals and Products) / (All Commodities)''',
                    'Animal_ag_share_feed': '''AASF = (Animals and Products + Feed Crops) / (All Commodities)''',
                    'Number_of_Family_Farmers': '''IFF = (NASS Field) "FARM OPERATIONS, ORGANIZATION, TAX PURPOSES, FAMILY & INDIVIDUAL - NUMBER OF OPERATIONS"''',
                    'Farmers_in_animal_ag_no_feed': '''IFAFXF = AASXF * IFF''',
                    'Farmers_in_animal_ag_feed': '''IFAFF = AASXF * IFF''',
                    'Total_Population': 'Raw value from CPS',
                    'Total_Registered': 'Raw value from CPS',
                    'farmers_no_feed_per_person': 'IFAFXFSP = (IFAFXF) / (Total Population)',
                    'farmers_feed_per_person': 'IFAFXFTRV = (IFAFXF) / (Total Registered Voters)',
                    'farmers_no_feed_per_voter': 'IFAFFSP = (IFAFF) / (Total Population)',
                    'farmers_feed_per_voter': 'IFAFXFTRV = (IFAFXF) / (Total Registered Voters)'
                    }