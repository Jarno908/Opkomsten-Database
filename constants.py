#! Python3

# Version
APP_VERSION = '0.2.1'
APP_NAME = 'ScoutingDocumentenApp'
APP_TITLE = APP_NAME + " V" + APP_VERSION

GITHUB_REPO = 'Jarno908/Opkomsten-Database'

# Sorting
FORBIDDEN_CHARACTERS = '/\\?%*:|"<>'
DOCUMENT_TYPES = {"O":"Opkomst"}
KEYS_TO_LOWER =    ["Materiaal",
                    "Zoekwoorden",
                    "Speltak(ken)",
                    "Categorie"]

#Opkomst-document
OPKOMST_KEYS = ["Titel",
                "Auteur",
                "Datum",
                "Speltak(ken)",
                "Categorie",
                "Omschrijving",
                "Materiaal",
                "Zoekwoorden",
                "version"]

SPELTAKKEN =   ["Bevers",
                "Welpen",
                "Verkenners",
                "Explorers",
                "Roverscouts",
                "Stam",
                "+Scouts",
                "Overig"]

SPELTAKKEN_DICTIONARY =    {"bevers" : "Bevers",
                            "bever" : "Bevers",
                            "welpen" : "Welpen",
                            "welp" : "Welpen",
                            "verkenners" : "Verkenners",
                            "verkenner" : "Verkenners",
                            "scouts" : "Verkenners",
                            "scout" : "Verkenners",
                            "explorers" : "Explorers",
                            "explorer" : "Explorers",
                            "rsa" : "Explorers",
                            "rsa429" : "Explorers",
                            "roverscouts" : "Roverscouts",
                            "roverscout" : "Roverscouts",
                            "rover scouts" : "Roverscouts",
                            "rover-scouts" : "Roverscouts",
                            "rovers" : "Roverscouts",
                            "rover" : "Roverscouts",
                            "stam" : "Stam",
                            "hakwadagstam" : "Stam",
                            "hakwadag stam" : "Stam",
                            "hakwadag-stam" : "Stam",
                            "hakwadag" : "Stam",
                            "+scouts" : "+scouts",
                            "+scout" : "+scouts",
                            "+ scouts" : "+scouts",
                            "plusscouts" : "+scouts",
                            "plus scouts" : "+scouts",
                            "plus-scouts" : "+scouts",
                            "plus_scouts" : "+scouts",
                            "overig" : "Overig"}

CATEGORIES =   ["Uitdagende Scoutingtechnieken",
                "Buitenleven",
                "Expressie",
                "Sport & Spel",
                "Identiteit",
                "Samenleving",
                "Internationaal",
                "Veilig & Gezond",
                "Overig"]

CATEGORIES_DICTIONARY =    {"uitdagende scoutingtechnieken" : "Uitdagende Scoutingtechnieken",
                            "uitdagendescoutingtechnieken" : "Uitdagende Scoutingtechnieken",
                            "uitdagende_scoutingtechnieken" : "Uitdagende Scoutingtechnieken",
                            "uitdagende-scoutingtechnieken" : "Uitdagende Scoutingtechnieken",
                            "buitenleven" : "Buitenleven",
                            "buiten leven" : "Buitenleven",
                            "buiten-leven" : "Buitenleven",
                            "buiten_leven" : "Buitenleven",
                            "expressie" : "Expressie",
                            "expresie" : "Expressie",
                            "sport & spel" : "Sport & Spel",
                            "sport &spel" : "Sport & Spel",
                            "sport& spel" : "Sport & Spel",
                            "sport&spel" : "Sport & Spel",
                            "sport en spel" : "Sport & Spel",
                            "sporten spel" : "Sport & Spel",
                            "sport enspel" : "Sport & Spel",
                            "sportenspel" : "Sport & Spel",
                            "sport spel" : "Sport & Spel",
                            "sportspel" : "Sport & Spel",
                            "identiteit" : "Identiteit",
                            "identitijt" : "Identiteit",
                            "samenleving" : "Samenleving",
                            "samen leving" : "Samenleving",
                            "samen_leving" : "Samenleving",
                            "samen-leving" : "Samenleving",
                            "internationaal" : "Internationaal",
                            "international" : "Internationaal",
                            "inter-nationaal" : "Internationaal",
                            "inter nationaal" : "Internationaal",
                            "inter_nationaal" : "Internationaal",
                            "veilig & gezond" : "Veilig & Gezond",
                            "veilig& gezond" : "Veilig & Gezond",
                            "veilig &gezond" : "Veilig & Gezond",
                            "veilig&gezond" : "Veilig & Gezond",
                            "veilig en gezond" : "Veilig & Gezond",
                            "veiligen gezond" : "Veilig & Gezond",
                            "veilig engezond" : "Veilig & Gezond",
                            "veiligengezond" : "Veilig & Gezond",
                            "veilig gezond" : "Veilig & Gezond",
                            "veiliggezond" : "Veilig & Gezond",
                            "overig" : "Overig"}
