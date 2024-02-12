# Exploration of Markov Chains on Decision Maker Panel data

This repo takes time-series data from Bank of England and Decision Maker Panel in order to construct a two-state Markov chain based on each category either increasing or decreasing in value from month to month.

dmp_downloader.py takes the month and year of interest, downloads the .xlsx file directly from source, and then processes it into .csv files that can be easily digested in Pandas to calculate the Markov chains by the next function.

markov_chains.py contains the necessary Python functions in Pandas to be able to construct the deltas from month-to-month, build the transition matrices for the chain, and then loop through a set number of iterations to build the state matrices, assuming an initial distribution based on the last month of the data.

orchestrator.ipynb is a Jupyter notebook with some driver code to show how these functions can be used. Data is returned as a dictionary so that outputs can be consumed as individual series (cell 4), or simply looped through to get the final iteration output for all series in the data (cell 5)
