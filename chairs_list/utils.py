from datetime import date
from urllib.parse import quote as uri_encode


def term_str(date=date.today()) -> str:
    year = date.year
    if date.month < 5:
        term = "Spring"
    elif date.month < 8:
        term = "Summer"
    else:
        term = "Fall"

    return f"{term} {year}"


# keys are Supervisory Organizations from Academic Chair Assignments report in Workday
# we have to map to a list solely because of CES which has two department codes
# TODO add parent division, looks like "X Faculty": {"codes": ["X"], "division": "Y"}
dept_codes_map: dict[str, list[str]] = {
    "Animation Faculty": ["ANIMA"],
    "Architecture Faculty": ["ARCHT"],
    "Ceramics Faculty": ["CERAM"],
    "Comics Faculty": ["COMIX"],
    "Community Arts Faculty": ["COMAR"],
    "Craft Faculty": ["CRAFT"],
    "Critical Ethnic Studies Faculty": ["ETHSM", "ETHST"],
    "Critical Studies Faculty": ["CRTSD"],
    "Fashion  Design Faculty": ["FASHN"],
    "Film Faculty": ["FILMS"],
    "First Year Core Studio Faculty": ["FYCST"],
    "Furniture Faculty": ["FURNT"],
    "Game Arts Faculty": ["GAMES"],
    "Glass Faculty": ["GLASS"],
    "Graduate Architecture Faculty": ["MARCH"],  # MAAD syllabi are under MARCH
    "Graduate Comics Faculty": ["COMIC"],
    "Graduate Curatorial Practice Faculty": ["CURPR"],
    "Graduate Design Faculty": ["DESGN"],
    "Graduate Design Strategy Faculty": [""],
    "Graduate Film Faculty": ["FLIMG"],
    "Graduate Fine Arts Faculty": [""],
    "Graduate Interaction Design Faculty": ["IXDGR"],
    "Graduate Visual and Critical Studies Faculty": ["VISCR"],
    "Graduate Writing Faculty": ["WRITE"],
    "Graphic Design Faculty": ["GRAPH"],
    "History of Art and Visual Culture Faculty": ["HAAVC"],
    "Illustration Faculty": ["ILLUS"],
    "Individualized Faculty": ["INDIV"],
    "Industrial Design Faculty": ["INDUS"],
    "Interaction Design Faculty": ["IXDSN"],
    "Interior Design Faculty": ["INTER"],
    "Jewelry and Metal Arts Faculty": ["METAL"],
    "Painting and Drawing Faculty": ["PNTDR"],
    "Photography Faculty": ["PHOTO"],
    "Printmedia Faculty": ["PRINT"],
    "Sculpture Faculty": ["SCIULP"],
    "Textiles Faculty": ["TEXTL"],
    "Upper Division Interdisciplinary Studio Faculty": ["UDIST"],
    "Writing and Literature Faculty": ["WRLIT"],
}


def vault_syllabi_hierarchy_url(division, dept_code: str, semester) -> str:
    # uri encode strings
    return f"https://vault.cca.edu/logon.do?page=%2Fhierarchy.do%3Ftopic%3D17c784ec-650f-4381-8492-f1a3edf7d8c0%3A{uri_encode(dept_code)}%2Cf416503d-ff0a-47f3-aaaa-93b7ea083873%3A{uri_encode(division)}%2C289af057-1502-498a-b73a-259f26b968c0%3A{uri_encode(semester)}%26sort%3Dname"
