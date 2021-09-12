import pandas as pd
from logger_class.logger_class_file import logger
import os

class DataTransformationPrediction:
    """
                      This class shall be used for transforming the Good Raw Training Data before loading it in Database!!.

                      Written By: Raghav Bakshi
                      Version: 1.0
                      Revisions: None

                      """

    def __init__(self):
        self.goodDataPath = "Prediction_Raw_Files_Validated/Good_Raw"
        self.logger = logger()

    def replace_missing_with_null_and_add_serial_number(self):

        """
            Replace missing values

            """
        log_file = open("Prediction_Logs/dataTransformLog.txt", 'a+')
        self.logger.log(log_file, "File Transformed started!!")

        try:

            files = [f for f in os.listdir(self.goodDataPath)]
            for file in files:
                df = pd.read_csv(self.goodDataPath + "/" + file)
                df = pd.DataFrame(df)
                df.fillna('NULL', inplace=True)

                """ 
                    Adding Serial Numbers
                        """

                lst = [i for i in range(1, df.shape[0] + 1)]
                df['serial'] = lst
                df = df.reindex(
                    columns=["serial", "status", "duration", "credit_history", "purpose", "amount", "savings",
                             "employment_duration", "installment_rate", "personal_status_sex", "other_debtors",
                             "present_residence", "property", "age", "other_installment_plans", "housing",
                             "number_credits", "job", "people_liable", "telephone", "foreign_worker"
                             ])
                df.to_csv(self.goodDataPath + "/" + file, header=True, index=False)
                self.logger.log(log_file, "File Transformed successfully!!")

        except Exception as e:
            self.logger.log(log_file, "Data Transformation failed ")
            log_file.close()
            raise e
        log_file.close()
