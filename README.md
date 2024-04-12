# Exploration of Markov Chains on Decision Maker Panel data

This repo takes time-series data from Bank of England and Decision Maker Panel in order to construct a two-state Markov chain based on each category either increasing or decreasing in value from month to month.

dmp_downloader.py takes the month and year of interest, downloads the .xlsx file directly from source, and then processes it into .csv files that can be easily digested in Pandas to calculate the Markov chains by the next function.

markov_chains.py contains the necessary Python functions in Pandas to be able to construct the deltas from month-to-month, build the transition matrices for the chain, and then loop through a set number of iterations to build the state matrices, assuming an initial distribution based on the last month of the data.

output_writer.py takes the results of the previous and assembles them into a .xlsx file with one sheet per set of Markov chains, with the probabilities for both a single step and the stationary distribution reached after n-iterations.

orchestrator.ipynb ties this all together. This is for ease of use, but could also be turned into another script with a main() function to combine the previous steps into one.

requirements.txt contains the Python packages necessary to run the project in a virtual environment.

Can also run Markovs on any .csv file which contains time series data, as long as the time index column is called "time" as follows:
    `growth_means_dict, growth_std_devs_dict, growth_future_dfs_dict = calculate_markovs("growth_mar.csv", 10)`

One-step iteration data:
    `print(growth_future_dfs_dict["employment"][0])`

n-step iteration data (10 in this case):
    `growth_future_dfs_dict["employment"][-1]`
