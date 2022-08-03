import utils
import numpy as np
import pandas as pd
from scipy import ndimage


def get_data(query):
    """
    Depending on the queried 'aspect', this function calls different other
    functions which scrape the corresponding data and prepare it for plotting

    Args:
        query (list): Queried aspect, team(s), and season

    Returns:
        :return A tuple containing all and only the required data in a pandas
                DataFrame, as well as an updated list of teams from
                which all teams for which no data is available have been
                removed.
    """
    aspect, teams, season = query

    if aspect == "mar":
        data, teams_updated = get_margins(teams, season)
    else:
        data = get_season_stats(aspect, teams, season)
        # no need to update teams
        teams_updated = teams

    if data.empty:
        print("\nNo data available for visualization. Terminating program.\n")
        quit()

    return data, teams_updated


def get_margins(teams, season):
    """
    For each of the queried teams, this function scrapes the points scored by
    the team and its opponent in all matches the team played in the queried
    season, and then processes these points to obtain the winning/losing
    margins. The margins are then further processed to obtain smoothed margins
    for improved legibility.

    Args:
        teams (list): The queried teams
        season (int): The queried season

    Returns:
        :return A tuple containing margins and smoothed margins for all teams in
                a pandas DataFrame, as well as an updated list of teams from
                which all teams for which no data is available have been
                removed.
    """
    data_all_teams = pd.DataFrame()
    teams_to_be_removed = []

    for team in teams:
        # scrape data from bbref
        url = f"https://www.basketball-reference.com/teams/{team}/{season}_games.html"
        try:
            data_team = list(pd.read_html(url))[0]  # read in HTML table as DataFrame
        except Exception:
            print(f"Data required for computing margins not available for {team}")
            teams_to_be_removed.append(team)
            continue

        # drop rows that don't contain game results
        data_team = data_team[data_team["G"] != "G"]
        # further preprocessing
        data_team = data_team.set_index("G")
        data_team["margin"] = np.subtract(
            pd.to_numeric(data_team["Tm"]),   # from 'team' points,
            pd.to_numeric(data_team["Opp"])   # subtract opponent points
        )
        data_team["smoothed"] = ndimage.gaussian_filter1d(data_team["margin"], sigma=3)

        # append to main data frame
        data_all_teams[f"{team}_margin"] = data_team["margin"]
        data_all_teams[f"{team}_smoothed"] = data_team["smoothed"]

    teams_updated = teams
    for team in teams_to_be_removed:
        teams_updated.remove(team)

    return data_all_teams, teams_updated


def get_season_stats(aspect, teams, season):
    """
    Scraping total season statistics and preprocessing them according to the
    queried aspect and teams.

    Args:
        aspect (str): Aspect to be visualized
        teams (list): The queried team(s)
        season (int): The queried season

    Returns:
        :return Data required for visualizing 'aspect' in a pandas DataFrame
    """
    season_stats = utils.scrape_season_stats(season)

    # replacing team names by three-letter abbreviations
    abbr = utils.abbreviations()
    # (convert team names to all caps in order to suit the entries in 'abbr':)
    season_stats["Team"] = season_stats["Team"].str.upper()
    season_stats = season_stats.replace({"Team": abbr})

    season_stats = season_stats.set_index("Team")

    # subset rows according to queried teams
    season_stats = season_stats[season_stats.index.isin(teams)]

    # subset columns according to queried aspect
    season_stats = season_stats[utils.aspects().loc[aspect, "corresponding cols" ]]

    return season_stats
