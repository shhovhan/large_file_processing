import logging
import dask.dataframe as dk

logger = logging.getLogger(__name__)


class LargeCSVProcessor:
    """
    Class to process lar    ge CSV files.

    This class provides functionality for processing CSV files in Python.
    """
    def __init__(self, input_file, output_file='output.csv'):
        """
        Initialize the CSVProcessor instance.

        Parameters:
        input_file (str): The path to the input CSV file.
        output_file (str, optional): The path to the output CSV file. Default is 'output.csv'.
        """
        self.df = None
        self.input_file = input_file
        self.output_file = output_file

    def process_data(self):
        """
        Process the CSV data.

        This method reads the data from the input CSV file, processes it, and writes the processed data
        into a new CSV file.

        Parameters: None
        Returns: None
        """
        logger.info(f'Start processing of CSV data.')
        logger.info(f'Reading data from {self.input_file}')

        df = dk.read_csv(self.input_file)
        result = df.groupby(['Song', 'Date'])['Number of Plays'].sum().reset_index()\
            .rename(columns={'Number of Plays': 'Total Number of Plays for Date'})
        result.to_csv(self.output_file, index=False, single_file=True)

        logger.info(f'CSV data processing completed!')
        logger.info(f'Output csv file has been created: {self.input_file}')
