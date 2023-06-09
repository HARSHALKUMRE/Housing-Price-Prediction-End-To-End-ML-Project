import os, sys
import pandas as pd
import numpy as np
from housing.constant import *
from housing.logger import logging
from housing.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact
from housing.exception import HousingException
from datetime import date
from collections import namedtuple
from housing.config.configuration import Configuration
from housing.components.data_ingestion import DataIngestion
from housing.components.data_validation import DataValidation
from housing.components.data_transformation import DataTransformation
from housing.components.model_trainer import ModelTrainer
from housing.components.model_evaluation import ModelEvaluation

class TrainingPipeline():
    def __init__(self, config: Configuration = Configuration())->None:
        try:
            self.config = config
        except Exception as e:
            raise HousingException(e,sys) from e  
        
    def start_data_ingestion(self)-> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config= self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise HousingException(e,sys) from e  
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            data_validation = DataValidation(
                data_validation_config = self.config.get_data_validation_config(), 
                data_ingestion_artifact = data_ingestion_artifact
            )
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise HousingException(e, sys) from e  

    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact,
                                  data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            data_transformation = DataTransformation(
                data_transformation_config=self.config.get_data_transformation_config(), 
                data_ingestion_artifact=data_ingestion_artifact, 
                data_validation_artifact=data_validation_artifact
            )
            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise HousingException(e, sys) from e 
        
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(
                model_trainer_config=self.config.get_model_trainer_config(), 
                data_transformation_artifact=data_transformation_artifact
            )
            return model_trainer.initiate_model_trainer()
        except Exception as e:
            raise HousingException(e, sys) from e   

    def start_model_evaluation(self, data_ingestion_artifact: DataIngestionArtifact,
                               data_validation_artifact: DataValidationArtifact,
                               model_trainer_artifact: ModelTrainerArtifact) -> ModelEvaluationArtifact:
        try:
            model_evaluate = ModelEvaluation(
                model_evaluation_config=self.config.get_model_evaluation_config(),
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact,
                model_trainer_artifact=model_trainer_artifact)
            return model_evaluate.initiate_model_evaluation()
        except Exception as e:
            raise HousingException(e, sys) from e

    def run_pipeline(self):
        try:
            # Data Ingestion
            data_ingestion_artifact = self.start_data_ingestion()

            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)

            data_transformation_artifact = self.start_data_transformation(
                data_ingestion_artifact=data_ingestion_artifact, 
                data_validation_artifact=data_validation_artifact
            )

            model_trainer_artifact = self.start_model_trainer(
                data_transformation_artifact=data_transformation_artifact
            )

            model_evaluation_artifact = self.start_model_evaluation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact,
                model_trainer_artifact=model_trainer_artifact
            )
        except Exception as e:
            raise HousingException(e,sys) from e  
