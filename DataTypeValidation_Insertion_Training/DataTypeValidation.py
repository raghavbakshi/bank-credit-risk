import csv
import os
import shutil
from os import listdir
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from logger_class.logger_class_file import logger
import pandas as pd

cloud_config = {
    'secure_connect_bundle': r'C:\Users\Dell\Downloads\secure-connect-bank-credit-risk.zip'
}
auth_provider = PlainTextAuthProvider('fHexycrHjsiCJXrIaoiiCvAO',
                                      'ZDTs.yp6Udwscn+ww4zWNa7XC1pwrLc3DmsADE-1_3pJr77GY8_qHwbD54AhM3X'
                                      '+FIgGZFSxu6ZohUIkT-z+35fXvy3+g7hmvlZMLia7yMqbUrSgfTG0Z8FzJJO3bd0Z')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)


class DataBaseOperation:
    """
        This class is responsible to create all DB operations
        """

    def __init__(self):
        self.path = 'Training_Database/'
        self.badFilePath = "Training_Raw_files_validated/Bad_Raw"
        self.goodFilePath = "Training_Raw_files_validated/Good_Raw"
        self.logger = logger()

    def database_connection(self):
        """
            Method Name: databaseConnection
            Description: This method opens the database with the given name
            Output: Connection to the DB
            On Failure: Raise ConnectionError

            Written By: Raghav Bakshi
            Version: 1.0
            Revisions: None
            """

        try:

            session = cluster.connect()
            file = open('Training_Logs/DataBaseConnectionLog.txt', 'a+')
            self.logger.log(file, 'Connection established successfully')
            file.close()
        except ConnectionError:
            file = open('Training_Logs/DataBaseConnectionLog.txt', 'a+')
            self.logger.log(file, 'Error while establishing connection')
            file.close()
            raise ConnectionError

    def create_table(self):
        """


        Method Name: createTableDb
        Description: This method creates a table in the given database which will be used to insert the Good data after raw data validation.
        Output: None
        On Failure: Raise Exception

        Written By: Raghav Bakshi
        Version: 1.0
        Revisions: None
        """

        try:
            session = cluster.connect()
            for row in session.execute("SELECT keyspace_name, table_name FROM   system_schema.tables;"):
                if row[0] == "dataset":
                    if row[1] == "data":
                        file = open('Training_Logs/DbTableCreateLog.txt', 'a+')
                        self.logger.log(file, 'table created successfully')
                        file.close()
                        break
                    else:
                        session.execute(
                            "CREATE TABLE dataset.data(serial decimal PRIMARY KEY,status decimal, duration decimal, credit_history  decimal,purpose decimal, amount decimal, savings decimal, employment_duration decimal, installment_rate decimal, personal_status_sex decimal, other_debtors decimal, present_residence decimal, property decimal, age decimal, other_installment_plans decimal, housing decimal, number_credits decimal, job decimal, people_liable decimal, telephone decimal, foreign_worker decimal, credit_risk decimal);").one()
                        file = open('Training_Logs/DbTableCreateLog.txt', 'a+')
                        self.logger.log(file, 'table created successfully')
                        file.close()
                        break
        except Exception as e:
            file = open('Training_Logs/DbTableCreateLog.txt', 'a+')
            self.logger.log(file, 'Error while creating table')
            file.close()
            raise e

    def insertIntoTableGoodData(self):

        """
                               Method Name: insertIntoTableGoodData
                               Description: This method inserts the Good data files from the Good_Raw folder into the
                                            above created table.
                               Output: None
                               On Failure: Raise Exception

                                Written By: Raghav Bakshi
                               Version: 1.0
                               Revisions: None

        """
        try:
            session = cluster.connect()
            goodFilePath = self.goodFilePath
            badFilePath = self.badFilePath
            onlyfiles = [f for f in listdir(goodFilePath)]
            log_file = open("Training_Logs/DbInsertLog.txt", 'a+')
            count_file_row = 0
            for file in onlyfiles:
                try:

                    with open(goodFilePath + '/' + file, "r") as f:
                        next(f)
                        reader = csv.reader(f)

                        for line in reader:
                            count_file_row += 1
                            try:
                                variable = line
                                variable = str(variable)
                                variable = variable.replace('[', '')
                                variable = variable.replace(']', '')
                                variable = variable.replace("'", "")
                                query = "insert into dataset.data(serial,status, duration, credit_history ,purpose, " \
                                        "amount, savings, employment_duration, installment_rate, personal_status_sex, " \
                                        "other_debtors, present_residence, property, age, other_installment_plans, " \
                                        "housing, number_credits, job, people_liable, telephone, foreign_worker, " \
                                        "credit_risk) values({});".format(
                                    variable)
                                session.execute(query)

                            except Exception as e:
                                raise e
                    try:
                        for i in session.execute("SELECT Count(*) from dataset.data"):
                            count_database_row = i[0]
                    except Exception as e:
                        raise e
                    try:
                        if count_file_row == count_database_row:
                            self.logger.log(log_file, "File loaded successfully!!")
                    except Exception as e:
                        raise e
                except Exception as e:
                    self.logger.log(log_file, "Error while inserting in table")
                    shutil.move(goodFilePath + '/' + file, badFilePath)
                    self.logger.log(log_file, "File Moved Successfully %s" % file)
                    log_file.close()
                    raise e
            log_file.close()
        except Exception as e:
            raise e

    def selectingDatafromtableintocsv(self):

        """
                               Method Name: selectingDatafromtableintocsv
                               Description: This method exports the data in GoodData table as a CSV file. in a given location.
                                            above created .
                               Output: None
                               On Failure: Raise Exception

                                Written By: iNeuron Intelligence
                               Version: 1.0
                               Revisions: None

        """

        self.fileFromDb = 'Training_FileFromDB/'
        self.fileName = 'InputFile.csv'
        log_file = open("Training_Logs/ExportToCsv.txt", 'a+')
        session = cluster.connect()
        try:

            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            with open(self.fileFromDb + self.fileName, 'w') as csvFile:
                for column_name in session.execute("SELECT * FROM dataset.data;").column_names:
                    csvFile.writelines(column_name + ',')
                csvFile.writelines('\n')
                for i in session.execute("SELECT * FROM dataset.data;").all():
                    for j in i:
                        csvFile.writelines(str(j) + ',')
                    csvFile.writelines('\n')

            self.logger.log(log_file, "File exported successfully!!!")
            log_file.close()

        except Exception as e:
            self.logger.log(log_file, "File exporting failed. Error : %s" % e)
            log_file.close()
