# Visualizing Basketball Statistics
Scientific Programming in Python • Final Project<br>
David Siecke, Madleen Uecker

## Overview
This is our final project for the course Scientific Programming in Python held in the summer term of 2022 at Osnabrück University.

The central functionality of this python module is scraping basketball data from [basketball-reference.com](https://www.basketball-reference.com) (a website that provides comprehensive statistics for NBA teams, seasons, and matches; from here on referred to as `bbref`) according to user specifications and visualizing it.

## Installation
To download the files, type the following into your terminal:

```
  git clone https://github.com/madule/ScipyFinalProject.git
```

### Requirements
To run properly, besides [`python`](https://www.python.org) the module requires [`numpy`](https://numpy.org), [`pandas`](https://pandas.pydata.org), [`scipy`](https://scipy.org) and [`matplotlib`](https://matplotlib.org) installations.
If you have [`miniconda`](https://docs.conda.io/en/latest/miniconda.html) already installed, getting these packages is straightforward. Below are step-by-step instructions on the procedure.

It is recommended to create a conda environment before the installation; however this is optional.
```
  conda create -n my-env
  conda activate my-env
```
You can then install the required packages as follows:
```
  conda install numpy
  conda install pandas
  conda install scipy
  conda install matplotlib
```
## Usage
To run the code, you need to activate the conda environment within which you have installed the required packages.
```
  conda activate my-env
```
Then, you just need to navigate to the directory to which `git` saved the code files in this repository, and execute the `main.py` file.

```
  cd path/to/repository
  python main.py
```
The further usage is explained in the terminal by the program itself. Some example usages can be found in the accompanying `.ipynb files.

## Acknowledgements
Besides the creators of the libraries mentioned above, this project was enabled by
- the people who created and maintain [basketball-reference](https://www.basketball-reference.com)
- [@sherpan](https://github.com/sherpan) and [@smehta73](https://github.com/smehta73) on GitHub, who published an extensive [list of the team abbreviations used on bbref](https://github.com/sherpan/bbref_team_game_logs#basketball-reference-team-abbreviations)

## Structure
### Files
The module consists of five `.py`-files:
- `main.py`
- `query_io.py`
- `sourcing.py`
- `plotting.py`
- `utils.py`

The `main.py` file controls the overall procedure of the program. In order to do that, it calls functions from the `query_io.py`, `sourcing.py`, and `plotting.py` files. Functions that are needed by more than one of those latter three files are stored in `utils.py`.

The three files `query_io.py`, `sourcing.py`, and `plotting.py` hold the main functionality of the module. Each of them has a controlling function at the top, by means of which it interfaces to the `main.py` file. This controlling function then calls other functions within the same file or from `utils.py` which achieve the respectively desired goal.<br>
- `query_io.get_query()` organizes a terminal dialog to get the user's specifications regarding which aspect to visualize and what data to use to do so (which team(s)/season).
- `sourcing.get_data(query)` structures the process of scraping data from `bbref`and preprocessing it for visualization.
- `plotting.visualize(data, query)` decides which function to use for plotting based on the query, specifically the queried aspect.

`query_io.py` is an exception here, in the sense that it has a second function that is addressed in `main.py`, namely `query_io.export(plot, query)`, which exports the plot as a PNG file and prints a notification about the location of the directory to which the file has been saved.

All further information regarding the mechanics of the code can be found in the function docstrings.

### Options
Users can influence the functionality of the program by specifying
- one completed NBA season (1946/47 – 2021/22),
- one or multiple NBA teams, and
- one of the following aspects for visualization:
  - winning / losing margins for all games in the season (line plot)
  - total points scored in the season (bar plot)
  - total number of offensive rebounds in the season (bar plot)
  - total number of defensive rebounds in the season (bar plot)
  - shooting accuracy in the season (with respect to 3- and 2-point-shots as well as free throws, grouped bar plot)
  - total number of assists vs turnovers in the season (scatter plot)

## A note on operability
When querying certain teams, the program at the stage of webscraping prints the notification that the data required for visualization is not available on `bbref` for the queried team, while it actually is.<br>
This is due to the dictionary of team names and their corresponding abbreviation we used not being complete and correct. Unfortunately, the abbreviations `bbref` uses in some cases deviate from the official NBA abbreviations, and no table of team names and abbreviations is provided on `bbref`. The best approximation we could find was [this inofficial listing](https://github.com/sherpan/bbref_team_game_logs/blob/master/README.md#basketball-reference-team-abbreviations) on GitHub, however it is still not complete and does contain errors (we fixed those that we detected manually).<br>
However, in our tests we found that this affects mostly teams that are long defunct (since 1960 or so). For all teams who participated in more recent NBA seasons, our program works fine.

We tried to create our own listing of team names and abbreviations used on `bbref` by scraping Google search results for the term `f'site:https://www.basketball-reference.com/teams/ "{teamname}"'` using the [`googlesearch`](https://github.com/Nv7-GitHub/googlesearch) package, but had to figure out that Google does not like being scraped and returns an `HTTP 429 Too Many Requests` error in case of too many requests over a too short time period, which would be necessary to scrape the abbreviations for all NBA teams.

## Contact

Our StudIP handles are `dsiecke` and `mauecker`. Combine them with `@uos.de` to obtain our email addresses.
