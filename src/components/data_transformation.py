import sys
from dataclasses import dataclass


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', "preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        # This function returns the data transformer object
        pass

    def initiate_data_transformation(self, train_path, test_path):
        # If we need to transform the data, we can do it here
        pass
