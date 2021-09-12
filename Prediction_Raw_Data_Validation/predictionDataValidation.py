from datetime import datetime
import os
import json
import shutil
import pandas as pd
from logger_class.logger_class_file import logger
import os
from os import listdir

class Prediction_Data_validation:
    """
               This class is used for handling all the validation done on the Raw Prediction Data!!.

               Written By: Raghav Bakshi
               Version: 1.0
               Revisions: None

               """

    def __init__(self, path):
        self.Batch_Directory = path
        self.schema_path = 'schema_prediction.json'
        self.logger = logger()


    def valuesFromSchema(self):
        """
                                Method Name: valuesFromSchema
                                Description: This method extracts all the relevant information from the pre-defined "Schema" file.
                                Output: column_names, Number of Columns
                                On Failure: Raise ValueError,KeyError,Exception

                                 Written By: Raghav Bakshi
                                Version: 1.0
                                Revisions: None

                                        """
        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                f.close()
            col_name = dic['col_name']
            no_of_columns = dic['no_of_columns']

            file = open("Prediction_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            message ='"NumberofColumns::{}'.format(no_of_columns)
            self.logger.log(file, message)

            file.close()



        except ValueError:
            file = open("Prediction_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, "ValueError:Value not found inside schema_prediction.json")
            file.close()
            raise ValueError

        except KeyError:
            file = open("Prediction_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, "KeyError:Key value error incorrect key passed")
            file.close()
            raise KeyError

        except Exception as e:
            file = open("Prediction_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, str(e))
            file.close()
            raise e

        return col_name, no_of_columns




    def createDirectoryForGoodBadRawData(self):

        """
                                        Method Name: createDirectoryForGoodBadRawData
                                        Description: This method creates directories to store the Good Data and Bad Data
                                                      after validating the prediction data.

                                        Output: None
                                        On Failure: OSError

                                         Written By: Raghav Bakshi
                                        Version: 1.0
                                        Revisions: None

                                                """
        try:
            path = os.path.join("Prediction_Raw_Files_Validated/", "Good_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join("Prediction_Raw_Files_Validated/", "Bad_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)

        except OSError as ex:
            file = open("Prediction_Logs/GeneralLog.txt", 'a+')
            self.logger.log(file, "Error while creating Directory %s:" % ex)
            file.close()
            raise OSError

    def deleteExistingGoodDataTrainingFolder(self):
        """
                                            Method Name: deleteExistingGoodDataTrainingFolder
                                            Description: This method deletes the directory made to store the Good Data
                                                          after loading the data in the table. Once the good files are
                                                          loaded in the DB,deleting the directory ensures space optimization.
                                            Output: None
                                            On Failure: OSError

                                             Written By: Raghav Bakshi
                                            Version: 1.0
                                            Revisions: None

                                                    """
        try:
            path = 'Prediction_Raw_Files_Validated/'
            if os.path.isdir(path + 'Good_Raw/'):
                shutil.rmtree(path + 'Good_Raw/')
                file = open("Prediction_Logs/GeneralLog.txt", 'a+')
                self.logger.log(file, "GoodRaw directory deleted successfully!!!")
                file.close()
        except OSError as s:
            file = open("Prediction_Logs/GeneralLog.txt", 'a+')
            self.logger.log(file, "Error while Deleting Directory : %s" %s)
            file.close()
            raise OSError
    def deleteExistingBadDataTrainingFolder(self):

        """
                                            Method Name: deleteExistingBadDataTrainingFolder
                                            Description: This method deletes the directory made to store the bad Data.
                                            Output: None
                                            On Failure: OSError

                                             Written By: Raghav Bakshi
                                            Version: 1.0
                                            Revisions: None

                                                    """

        try:
            path = 'Prediction_Raw_Files_Validated/'
            if os.path.isdir(path + 'Bad_Raw/'):
                shutil.rmtree(path + 'Bad_Raw/')
                file = open("Prediction_Logs/GeneralLog.txt", 'a+')
                self.logger.log(file,"BadRaw directory deleted before starting validation!!!")
                file.close()
        except OSError as s:
            file = open("Prediction_Logs/GeneralLog.txt", 'a+')
            self.logger.log(file,"Error while Deleting Directory : %s" %s)
            file.close()
            raise OSError

    def moveBadFilesToArchiveBad(self):


        """
                                            Method Name: moveBadFilesToArchiveBad
                                            Description: This method deletes the directory made  to store the Bad Data
                                                          after moving the data in an archive folder. We archive the bad
                                                          files to send them back to the client for invalid data issue.
                                            Output: None
                                            On Failure: OSError

                                             Written By: Raghav Bakshi
                                            Version: 1.0
                                            Revisions: None

                                                    """
        now = datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")
        try:
            path = "PredictionArchivedBadData"
            if not os.path.isdir(path):
                os.makedirs(path)
            source = 'Prediction_Raw_Files_Validated/Bad_Raw/'
            dest = 'PredictionArchivedBadData/BadData_' + str(date)+"_"+str(time)
            if not os.path.isdir(dest):
                os.makedirs(dest)
            files = os.listdir(source)
            if len(files) != 0:
                for f in files:
                    if f not in os.listdir(dest):
                        shutil.move(source + f, dest)           # files moved from bad data folder to archived bad data
                file = open("Prediction_Logs/GeneralLog.txt", 'a+')
                self.logger.log(file, "Bad files moved to archive")
                path = 'Prediction_Raw_Files_Validated/'
                if os.path.isdir(path + 'Bad_Raw/'):            # files deleted from bad data folder
                    shutil.rmtree(path + 'Bad_Raw/')
                self.logger.log(file, "Bad Raw Data Folder Deleted successfully!!")
                file.close()
            else:
                file = open("Prediction_Logs/GeneralLog.txt", 'a+')
                path = 'Prediction_Raw_Files_Validated/'
                if os.path.isdir(path + 'Bad_Raw/'):  # files deleted from bad data folder
                    shutil.rmtree(path + 'Bad_Raw/')
                self.logger.log(file, "Bad Raw Data Folder Deleted successfully!!")
                file.close()

        except OSError as e:
            file = open("Prediction_Logs/GeneralLog.txt", 'a+')
            self.logger.log(file, "Error while moving bad files to archive:: %s" % e)
            file.close()
            raise OSError





    def validateColumnLength(self,NumberofColumns):
        """
                    Method Name: validateColumnLength
                    Description: This function validates the number of columns in the csv files.
                                 It is should be same as given in the schema file.
                                 If not same file is not suitable for processing and thus is moved to Bad Raw Data folder.
                                 If the column number matches, file is kept in Good Raw Data for processing.

                     Output: None
                    On Failure: Exception

                     Written By: Raghav Bakshi
                    Version: 1.0
                    Revisions: None

             """
        try:
            f = open("Prediction_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Column Length Validation Started!!")
            for file in os.listdir('Prediction_Raw_Files_Validated/Good_Raw/'):
                df = pd.read_csv("Prediction_Raw_Files_Validated/Good_Raw/" + file)
                if df.shape[1] == NumberofColumns:
                    #df.to_csv("Prediction_Raw_Files_Validated/Good_Raw/" + file, index=None, header=True)
                    self.logger.log(f, "Column Length Validation Completed!!")
                    pass
                else:
                    shutil.move("Prediction_Raw_Files_Validated/Good_Raw/" + file, "Prediction_Raw_Files_Validated/Bad_Raw")
                    self.logger.log(f, "Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)


        except OSError:
            f = open("Prediction_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Error Occured while moving the file :: %s" % OSError)
            f.close()
            raise OSError
        except Exception as e:
            f = open("Prediction_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Error Occured:: %s" % e)
            f.close()
            raise e

        f.close()

    def deletePredictionFile(self):

        """
                            Method Name: deletePredictionFile
                            Description: This function deletes the prediction files
                             Output: None
                            On Failure: Exception

                             Written By: Raghav Bakshi
                            Version: 1.0
                            Revisions: None

                     """

        if os.path.exists('Prediction_Output_File/Predictions.csv'):
            os.remove('Prediction_Output_File/Predictions.csv')

    def validateMissingValuesInWholeColumn(self):
        """
                                  Method Name: validateMissingValuesInWholeColumn
                                  Description: This function validates if any column in the csv file has all values missing.
                                               If all the values are missing, the file is not suitable for processing.
                                               SUch files are moved to bad raw data.
                                  Output: None
                                  On Failure: Exception

                                   Written By: Raghav Bakshi
                                  Version: 1.0
                                  Revisions: None

                              """
        try:
            f = open("Prediction_Logs/missingValuesInColumn.txt", 'a+')
            self.logger.log(f, "Missing Values Validation Started!!")

            for file in os.listdir('Prediction_Raw_Files_Validated/Good_Raw/'):
                df = pd.read_csv("Prediction_Raw_Files_Validated/Good_Raw/" + file)
                count = 0
                for columns in df:
                    if (len(df[columns]) - df[columns].count()) == len(df[columns]):    # condition to check whether all values are missing or not
                        count += 1
                        shutil.move("Prediction_Raw_Files_Validated/Good_Raw/" + file,
                                    "Prediction_Raw_Files_Validated/Bad_Raw")
                        self.logger.log(f, "Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)
                        break
                if count == 0:

                    df.to_csv("Prediction_Raw_Files_Validated/Good_Raw/" + file, index=None, header=True)
                    self.logger.log(f, "Missing Values Validation Complete!!")
        except OSError:
            f = open("Prediction_Logs/missingValuesInColumn.txt", 'a+')
            self.logger.log(f, "Error Occured while moving the file :: %s" % OSError)
            f.close()
            raise OSError
        except Exception as e:
            f = open("Prediction_Logs/missingValuesInColumn.txt", 'a+')
            self.logger.log(f, "Error Occured:: %s" % e)
            f.close()
            raise e
        f.close()

    def validationFileNameRaw(self):
        """
                    Method Name: validationFileNameRaw
                    Description: This function validates the name of the training csv files as per given name in the schema!
                    Output: None
                    On Failure: Exception

                     Written By: Raghav Bakshi
                    Version: 1.0
                    Revisions: None

                """

        self.deleteExistingBadDataTrainingFolder()
        self.deleteExistingGoodDataTrainingFolder()
        # create new directories
        self.createDirectoryForGoodBadRawData()
        onlyfiles = [f for f in os.listdir(self.Batch_Directory)]
        try:
            f = open("Prediction_Logs/nameValidationLog.txt", 'a+')
            for filename in onlyfiles:
                if (filename == "SouthGermanCredit.csv"):

                    shutil.copy("Prediction_Batch_files/" + filename, "Prediction_Raw_Files_Validated//Good_Raw")
                    self.logger.log(f, "Valid File name!! File moved to GoodRaw Folder :: %s" % filename)

                else:
                    shutil.copy("Prediction_Batch_files/" + filename, "Prediction_Raw_Files_Validated/Bad_Raw")
                    self.logger.log(f, "Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)

            f.close()

        except Exception as e:
            f = open("Prediction_Logs/nameValidationLog.txt", 'a+')
            self.logger.log(f, "Error occured while validating FileName %s" % e)
            f.close()
            raise e










