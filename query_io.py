import utils
import pandas as pd
import matplotlib.pyplot as plt
import os


def get_query():
    """
    Gets information from user regarding which aspect to visualize, and from
    which season and which team(s) to source the corresponding data. This is
    achieved via a dialogue in the terminal.

    Returns:
        :return Aspect to visualize (str), season (int), and list of teams in a
                3-place list
    """

    # aspect
    print(
        """
        What aspect would you like to be visualized?
        Choose one of the following options:
        Type in:      Option:"""
    )
    # print all aspect options and their corresponding abbreviation:
    aspects = utils.aspects()
    for abbr in aspects.index:
        print("\t     ", abbr, "\t", aspects.loc[abbr, "full"])
    print("")   # one free line between options and input
    aspect = get_suitable_input("Aspect: ", required=(aspects))

    # season
    print(
        """\n
        From which season should the data be sourced?
        Please type in the year in which the season ended.
        For example, if you are interested in season 2021/22, type in:
            2022
        """
    )
    season = get_suitable_input("Ending year of season: ", required=(aspect, aspects))

    # team(s)
    print(
        """\n
        From which NBA team(s) should the data be sourced?
        Please type in for each team either the three-letter abbreviation or
        the official name. If you are interested in multiple teams,
        separate them by a comma. For example, if you are interested
        in Miami Heat and Dallas Mavericks, you can type in:
            MIA, Dallas Mavericks
        """
    )
    names_abbrs = utils.abbreviations()
    # flip the names_abbrs dictionary
    abbrs_names = dict((abbr, name) for (name, abbr) in names_abbrs.items())
    teams = get_suitable_input("Team(s): ", required=(season, abbrs_names, names_abbrs))

    # get a nicely legible string representation of all queried teams and their
    # respective abbreviation used by bbref
    teams_verbal_enum = ""
    for team in teams:
        if len(teams) > 1 and team == teams[-1]:
            # insert an "and" in front of the last team in the enumeration
            teams_verbal_enum += "and "
        # represent each team like this: "Full name (Abbreviation)"
        teams_verbal_enum += f"{abbrs_names[team]} ({team})"
        if len(teams) > 2 and team != teams[-1]:
            teams_verbal_enum += ", "
        elif len(teams) == 2 and team != teams[-1]:
            # ensuring that there is a blank space before the "and"
            teams_verbal_enum += " "

    print(f"\n\nVisualizing {aspects.loc[aspect, 'short']} data of {teams_verbal_enum} in {'NBA' if season >= 1950 else 'BAA'} season {season-1}/{season} ...\n")
    return [aspect, teams, season]


def get_suitable_input(category, required=None):
    """
    This function repeatedly asks the user to type in what is specified by
    'category' (an aspect, a season or team(s)) until the input satisfies the
    requirements corresponding to 'category' which are implemented in the body
    of the loop.

    Args:
        category (str): What the user is asked to type in (this determines the
                        requirements the input has to meet)
        required (tuple): Information that is required for checking whether the
                          requirements are satisfied

    Returns:
        :return A suitable input (list if category=="Team(s): ", str otherwise)
    """
    suitable_input = False
    while not suitable_input:
        inp = input(category)

        if category == "Aspect: ":
            aspects = required
            try:
                if not inp in aspects.index:
                    raise ValueError
            except ValueError:
                print("Please choose one of the options given above.")
            else:
                suitable_input = True

        elif category == "Ending year of season: ":
            aspect, aspects = required
            # season from which on data required for visualizing 'aspect'
            # is available:
            min_season = aspects.loc[aspect, "availability"]
            try:
                inp = int(inp)   # may raise a ValueError
                if not min_season <= inp <= 2022:
                    raise Exception
            except ValueError:
                print("Please make sure to type in the year in which the season ended.")
            except Exception:
                print(f"Data required for visualizing {aspects.loc[aspect, 'short']} is available from the season ending in {min_season} on, until the season ending in 2022.")
            else:
                suitable_input = True

        elif category == "Team(s): ":
            season, abbrs_names, names_abbrs = required
            # get all teams that participated in season, convert to all caps in
            # order to allow case insensitive input by ...
            possible_teams = utils.scrape_season_stats(season).set_index("Team").index.str.upper()

            # ... converting also the input to all caps
            inp = inp.upper().split(", ")
            to_be_removed = []
            # Here things get a bit complex. Essentially, what we are doing
            # here is checking whether the queried teams participated in the
            # queried season. We do this by comparing their full names to the
            # full names of those teams listed in the table containing total
            # season statistics.
            # If we compared the abbreviations, it could be that a team which
            # did actually participate in the queried season is rejected
            # because the dictionary we use (utils.abbreviations()) is not
            # complete and correct. (We elaborate on this in README.md.)
            # Evading this by comparing full team names requires one additional
            # step (converting abbreviations to full names and then back), but
            # also enables more precise and accurate feedback.
            for i, team in enumerate(inp):
                # convert abbreviations to full team names
                if len(team) == 3:
                    try:
                        inp[i] = abbrs_names[team]
                    except KeyError:
                        to_be_removed.append(team)
                        print(f"It seems that {team} is not used as an abbreviation for any team on BBREF.")
                        other_team = input("You can try the team's full name, specify another team, or just press enter: ").upper()
                        if other_team:
                            inp.append(other_team)
                        continue
                if not (inp[i] in possible_teams):
                    to_be_removed.append(inp[i])
                    print(f"It seems that '{inp[i]}' did not participate in NBA season {season-1}/{season}.")
                    other_team = input("Specify another team, or just press enter: ").upper()
                    if other_team:
                        inp.append(other_team)
                else:   # 'team' did participate in season
                    try:
                        # convert to abbreviation
                        inp[i] = names_abbrs[inp[i]]
                    except KeyError:
                        to_be_removed.append(inp[i])
                        print(f"Sorry, we do not know the abbreviation BBREF uses for '{inp[i]}'.")
                        other_team = input("Specify another team, or just press enter: ").upper()
                        if other_team:
                            inp.append(other_team)
            for team in to_be_removed:
                inp.remove(team)
            # if any teams are left by now, we do have suitable input
            if inp:
                suitable_input = True
                # remove duplicates while retaining order
                inp = list(dict.fromkeys(inp))
            else:
                print(f"\nNone of the queried teams participated in season {season-1}/{season}. Please choose a different set of teams.")

    return inp


def export(plot, query):
    """
    Save the plot to the current directory and print a corresponding
    notification.

    Args:
        plot (matplotlib Figure): The queried plot
        query (list): Queried aspect, teams, and season

    Return:
        :return None
    """
    aspect, teams, season = query

    current_dir = os.getcwd()
    folder = "visualizations"

    # create a folder 'visualizations' if it doesn't exist in the current dir
    if not os.path.isdir(f"{current_dir}/{folder}"):
        os.mkdir(f"{current_dir}/{folder}")

    # file name contains aspect, teams, and season
    filename = f"plot-{utils.aspects().loc[aspect, 'file title']}-{'_'.join(teams)}-{season-1}_{season}.png"
    path = f"{folder}/{filename}"

    plot.savefig(
        path,
        bbox_inches="tight"
    )
    print(f"""
        The plot can be found under
            {current_dir}/{folder}
        as
            {filename}
    """)
