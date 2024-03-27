import json
import pandas as pd
import numpy as np


def string_to_nums(data: list) -> list:
    """Converts features supposed to be string as float

    Args:
        data (list): dataset

    Returns:
        list: dataset
    """
    """Converts string values to numbers

    Args:
        data (list): Property data

    Returns:
        list: Modified property data
    """
    new_data = []
    str_list = [
        "price",
        "Taxes",
        "Maintenance",
        "Bedrooms",
        "Bedrooms Plus",
        "Bathrooms",
        "Kitchens",
        "Rooms",
        "Rooms Plus",
        "Parking Places",
        "Parking Total",
        "Stories",
        "Locker Level",
        "Tax Year",
        "propertyLat",
        "propertyLng",
        "Lot Depth",
        "Frontage",
    ]

    for item in data:
        new_item = item.copy()
        for key in str_list:
            # Exception for price
            if key == "price":
                new_item[key] = new_item[key].split("$").pop().replace(",", "")
                try:
                    price_int = float(new_item[key])
                except Exception as e:
                    print(f"{key}: Caught exception {e}")
                    price_int = None
                new_item[key] = price_int
            else:
                try:
                    num = float(new_item[key])
                except Exception as e:
                    print(f"{key}: Caught exception {e}")
                    num = None
                new_item[key] = num
        new_data.append(new_item)
    return new_data


def lotDepth_remove_nulls(data: list):
    new_data: list = []
    for item in data:
        new_item = item.copy()
        if "Lot Depth" in new_item:
            if new_item["Lot Depth"] == None:
                print(f"Lot Depth found as Null for {new_item["street_address"]}")
                new_item["Lot Depth"] = 0

        new_data.append(new_item)
    return new_data


def frontage_remove_nulls(data: list):
    new_data: list = []
    for item in data:
        new_item = item.copy()
        if "Frontage" in new_item and "Type" in new_item:  # Check if both keys exist
            if new_item["Frontage"] == None and new_item["Type"] == "Condo Apt":
                print(f"{new_item['street_address']} - {new_item['Type']} found no frontage, changing to 0")
                new_item["Frontage"] = 0
        new_data.append(new_item)
    return new_data


def remove_vacant_land(data: list):
    new_data: list = []
    for item in data:
        new_item = item.copy()
        if "Type" in new_item and new_item["Type"] != "Vacant Land" and new_item["street_address"] != "":
            new_data.append(new_item)
        else:
            print(f"Excluded item {new_item['street_address']}  - {new_item.get('Type', 'Type not found')}")
    return new_data


def convert_to_bool(data: list):
    features = ["Den/Family Room","Central Vac", "Retirement", "Ensuite Laundry", "Elevator", "Fireplace", "Cable Included", "Heating Included", "Parking Included", "Water Included", "Central A/C Included", "Electricity", "Gas", "Cable", "Telephone", "Handicap Equipped"]
    
    new_data: list = []
    for item in data:
        new_item = item.copy() 
        for feature in features: # Loop through features list
            if feature in new_item:  # Check if the feature exists in the item
                if new_item[feature] == "Y":
                    new_item[feature] = 1
                elif new_item[feature] == "N":
                    new_item[feature] = 0
                else:
                    print(f"address {new_item['street_address']} not bool: {new_item[feature]}")
            else:
                continue
        new_data.append(new_item)
        
    return new_data

def remove_office_types(data: list):
    new_data: list = []
    for item in data:
        new_item = item.copy()
        if "Type" in new_item and new_item["Type"] != "Office":
            new_data.append(new_item)
        else:
            print(f"{new_item["street_address"]} is an office, removing...")
    return new_data

def clean_sqft(data: list) -> list:
    """Converts sqft feature into two features, sqft_range_min
    and sqft_range_max

    Args:
        data (list): dataset

    Returns:
        list: dataset
    """
    new_data = []
    for item in data:
        new_item = item.copy()
        if "Size (sq ft)" in new_item:
            sqft_raw: str = new_item["Size (sq ft)"]
            if "-" in sqft_raw:
                sqft_range_list = sqft_raw.split("-")
                sqft_range_min = int(sqft_range_list[0].replace("+", ""))
                sqft_range_max = int(sqft_range_list[1].replace("+", ""))
                # Add it to the dict
                new_item["sqft_range_min"] = sqft_range_min
                new_item["sqft_range_max"] = sqft_range_max
            else:
                print(f"clean_sqft: Unexpected format in {new_item['Size (sq ft)']}")

            # Remove the sqft string
            new_item.pop("Size (sq ft)", None)
        else:
            print(f"clean_sqft: No sqft in {new_item['street_address']}")
        new_data.append(new_item)
    return new_data


def clean_age(data: list) -> list:
    """Converts age feature into two features, age_range_min
    and age_range_max

    Args:
        data (list): dataset

    Returns:
        list: dataset
    """
    new_data = []
    for item in data:
        new_item = item.copy()
        if "Age" in new_item:
            age_raw: str = new_item["Age"]
            if age_raw == "New":
                age_range_min = 0
                age_range_max = 0
            elif "-" in age_raw:
                age_range_list: list = age_raw.split("-")
                age_range_min = int(age_range_list[0].replace("+", ""))
                age_range_max = int(age_range_list[1].replace("+", ""))
            else:
                print(f"clean_age: Unexpected format in {new_item['Age']}")
                continue

            # Add it to dict and remove old feature
            new_item["age_range_min"] = age_range_min
            new_item["age_range_max"] = age_range_max
            new_item.pop("Age", None)
        new_data.append(new_item)
    return new_data


def remove_unneeded_attrs(data: list):
    """Removes unneeded features from the dataset

    Args:
        data (list): dataset

    Returns:
        _type_: dataset
    """
    new_data = []
    unwanted: set = (
        "appuuid",
        "isListingPage",
        "sarea",
        "searchCity",
        "hasVirtualTour",
        "tourIsHttpsEnabled",
        "customFilterSearch",
        "isCommercialSearch",
        "appStoreRedirect",
        "Parcel Number",
        "propertyId",
        "Virtual Tour",
        "searchNeighborhood",
        "pageAction",
        "Corporation Number",
        # These ones I'm removing as a test
        "Patio Terrace",
        "Unit Exposure",
        "Parking Space",
        "Parking Description",
        "Parking Designation",
        "Parking Features",
        "Parking Places",
        "Lockers",
        "Locker Level",
        "Locker Number",
        "Building Insurance Included",
        "Common Elements Included",
        "Cross Street",
        "Municipality District",
        "Garage",
        "Locker Quantity",
        "Amenity",
        "Feature",
        "Condo Corporation",
        "Property Management",
        "isResidentialProperty",
        "Zoning",
        "mapArea",
        "Bedrooms Plus",  # Have no idea what this is
        "Rooms Plus",
        "Community",
        "Tax Year",
        "Sewer",
        "Hydro Included",
        "Covered Parking Places",
        "Fronting On",
        "Lot Size Units",
        "Water supply",
        "Acres ", # Not sure if this is unnecessary
        "Open House Date",
        "Open House Start",
        "Open House Finished",
        "Tax Legal Description",
        "Assesment Year",
        "Assessment",
        "Lot Irregularities",
        "Parcel of Tied Land",
        "Style", # Not sure if needed
        "Green PIS",
        "Driveway",
        "Energy Certificate",
        "Exterior Features",
        "Open House Start ",
        "Open House From ",
        "Exterior",
        "Additional Monthly Fee",
        "Apartment Number",
        "Cable",
        "Sold Date",
        "Closed Date",
        "Expiry Date",
        "Sold Price",
        "Unavailable Date",
        "Input Date",
        "Prior LSC",
        "Free Standing",
        "Kitchens Plus", # Not sure if needed
        "Share Percentage",
        "Shore Allow",
        "Shoreline Exposure",
        "Conditional",
        "Conditional Sold Extension",
        "Days on Market",
        "List Date",
        "Last Status",
        "Cable Included",
        "Certificate Level",
        "Waterfront",
        "Farm/Agriculture",
        "Handicap Equipped",
        "Parking Charges",
        "Retirement",
        "Sprinklers",
        "UFFI",
        "List Price Type",
        "Lot Code",
        "Water Body Name",
        "Water Source",
        "Water Supply",
        "Waterfront Features",
        "Taxes Included",
        "Structure",
        "Municipality",
        "Area",
        "Telephone"
    )

    for item in data:
        new_item = item.copy()
        for attr in unwanted:
            new_item.pop(attr, None)
        new_data.append(new_item)

    return new_data

def pandas_cleanup(data: list):
    col_list = ["Central A/C Included", "Central Vac", "Elevator", "Ensuite Laundry", "Heating Included", "Kitchens", "Maintenance", "Parking Included", "Rooms", "Stories", "Taxes", "Water Included", "Age Range Max", "Age Range Min"]
    df = pd.DataFrame(data)
    
    # Simple convert to 0.0 (no other unique results)
    for col in col_list:
        if col in df.columns:
            df[col] = df[col].fillna(0.0)
        
    df["Air Conditioning"] = df["Air Conditioning"].replace({None: 0, "Central Air": 1, "Wall Unit": 1, "None": 0, "Window Unit": 1, "Other": 1})
    df["Basement"] = df["Basement"].replace({None: 0, "None": 0, "Sep Entrance": 1, "Full": 1, "Unfinished": 0, "Finished": 1, "Part Bsmt": 1, "Apartment": 1, "Fin W/O": 0, "W/O": 0, "Walk-Up": 1, "Part Fin": 1, "Half": 1, "Other": 0})
    df['Electricity'] = df["Electricity"].replace({None: 0, "A": 1})
    df['Furnished'] = df["Furnished"].replace({None: 0, "Part": 1, "Y": 1})
    df['Gas'] = df['Gas'].replace({None: 0, 'A': 1})
    df['Heating'] = df['Heating'].replace({None: 0, 'Forced Air': 1, "Heat Pump": 1, "Fan Coil": 1, "Radiant": 1,"Baseboard": 1, "Other": 0})
    df["Laundry"] = df["Laundry"].replace({None: 0, "Ensuite": 1})
    df["Pets"] = df["Pets"].replace({None: 0, "Restrict": 1, "N": 0})
    df["Pool"] = df["Pool"].replace({None: 0, "None": 0, "Inground": 1, "Abv Grnd": 1, "Indoor": 1})
    df["Private Entrance"] = df["Private Entrance"].replace({None: 0, "N": 0, "Y": 1})
    
    
    # Drop lease rows
    df = df.loc[df["Status"] != "Lease"]
    
    
    # Replace all NaN with null in json
    df = df.replace({np.nan:None})
    return df.to_dict('records')

def main():
    datasets = {"small": "test.json", "large": "zolo_total_unclean.json"}
    try:
        with open(datasets["large"], "r") as f:
            data = json.loads(f.read())
    except IOError:
        print("Error opening or reading input file.")
        return

    # Data cleanup
    data = string_to_nums(data)
    data = clean_sqft(data)
    data = clean_age(data)
    data = remove_unneeded_attrs(data)
    data = lotDepth_remove_nulls(data)
    data = frontage_remove_nulls(data)
    data = remove_vacant_land(data)
    data = convert_to_bool(data)
    data = remove_office_types(data) # Since focus is residential
    
    # Pandas stuff
    data = pandas_cleanup(data)
    
    # Data write
    try:
        with open("result.json", "w") as f:
            print("dumping data")
            json.dump(data, f)
    except IOError:
        print("Error opening or writing to output file.")


main()


"""
TASKS: 

[ DO THIS ] Make a function to convert nulls to 0 just for general purpose of different features

[ DO THIS ] Convert Boolean Features: Features like "Ensuite Laundry", "Fireplace", "Building Insurance Included", "Cable Included", etc., seem to have values "Y" or "N" which represent Yes/No. 
These can be converted to binary 1/0 representation which is more suitable for machine learning algorithms.

[ DO THIS ] Handle Null Values: Features like "Rooms Plus" and "Locker Level" have null values. 
\Depending on the proportion of missing values and the importance of the feature, you can choose to fill them with a 
default value (like the mean or median for numerical features, or the most common value for categorical features), 
or you might choose to drop the feature if it has too many missing values.

[ ] Categorical Encoding: Features like "Unit Exposure", "Air Conditioning", "Pets", "Heating", "Exterior", "Garage", etc., 
are categorical. You might want to convert these to numerical values using techniques like one-hot encoding or ordinal encoding, 
depending on the nature of the category.

[ ] Text Processing: The "description" field is a text field. If you want to use this in your model, you might need to 
perform text preprocessing steps like tokenization, stemming, or vectorization (like TF-IDF or word embeddings).

[ ] Drop Unnecessary Features: Some features might not be useful for your model, like "Virtual Tour" (which is a URL), 
"pageAction", "mapArea", etc. You can consider dropping these.

[ ] Feature Engineering: You can create new features based on existing ones. For example, you can create a "Total Amenities Included"
feature by adding up all the "Included" features.

[ ] Maybe I should've converted all of this to a DF first before doing cleanup...

[ ] Pool = All none and null = 0; all else == 1

[ ] Sale -- Remove any lease 

[ ] Merge "Price" and "List Price"

[ ] Fix "Basement" types

Project Phases:

Data Collection: Gather your data from various sources.

Data Cleaning: Handle missing values, remove duplicates, correct errors, etc.

Data Exploration: Understand the distribution of your data, the relationships between features, etc.

Feature Engineering: Create new features, transform existing ones, encode categorical variables, normalize numerical variables, etc.

Modeling: Train your machine learning model on your preprocessed dataset.

Evaluation: Assess the performance of your model, tune hyperparameters, etc.

Deployment: Implement your model in a production environment.

"""
