import pandas as pd
from typing import List

# Define helper functions
def get_transition_tuples(ls: List[float]) -> List[tuple[float, float]]:
    """Converts a time series into a list of transition tuples"""
    
    return [(ls[i-1], ls[i]) for i in range(1, len(ls))]

def get_transition_event(tup) -> str:
    """Converts a tuple into a discrete transition event"""

    return "up" if tup[0] < tup[1] else "down"

# Read in whole data set

def read_time_series_data(path: str) -> tuple[pd.DataFrame, List[str]]:
    """Function to read in a time-series data set in .csv form"""

    df: pd.DataFrame = pd.read_csv(path)
    dropped_df: pd.DataFrame = df.dropna(how='all', axis='columns')
    renamed_df: pd.DataFrame = dropped_df.rename(columns=lambda col: col.lower().replace(" ", "_"))
    indexed_df: pd.DataFrame = renamed_df.set_index("month")

    column_names = indexed_df.columns.values.tolist()

    return indexed_df, column_names

def get_means_and_std_devs(df: pd.DataFrame) -> tuple[List[float], List[float]]:
    """Function to get means and std devs for a DataFrame"""

    means_list: List[float] = []
    std_devs_list: List[float] = []

    for column in df:
        means_list.append(df[column].mean())
        std_devs_list.append(df[column].std())
    
    return means_list, std_devs_list

def convert_columns_to_lists(df: pd.DataFrame) -> List[List[float]]:
    
    columns_list: List[List[float]] = []
    for column in df:
        columns_list.append(df[column].tolist())
    
    return columns_list

def get_iterations(initial_dfs_list: List[pd.DataFrame], rnorm_transition_dfs_list: List[pd.DataFrame], num_iterations: int) -> List[List[pd.DataFrame]]:

    i: int = 0;
    iterations_lists: List[List[pd.DataFrame]] = [[] for _ in initial_dfs_list]

    while i < num_iterations:

        future_dfs_list = [initial_df.dot(rnorm_transition_dfs_list[index]) for index, initial_df in enumerate(initial_dfs_list)]

        for iterations_list, df in zip(iterations_lists, future_dfs_list):
            iterations_list.append(df)
        
        initial_dfs_list = future_dfs_list
        i+=1
    
    return iterations_lists

def calculate_markovs(file_path: str, num_iterations: int) -> tuple[List[float], List[float], dict[str, List[pd.DataFrame]]]:
    """Function to read in a .csv time-series dataset and calculate the forward iterations n-steps ahead"""

    # Read in data
    data_set_df: pd.DataFrame
    column_names: List[str]
    data_set_df, column_names = read_time_series_data(file_path)

    # Get means and std_devs
    means_list: List[float]
    std_devs_list: List[float]
    means_list, std_devs_list = get_means_and_std_devs(data_set_df)

    # Pick out each time series as its own list
    column_lists: List[List[float]] = convert_columns_to_lists(data_set_df)

    # Derive single-step state transition tuples
    transitions_list: List[List[tuple[float, float]]] = [get_transition_tuples(x) for x in column_lists]

    # Convert raw time series data into discrete events
    events_list: List[List[str]] = [[get_transition_event(tup) for tup in x] for x in transitions_list]
    event_transitions_list: List[List[tuple[str, str]]] = [get_transition_tuples(x) for x in events_list]

    # Initialize Markov transition matrices with zeros
    ls_index: List[str] = ["up", "down"]
    transition_dfs_list: List[pd.DataFrame] = [pd.DataFrame(0, index=ls_index, columns=ls_index) for _ in column_lists]

    # Derive transition matrices
    for index, transition_df in enumerate(transition_dfs_list):
        for j, k in event_transitions_list[index]:
            transition_df[k][j] += 1  # Update k-th column and j-th row for i-th matrix
            
    #  Derive row-normalized transition matrix:
    # - Elements are normalized by row sum (fill NAs/NaNs with 0s)
    # - df.sum(axis=1) sums up each row, df.div(..., axis=0) then divides each column element
    rnorm_transition_dfs_list: List[pd.DataFrame] = [df.div(df.sum(axis=1), axis=0).fillna(0.00) for df in transition_dfs_list]

    # Grab the initial states from the earlier data
    initial_dfs_list: List[pd.DataFrame] = [pd.DataFrame({"up": [int(events[-1] == "up")], "down": [int(events[-1] == "down")]}) for events in events_list]

    # Use the transition matrix to project n steps ahead in time (n months)
    future_dfs_list: List[List[pd.DataFrame]] = get_iterations(initial_dfs_list, rnorm_transition_dfs_list, num_iterations)

    # Return a dictionary with column names and series evolutions
    future_dfs_dict: dict[str, List[pd.DataFrame]] = {column_name: future_df for column_name, future_df in zip(column_names, future_dfs_list)}

    return means_list, std_devs_list, future_dfs_dict