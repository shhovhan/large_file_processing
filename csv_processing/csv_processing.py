import dask.dataframe as dk
import logging

logging.basicConfig(level=logging.INFO)


class LargeCSVProcessor:
    """
    Class to read large csv files, process data and write into new file.
    To create instance of this class, filepath should be passed to the constructor of class.
    It will write output data in output_<input_file>.csv file
    """
    def __init__(self, input_file, output_file='output.csv'):
        self.df = None
        self.input_file = input_file
        self.output_file = output_file

    def process_data(self):
        logging.info(f'Start processing of CSV data.')
        logging.info(f'Reading data from {self.input_file}')

        df = dk.read_csv(self.input_file)
        result = df.groupby(['Song', 'Date'])['Number of Plays'].sum().reset_index()\
            .rename(columns={'Number of Plays': 'Total Number of Plays for Date'})
        result.to_csv(self.output_file, index=False, single_file=True)

        logging.info(f'CSV data processing completed!')
        logging.info(f'Output csv file has been created: {self.input_file}')
