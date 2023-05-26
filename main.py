import os, sys
import pandas as pd
import numpy as np
from housing.constant import *
from housing.logger import logging
from housing.exception import HousingException
from housing.pipeline.training_pipeline import TrainingPipeline

def main():
    try:
        pipeline = TrainingPipeline()
        pipeline.run_pipeline()
    except Exception as e:
        logging.error(f"{e}")

if __name__ == "__main__":
    main() 