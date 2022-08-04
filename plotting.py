import utils
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def visualize(data, query):
    """
    Calls the plotting function that corresponds to the queried 'aspect', and
    returns the resulting plot.

    Args:
        data (DataFrame): All and only the data required for visualization
        query (list): Queried aspect, team(s), and season

    Returns:
        :return Plot as a matplotlib Figure
    """
    aspect, teams, season = query

    plt.style.use("fivethirtyeight")

    if aspect == "mar":
        plot = lineplot(data, teams, season)
    elif aspect == "a/t":
        plot = scatterplot(data, teams, season)
    elif aspect == "acc":
        plot = grouped_barplot(data, teams, season)
    else:
        plot = simple_barplot(aspect, data, teams, season)

    return plot


def lineplot(data, teams, season):
    """
    Visualizes winning/losing margins in a lineplot.

    Args:
        data (DataFrame): Winning/losing margins for all games in the season
        teams (list): The queried team(s)
        season (int): The queried season

    Returns:
        :return Plot as a matplotlib Figure
    """
    fig, ax = plt.subplots()

    for team in teams:
        # plot margins & smoothed margins in the same color
        team_color = next(ax._get_lines.prop_cycler)['color']
        # plot margins
        data[f"{team}_margin"].plot(  # may raise a KeyError
            ax=ax,
            color=team_color,
            linewidth=2,
            alpha=0.2,
            label=team
        )
        # plot smoothed margins
        data[f"{team}_smoothed"].plot(
            ax=ax,
            color=team_color,
            linewidth=3,
            linestyle="dashed",
            label=f"{team} smooth"
        )

    ax.axhline(y=0, color="dimgray", linewidth=1)
    plt.grid(axis="x")
    ax.legend();
    ax.set(
        ylabel = "Winning / Losing Margin (points)",
        xlabel = "Game No.",
        title = f"Winning / losing margins for all games in {'NBA' if season >= 1950 else 'BAA'} season {season-1}/{season}"
    )

    fig.set_size_inches(16, 9)

    return fig


def scatterplot(data, teams, season):
    """
    Visualizes assists and turnovers in a scatterplot.

    Args:
        data (DataFrame): Winning/losing margins for all games in the season
        teams (list): The queried team(s)
        season (int): The queried season

    Returns:
        :return Plot as a matplotlib Figure
    """
    fig, ax = plt.subplots()

    ax.scatter(data["AST"], data["TOV"], s=200)
    for team in teams:
        ax.annotate(
            text=team,
            # the data point to annotate:
            xy=(data.loc[team, "AST"], data.loc[team, "TOV"]),
            # where to insert the text relative to xy:
            xytext=(15, -5),
            # specify that the xytext value is given in pixels, not axis values:
            textcoords="offset pixels",
            fontsize="large"
        )

    ax.set(
        xlabel="Assists",
        ylabel="Turnovers",
        title = f"Average Number of Assists vs Turnovers in {'NBA' if season >= 1950 else 'BAA'} season {season-1}/{season}"
    )
    fig.set_size_inches(10,10)

    return fig


def grouped_barplot(data, teams, season):
    """
    Visualizes accuracy regarding 3- and 2-point-shots as well as free throws
    in a grouped bar plot.

    Args:
        data (DataFrame): Winning/losing margins for all games in the season
        teams (list): The queried team(s)
        season (int): The queried season

    Returns:
        :return Plot as a matplotlib Figure
    """
    fig, ax = plt.subplots()

    bars_roots = np.arange(len(teams))
    width = 0.22

    # each of the three following variables contains one bar for each team
    bars_3P = ax.bar(
        bars_roots - width,
        data["3P%"],
        width,
        label="3-Point-Shots"
    )
    bars_2P = ax.bar(
        bars_roots,
        data["2P%"],
        width,
        label="2-Point-Shots"
    )
    bars_FT = ax.bar(
        bars_roots + width,
        data["FT%"],
        width,
        label="Free Throws"
    )

    ax.bar_label(bars_3P, padding=5)
    ax.bar_label(bars_2P, padding=5)
    ax.bar_label(bars_FT, padding=5)
    ax.set_title(f"Shooting Accuracy in {'NBA' if season >= 1950 else 'BAA'} season {season-1}/{season}")
    ax.set_ylabel("Accuracy")
    ax.set_xticks(bars_roots, teams)
    ax.legend(loc=4)
    plt.grid(axis="x")
    fig.set_size_inches(len(teams)*4, 7)

    return fig


def simple_barplot(aspect, data, teams, season):
    """
    Visualizes 'aspect' in a bar plot.

    Args:
        aspect (str): The queried aspect
        data (DataFrame): Winning/losing margins for all games in the season
        teams (list): The queried team(s)
        season (int): The queried season

    Returns:
        :return Plot as a matplotlib Figure
    """
    fig, ax = plt.subplots()

    bars = ax.bar(teams, data[aspect.upper()], width=0.8)
    ax.bar_label(bars, padding=3, fontsize="large")

    # adapt range of y-axis for legibility / discriminability:
    if len(teams) > 1:
        low = np.min(data.values)
        high = np.max(data.values)
        ax.set_ylim([
            np.ceil(low-0.6*(high-low)),
            np.ceil(high+0.4*(high-low))
        ])
    else:
        ax.set_ylim([
            np.ceil(data.values - 0.6*(data.values/10)),
            np.ceil(data.values + 0.4*(data.values/10))
        ])

    # set y axis label and plot title depending on aspect
    aspect_variants = utils.aspects().loc[aspect]
    ax.set(
        ylabel=aspect_variants["short"],
        title=f"{aspect_variants['plot title']} in {'NBA' if season >= 1950 else 'BAA'} season {season-1}/{season}"
    )

    plt.grid(axis="x")
    fig.set_size_inches(len(teams)*1.5, 3)

    return fig
