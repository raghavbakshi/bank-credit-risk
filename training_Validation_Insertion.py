from Training_Raw_data_validation.rawValidation import Prediction_Data_Validation
from DataTypeValidation_Insertion_Training.DataTypeValidation import DataBaseOperation
from DataTransform_Training.DataTransformation import dataTransform
from logger_class.logger_class_file import logger

class train_validation:
    def __init__(self, path):
        self.raw_data = Prediction_Data_Validation(path)
        self.dataTransform = dataTransform()
        self.dBOperation = DataBaseOperation()
        self.file_object = open("Training_Logs/Training_Main_Log.txt", 'a+')
        self.log_writer = logger()

    def train_validation(self):
        try:

            self.log_writer.log(self.file_object, 'Start of Validation on files!!')
            # validating filename of prediction files
            self.raw_data.validationFileNameRaw()

            # extracting values from prediction schema
            column_names, no_of_columns = self.raw_data.valuesFromSchema()

            # validating column length in the file
            self.raw_data.validateColumnLength(no_of_columns)

            # validating if any column has all values missing
            self.raw_data.validateMissingValuesInWholeColumn()
            self.log_writer.log(self.file_object, "Raw Data Validation Complete!!")
            self.log_writer.log(self.file_object, "Starting Data Transformation!!")

            # replacing blanks in the csv file with "Null" values to insert in table
            self.dataTransform.replace_missing_with_null_and_add_serial_number()
            self.log_writer.log(self.file_object, "DataTransformation Completed!!!")
            self.log_writer.log(self.file_object, "Creating Training_Database and tables on the basis of given schema!!!")

            # create database with given name, if present open the connection! Create table with columns given in schema
            self.dBOperation.create_table()
            self.log_writer.log(self.file_object, "Table creation Completed!!")
            self.log_writer.log(self.file_object, "Insertion of Data into Table started!!!!")

            # insert csv files in the table
            self.dBOperation.insertIntoTableGoodData()
            self.log_writer.log(self.file_object, "Insertion in Table completed!!!")
            self.log_writer.log(self.file_object, "Deleting Good Data Folder!!!")

            # Delete the good data folder after loading files in table
            self.raw_data.delete_Existing_GoodData_Training_Folder()
            self.log_writer.log(self.file_object, "Good_Data folder deleted!!!")
            self.log_writer.log(self.file_object, "Moving bad files to Archive and deleting Bad_Data folder!!!")

            # Move the bad files to archive folder
            self.raw_data.moveBadFilesToArchiveBad()
            self.log_writer.log(self.file_object, "Bad files moved to archive!! Bad folder Deleted!!")
            self.log_writer.log(self.file_object, "Validation Operation completed!!")
            self.log_writer.log(self.file_object, "Extracting csv file from table")

            # export data in table to csvfile
            self.dBOperation.selectingDatafromtableintocsv()
            self.file_object.close()

        except Exception as e:
            raise e









