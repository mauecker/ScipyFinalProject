# Visualizing Basketball Statistics
Scientific Programming in Python • Final Project<br>
David Siecke, Madleen Uecker

## Overview
This is our final project for the course Scientific Programming in Python held in the summer term of 2022 at Osnabrück University.

The central functionality of this python module is scraping basketball data from [basketball-reference.com](basketball-reference.com) (a website that provides comprehensive statistics for NBA teams, seasons, and matches; from here on referred to as `bbref`) according to user specifications and visualizing it.

## Installation
To download the files, type the following into your terminal:

```
  git clone ...?
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
The further usage is explained in the terminal by the program itself.

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

### Options
