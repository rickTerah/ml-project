import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass


@dataclass
class DataIngestionConfig():
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'raw.csv')


class DataIngestion():
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info('Entered data ingestion component')
        try:
            df = pd.read_csv('notebook/data/candidates.csv')
            logging.info('Read dataset as data frame')

            os.makedirs(os.path.dirname(
                self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,
                      index=False, header=True)
            logging.info('Train test split initiated')

            # train_set, test_set = train_test_split(
            #     df, train_size=0.2, random_state=42)
            # We don't have enough data to split into train and test
            train_set = pd.read_csv('notebook/data/candidates.csv')
            test_set = pd.read_csv('notebook/data/candidates.csv')

            train_set.to_csv(
                self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(
                self.ingestion_config.test_data_path, index=False, header=True)

            logging.info('Ingestion completed')
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
