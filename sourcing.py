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
        :return All and only the required data in a pandas DataFrame, as well as
                an updated list of teams from which all teams for which no or
                not enough data is available have been removed.
    """
    aspect, teams, season = query

    if aspect == "mar":
        data, teams_updated = get_margins(teams, season)
    else:
        data, teams_updated = get_season_stats(aspect, teams, season)

    if not teams_updated:
        print("\nNo data available for visualization. Terminating program.\n")
        quit()

    return data, teams_updated


def get_margins(teams, season):
    """
    For each of the queried teams, this function scrapes the points scored by
    the team and its opponent in all matches the team played in the queried
    season, and then processes these points to obtain the winning/losing
    margins. The margins are then further processed to obtain smoothed margins
    for improved legibility. NaNs are handled.

    Args:
        teams (list): The queried teams
        season (int): The queried season

    Returns:
        :return Margins and smoothed margins for all teams in a pandas
                DataFrame, as well as an updated list of teams from which all
                teams for which not enough data is available have been removed.
    """
    data_all_teams = pd.DataFrame()
    teams_to_be_removed = []

    for team in teams:
        # scrape data from bbref
        url = f"https://www.basketball-reference.com/teams/{team}/{season}_games.html"
        data_team = list(pd.read_html(url))[0]  # read in HTML table as DataFrame

        # drop rows that don't contain game results
        data_team = data_team[data_team["G"] != "G"]

        data_team["margin"] = np.subtract(
            pd.to_numeric(data_team["Tm"]),   # from 'team' points,
            pd.to_numeric(data_team["Opp"])   # subtract opponent points
        )
        # if not at least 75% of values are non-NaNs, do not consider this team
        if not (data_team["margin"].count() > (3/4 * data_team["margin"].size)):
            print(f"Too many missing values for {team}.")
            teams_to_be_removed.append(team)
            continue

        data_team["smoothed"] = ndimage.gaussian_filter1d(data_team["margin"], sigma=3)
        data_team = data_team.set_index("G")

        # append to main data frame
        data_all_teams[f"{team}_margin"] = data_team["margin"]
        data_all_teams[f"{team}_smoothed"] = data_team["smoothed"]

    teams_updated = teams
    for team in teams_to_be_removed:
        teams_updated.remove(team)

    return data_all_teams, teams_updated


def get_season_stats(aspect, teams, season):
    """
    Scraping average season statistics and preprocessing them according to the
    queried aspect and teams.

    Args:
        aspect (str): Aspect to be visualized
        teams (list): The queried team(s)
        season (int): The queried season

    Returns:
        :return Data required for visualizing 'aspect' in a pandas DataFrame, as
                well as an updated list of teams from which all teams for which
                no data is available have been removed.
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
    season_stats = season_stats[utils.aspects().loc[aspect, "corresponding cols"]]

    # remove all teams for which at least one value is missing
    season_stats = season_stats.dropna(how="any")

    teams_updated = teams
    for team in teams:
        # if the team's row was removed by dropna
        if not team in season_stats.index:
            print(f"Data missing for {team}.")
            teams_updated.remove(team)

    return season_stats, teams_updated
