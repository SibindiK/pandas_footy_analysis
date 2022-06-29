#url to source of football data website
MAIN_FOOTBALL_DATA_WEBSITE_URL = "https://www.football-data.co.uk/all_new_data.php"
ALL_EURO_LEAGUES_DATA_URL='https://www.football-data.co.uk/mmz4281/2122/all-euro-data-2021-2022.xlsx'
ALL_EURO_FIXTURES_URL = 'https://www.football-data.co.uk/fixtures.xlsx'
EXCEL_FILE_PATH = f'data/2022_04_30.xlsx'

#messages
LOADING_IN_PROGRESS_MESSAGE = "Loading in Progress"
LOADING_COMPLETE_MESSAGE = "Loading Successfully Completed"
NO_DATA_MESSAGE = "No Data Loaded!!. Load Data First"

#data tables column names
MAIN_LEAGUES_DATA_COLS = ['Div','Date','HomeTeam','AwayTeam','FTHG','FTAG',
                        'FTR','HTHG','HTAG','HTR','HS','AS','HST','AST',
                        'HC','AC','HY','AY','HR','AR']

OTHER_LEAGUES_DATA_COLS = ['Country','League','Season','Date','Home','Away','HG','AG','Res']

FIXTURES_DATA_COLS = ['Div','Date','Time','HomeTeam','AwayTeam']

FT_HOMES_TABLE_DATA_COLS = ['HomeTeam','Played','Won','Draw','Lost','HomePts',
                        'GamesScored','Scored2','FTHG','FailToScore',
                        'GamesConceded','HS','HST','HC','HY','HR']

FT_AWAYS_TABLE_DATA_COLS = ['AwayTeam','Played','Won','Draw','Lost','AwayPts',
                        'GamesScored','Scored2','FTAG','FailToScore',
                        'GamesConceded','AS','AST','AC','AY','AR']

HT_HOMES_TABLE_DATA_COLS = ['HomeTeam','Played','Won','Draw','Lost','HomeHTPts',
                        'GamesScored','Scored2','HTHG','FailToScore',
                        'GamesConceded']

HT_AWAYS_TABLE_DATA_COLS = ['AwayTeam','Played','Won','Draw','Lost','AwayHTPts',
                        'GamesScored','Scored2','HTAG','FailToScore',
                        'GamesConceded']
