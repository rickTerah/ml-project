import sys
import os
import json
import re
import pickle

from dataclasses import dataclass
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from src.exception import CustomException
from src.logger import logging

import pandas as pd


@dataclass
class ProcessPipelineConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', "encodings.pickle")


class ProcessPipeline:
    def __init__(self):
        self.data_transformation_config = ProcessPipelineConfig()

    # Extract relevant information on the candidates
    def extract_info(self, row):
        logging.info('Extracting information from the candidates')
        experiences_str = row['LI - List of Experience Information'].replace(
            'null', 'None')

        try:
            experiences = json.loads(
                experiences_str) if experiences_str != 'None' else []
        except json.JSONDecodeError:
            experiences = []

        titles = [exp['title'] for exp in experiences]
        description = [exp['description'] for exp in experiences]
        return titles, description

    def calculate_encodings(self, candidates):
        logging.info('Calculating encodings for the candidates')
        candidates[['Job Titles', 'Description']] = candidates.apply(
            lambda row: pd.Series(self.extract_info(row)), axis=1)
        candidates['inputCandidate'] = candidates.apply(lambda row: [re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', title + ' ' + description))
                                                                     if title is not None and description is not None else '' for title, description in zip(row['Job Titles'], row['Description'])], axis=1)

        model = SentenceTransformer('all-mpnet-base-v2')

        # Create a dictionary to store encodings for each candidate
        encoded_job_experience = {}

        # Get the unique vacancy titles from the DataFrame
        unique_titles = candidates['inputCandidate'].explode().unique()

        # Calculate and store encodings for each unique vacancy title with tqdm
        for title in tqdm(unique_titles, desc='Encoding Titles', unit='title'):
            if title is not None and isinstance(title, str) and title not in encoded_job_experience:
                encoding = model.encode([title], convert_to_tensor=True)
                encoded_job_experience[title] = encoding

        # Save the encoded jobtitles dictionary to a pickle file
        with open('artifacts/encodings.pickle', 'wb') as file:
            pickle.dump(encoded_job_experience, file)

    def initiate_data_processing(self):
        try:
            logging.info('Initiating data processing')
            candidates = pd.read_csv('notebook/data/candidates.csv')
            self.calculate_encodings(candidates)
            logging.info('Data processing completed')
        except Exception as e:
            logging.error('Error while processing data')
            raise CustomException(e, sys)
