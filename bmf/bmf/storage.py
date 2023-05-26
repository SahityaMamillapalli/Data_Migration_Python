from typing import Callable
import pandas as pd
from bmf.bmf.logging import logger


class Storage():

    @classmethod
    def read(cls, filepath: str, **kwargs) -> pd.DataFrame:
        """Read a table into a dataframe

        Parameters
        ----------
        filepath : str
            The path to the file.

        Returns
        -------
        pd.DataFrame
            The loaded table
        **kwargs
            Extra arguments parsed to the reader
        """

        ext = filepath.split('.')[-1]
        read = cls._get_reader(ext)

        logger.info(f'Reading file {filepath} with extension {ext}')

        return read(filepath, **kwargs)

    @classmethod
    def _get_reader(cls, ext: str) -> Callable:

        logger.info(f"Class name -> {__name__}.{__class__.__name__} Method name is ->{cls._get_reader.__name__ }")
        logger.info(f'extension is : {ext}')
        if ext in ['xlsx', 'xls']:
            return pd.read_excel
        elif ext == 'csv':
            return pd.read_csv
        elif ext == 'parquet':
            return pd.read_parquet
        else:
            logger.error(f"Don't know how to read file with extension [{ext}]")
            raise ValueError(f"Don't know how to read file with extension [{ext}]")

    @classmethod
    def write(cls, df: pd.DataFrame, filepath: str, **kwargs) -> None:
        """Write a dataframe to file

        Parameters
        ----------
        df : pd.DataFrame
            The df to write
        filepath : str
            The location to save df
        **kwargs
            Extra arguments parsed to the writer
        """
        logger.info(f"Class name -> {__name__}.{__class__.__name__} Method name is ->{cls.write.__name__}")

        ext = filepath.split('.')[-1]
        logger.info(f'extension is : {ext}')

        if ext in ['xlsx', 'xls']:
            df.to_excel(filepath, index=False, **kwargs)
        elif ext == 'csv':
            df.to_csv(filepath, index=False, **kwargs)
        elif ext == 'parquet':
            df.to_parquet(filepath, **kwargs)
        else:
            logger.error(f"Error occurred because the extension is -> {ext}]")
            raise ValueError(f"Don't know how to write file with extension [{ext}]")

