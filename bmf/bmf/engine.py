"""
This is the Engine for creating transformations
"""
from typing import Dict
from tqdm import tqdm
from collections import OrderedDict
from bmf.bmf.storage import Storage
from bmf.bmf.functions import transformation_functions
import pandas as pd
from bmf.bmf.logging import logger


class TransformationEngine():

    def __init__(self, config: Dict):
        """Initialize with config

        Parameters
        ----------
        config : Dict
            The YAML configuration file as dict
        """

        self.input_path = config['input_file']
        self.output_path = config['output_file']

        # Taking the path of solution file and filter  from YAML configuration file

        self.solution_path = config['solution_file']
        self.filter = config.get('filter')
        self.transformations = config['transformations']

        logger.info(f'Input file path: {self.input_path}')
        logger.info(f'Output file path: {self.output_path}')
        logger.info(f'Solution file path: {self.solution_path}')
        logger.info(f'Transformations: {self.transformations}')
        logger.info(f'filter: {self.filter}')

    def run(self):
        """
        Transform the input based on the
        transformation rules from the config
        """

        df = Storage.read(self.input_path)
        logger.info(f'Reading input file : {self.input_path}')

        # Apply filter on data
        if self.filter:
            # query() method in Pandas is used to apply the filter condition to the dataframe.
            df = df.query(self.filter)
            logger.info(f'Applying filter: {self.filter}')

        for transformation in tqdm(self.transformations):

            logger.info(f'Transformation name: {transformation}')
            transformation_function = transformation_functions[transformation['action']]
            transformation.pop('action')

            df = df.apply(
                        transformation_function,
                        axis=1,
                        **transformation
                    )


        #We only keep the target columns in the output
        target_columns = [transformation.get('target')
                          for transformation in self.transformations
                          if transformation.get('target') is not None]
        unique_target_columns = list(OrderedDict.fromkeys(target_columns))
        logger.info(f'Unique target columns in output file : {unique_target_columns}')

        Storage.write(df[unique_target_columns], self.output_path)
        logger.info(f'Writing output file : {self.output_path}')

        """ 
        Checking the data validation for output.csv and solution.csv
        For Validation I have used the equals method, it will check the entire data frame for equality, including the column names, row indexes, and cell values. 
        This can help ensure that the output matches the expected solution file exactly.    
        """

        df1 = Storage.read(self.output_path)
        logger.info(f'For validation purpose reading output file : {self.output_path}')
        df2 = Storage.read(self.solution_path)
        logger.info(f'For validation purpose reading solution file : {self.solution_path}')
        if df1.equals(df2):
            logger.info(f'output file and solution file both are identical')
        else:
            logger.info(f'output file and solution file both are different')








