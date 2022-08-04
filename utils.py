import requests
import pandas as pd

def aspects():
    """
    Returns a pandas DataFrame with additional information regarding the various
    aspects, such as f. ex. a full description of what each aspect concretely
    refers to and from which year on the respectively required data is available
    on bbref.
    Used f. ex. in query_io.get_query() when displaying the different aspect
    options, in sourcing.get_season_stats() when subsetting the DataFrame, and
    in plotting.simple_barplot() when defining the title of the plot.

    Returns:
        :return Information regarding aspects in a pandas DataFrame
    """
    aspects = pd.DataFrame()

    aspects["abbr"] = pd.Series(["mar", "pts", "orb", "drb", "acc", "a/t"])
    aspects["full"] = pd.Series([
        "Winning / losing margins for all games in the season",
        "Total points scored in the season",
        "Total number of offensive rebounds in the season",
        "Total number of defensive rebounds in the season",
        "Shooting accuracy in the season",
        "Total number of assists vs turnovers in the season"
    ])
    aspects["plot title"] = pd.Series([full[:-14] for full in aspects["full"]])
    aspects["short"] = pd.Series([
        "margins",
        "points",
        "offensive rebounds",
        "defensive rebounds",
        "accuracy",
        "assists/turnovers"
    ])
    aspects["file title"] = pd.Series([s.replace(" ", "_").replace("/", "_") for s in aspects["short"]])
    aspects["corresponding cols"] = pd.Series([
        ["<doesn't apply>"],
        ["PTS"],
        ["ORB"],
        ["DRB"],
        ["3P%", "2P%", "FT%"],
        ["AST", "TOV"]
    ])
    aspects["availability"] = pd.Series([1947, 1947, 1974, 1974, 1980, 1974])

    aspects = aspects.set_index("abbr")

    return aspects


def abbreviations():
    """
    Returns the abbreviations used on bbref for the different teams. All caps
    entries enable case insensitive 'teams' input ('teams' input will match
    regardless of case when also converted to all caps).
    Taken from
    https://github.com/sherpan/bbref_team_game_logs/blob/master/README.md

    Returns:
        :return Dictionary with team names (keys) and corresponding
                abbreviations (values)
    """
    abbr = {
        "ATLANTA HAWKS" : "ATL",
        "ST. LOUIS HAWKS" : "SLH",
        "MILWAUKEE HAWKS" : "MIL",
        "TRI-CITIES BLACKHAWKS" : "TRI",
        "BOSTON CELTICS" : "BOS",
        "BROOKLYN NETS" : "BRK",
        "NEW JERSEY NETS" : "NJN",
        "CHICAGO BULLS" : "CHI",
        "CHARLOTTE HORNETS" : "CHO",
        "CHARLOTTE BOBCATS" : "CHA",
        "CLEVELAND CAVALIERS" : "CLE",
        "DALLAS MAVERICKS" : "DAL",
        "DENVER NUGGETS" : "DEN",
        "DETROIT PISTONS" : "DET",
        "FORT WAYNE PISTONS" : "FWP",
        "GOLDEN STATE WARRIORS" : "GSW",
        "SAN FRANCISCO WARRIORS" : "SFW",
        "PHILADELPHIA WARRIORS" : "PHW",
        "HOUSTON ROCKETS" : "HOU",
        "INDIANA PACERS" : "IND",
        "LOS ANGELES CLIPPERS" : "LAC",
        "SAN DIEGO CLIPPERS" : "SDC",
        "BUFFALO BRAVES" : "BUF",
        "LOS ANGELES LAKERS" : "LAL",
        "MINNEAPOLIS LAKERS" : "MIN",
        "MEMPHIS GRIZZLIES" : "MEM",
        "VANCOUVER GRIZZLIES" : "VAN",
        "MIAMI HEAT" : "MIA",
        "MILWAUKEE BUCKS" : "MIL",
        "MINNESOTA TIMBERWOLVES" : "MIN",
        "NEW ORLEANS PELICANS" : "NOP",
        "NEW ORLEANS/OKLAHOMA CITY HORNETS" : "NOK",
        "NEW ORLEANS HORNETS" : "NOH",
        "NEW YORK KNICKS" : "NYK",
        "OKLAHOMA CITY THUNDER" : "OKC",
        "SEATTLE SUPERSONICS" : "SEA",
        "ORLANDO MAGIC" : "ORL",
        "PHILADELPHIA 76ERS" : "PHI",
        "SYRACUSE NATIONALS" : "SYR",
        "PHOENIX SUNS" : "PHO",
        "PORTLAND TRAIL BLAZERS" : "POR",
        "SACRAMENTO KINGS" : "SAC",
        "KANSAS CITY KINGS" : "KCK",
        "KANSAS CITY-OMAHA KINGS" : "KCK",
        "CINCINNATI ROYALS" : "CIN",
        "ROCHESTER ROYALS" : "ROR",
        "SAN ANTONIO SPURS" : "SAS",
        "TORONTO RAPTORS" : "TOR",
        "UTAH JAZZ" : "UTA",
        "NEW ORLEANS JAZZ" : "NOJ",
        "WASHINGTON WIZARDS" : "WAS",
        "WASHINGTON BULLETS" : "WAS",
        "CAPITAL BULLETS" : "CAP",
        "BALTIMORE BULLETS" : "BAL",
        "CHICAGO ZEPHYRS" : "CHI",
        "CHICAGO PACKERS" : "CHI",
        "ANDERSON PACKERS" : "AND",
        "CHICAGO STAGS" : "CHS",
        "INDIANAPOLIS OLYMPIANS" : "IND",
        "SHEBOYGAN RED SKINS" : "SRS",
        "ST. LOUIS BOMBERS" : "STB",
        "WASHINGTON CAPITOLS" : "WAS",
        "WATERLOO HAWKS" : "WAT"
    }
    return abbr


def scrape_season_stats(season):
    """
    Scrapes the total season statistics for all teams who participated. This is
    used not only in sourcing.get_season_stats(), but also in
    query_io.get_query() to verify that all queried teams participated in the
    queried season.

    Args:
        season (int): The queried season

    Returns:
        :return Total season statistics (all teams, all aspects) in a pandas
                DataFrame
    """
    season_stats = pd.DataFrame()

    url = f"https://www.basketball-reference.com/leagues/{'NBA' if season > 1949 else 'BAA'}_{season}.html"
    tables = list(pd.read_html(url))   # get all tables on the specified webpage
    # find the table containing total season statistics
    for table in tables:
        try:
            # the NBA record for points in a single game is just below 200 - we
            # can use this for identifying the table containing total stats
            if any(score > 200 for score in table["PTS"]):
                season_stats = table
                break
        except KeyError:
            # if the table does not even have a "PTS" column, it is not the one
            # we are looking for
            pass

    # preprocessing steps needed in both sourcing.get_season_stats() and
    # query_io.get_query():
    # removing asterisk from team name where necessary
    for teamname in season_stats["Team"]:
        if teamname[-1] == "*":
            teamname_clean = teamname[:-1]
            season_stats.loc[season_stats["Team"] == teamname, "Team"] = teamname_clean

    return season_stats
