from typing import Any
import re
import pandas as pd
from bmf.bmf.logging import logger

def insert(row: pd.Series, source: str, target: str) -> pd.Series:
    """Insert the source column into the target column

    Parameters
    ----------
    row : pd.Series
        A row of a dataframe
    source : str
        The name of the source column to insert from
    target : str
        The name of the target column to insert into

    Returns
    -------
    pd.Series
        The transformed row
    """
    # logger.info(f"Inserting the source column {source} data into target column {target}")
    row[target] = row[source]

    return row




def constant(row: pd.Series, target: str, value: Any) -> pd.Series:
    """Insert a constant column into the target column

    Parameters
    ----------
    row : pd.Series
        A row of a dataframe
    target : str
        The name of the target column to insert constant into
    value : Any
        The value to insert into the target column

    Returns
    -------
    pd.Series
        The transformed row
    """
    # logger.info(f"Insert a constant value -> {value} into the target column -> {target} ")
    row[target] = value
    return row


def replace_substring(
    row: pd.Series,
    source: str,
    target: str,
    old: str,
    new: str,
    regex: bool = False
) -> pd.Series:
    """Replace all occurrences of 'old' in the source column
    with 'new' and insert in the target column.

    Parameters
    ----------
    row : pd.Series
        A row of a dataframe
    source : str
        The name of the source column to replace values in
    target : str
        The name of the target column to insert constant into
    old : str
        The value to replace occurences of in substring
    new : Any
        The value to insert in substring instead
    regex : bool
        Whether the old value is a regex

    Returns
    -------
    pd.Series
        The transformed row
    """

    if regex:
        row[target] = re.sub(old, new, str(row[source]))
    else:
        row[target] = str(row[source]).replace(old, new)



    # replace backward slashes with forward slashes
    row[target] = row[target].replace("\\", "/")
    # Use regular expression to extract the desired part of the path
    if "/R&D/" in row[target]:
        match = re.search(r"/R&D/.*", row[target])
        if match:
            row[target] = match.group()
    elif "/CE/" in row[target]:
        match = re.search(r"/CE/.*", row[target])
        if match:
            row[target] = match.group()
    # Removing the Missing values and leave it as null.
    elif "Missing" in row[target]:
        row[target] = pd.NaT

    return row


def key_value_translate(
    row: pd.Series,
    source: str,
    target: str,
    translate_dict: dict
) -> pd.Series:
    """Key-value translate multiple values in a source column.

    Parameters
    ----------
    row : pd.Series
        A row of a dataframe
    source : str
        The name of the source column to replace values in
    target : str
        The name of the target column to insert constant into
    translate_dict : dict
        A dictionary to translate values

    Returns
    -------
    pd.Series
        The transformed row
    """
    if row[source] in translate_dict:
        row[target] = translate_dict[row[source]]
    return row

def concat(row: pd.Series, source: tuple, target: str) -> pd.Series:
    """Insert the source column into the target column

    Parameters
    ----------
    row : pd.Series
        A row of a dataframe
    source : str
        The list of the source columns to insert from
    target : str
        The name of the target column to insert into

    Returns
    -------
    pd.Series
        The transformed row

    """

    # concat the two columns data with .
    row[target] = f"{row[source[0]]}.{row[source[1]]}"
    return row





transformation_functions = {
    'insert': insert,
    'constant': constant,
    'replace_substring': replace_substring,
    'key_value_translate': key_value_translate,
    'concat': concat
}
