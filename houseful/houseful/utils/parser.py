import json
import re

data_str = '\n    var ZOLO_DATA = {\n        appuuid: "",\n        pageAction: "property",\n        isListingPage: true,\n        isResidentialProperty: true,\n        sarea: "",\n        mapArea: "100 Parrotta Drive, Toronto M9M 0B5",\n        propertyId: "15355882",\n        propertyLat: "43.734039",\n        propertyLng: "-79.534195",\n        searchCity: "toronto",\n        searchNeighborhood: "humberlea-pelmo-park-w5",\n        hasVirtualTour: false,\n        tourIsHttpsEnabled: false,\n        customFilterSearch: "",\n        isCommercialSearch: false,\n        appStoreRedirect: "https:\\/\\/www.zolo.ca\\/app"\n    }'


def parse_zolo_json(data: str) -> dict:
    # Remove the variable assignment part to get just the JSON-like string
    data = re.sub(r"var ZOLO_DATA = ", "", data).strip()

    # Properly escape backslashes before manipulating the string further
    data = data.replace("\\", "\\\\")

    # Add double quotes around the keys
    data = re.sub(
        r'(?<!\\)"', "'", data
    )  # Temporarily replace unescaped double quotes with single quotes
    data = re.sub(
        r"([\{\s,])(\w+)(\s*:)", r'\1"\2"\3', data
    )  # Add double quotes around the keys
    data = data.replace("'", '"')  # Revert single quotes back to double quotes

    # Load the string as a JSON object
    data_dict = json.loads(data)
    print(data_dict)
    return data_dict
