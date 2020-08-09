#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is python file as part of Assignment 1 – PS3 - [India Census]
"""

__author__ = "Amar Joshi, KUSAM PHANI SINDHU, SAI CHANDRA SEKHAR MBRNV - Group 219"
__version__ = "0.1.0"
__license__ = "MIT"

import pandas as pd
import os
from datetime import datetime

class Census():
    """
    A class used to represent an Census data
    ...
    Attributes
    ----------
    input_file : str
        a formatted string for input file name that contains census data
    prompts_file : str
        a formatted string for prompts file name that contains what data is required
    output_file: str
        a formatted string for output_file name to print required data
    dict_noOfBirth : dict
        a dict to hold no. of births per year from census data
    dict_noOfDeaths : dict
        a dict to hold no. of deaths per year from census data
    dict_noOfDeaths : dict
        a dict to hold no. of persons alive from census data

    Methods
    -------
    readInputData()
        Reads data from file and creates relevant dictionaries containing data and number of records
        in that file
    readFromPromptsFile()
        Reads data from prompts file and print relevant data
    countBorn(dict_no_of_birth, year)
        Returns a formatted string with number of births in that year
    countDied(dict_no_of_birth, year)
        Returns a formatted string with number of deaths in that year
    maxPop(dict_no_of_alive)
        Returns a formatted string, the year of maximum population
    minPop(dict_no_of_alive, year)
        Returns a formatted string, the year of least population
    maxBirth(dict_no_of_birth, year)
        Returns a formatted string, the year with max number of births
    maxDeath(dict_no_of_death, year)
        Returns a formatted string, the year with max number of deaths
    printOutput(stringToPrint)
        Writes the formatted string to output file
    """

    def __init__(self, input_file, prompts_file, output_file):
        """
        :param input_file: str
            a formatted string for input file name that contains census data
        :param prompts_file:
            a formatted string for prompts file name that contains what data is required
        :param output_file:
            a formatted string for output_file name to print required data
        """
        self.input_file = input_file
        self.prompts_file = prompts_file
        self.output_file = output_file
        self.dict_noOfBirth = {}
        self.dict_noOfDeaths = {}
        self.dict_noOfAlive = {}


    def readInputData(self):
        """
        Reads data from file and creates relevant dictionaries containing data
        :return: int
            number of records in the file
        """
        try:
            # reading input file and creating dataframe
            df = pd.DataFrame()
            with open(self.input_file) as f:
                for line in f:
                    lsplit = line.split(",")
                    dateOfBirth = lsplit[2]
                    sp = pd.Series(lsplit)
                    dateOfDeath = lsplit[3]
                    # print(dateOfDeath)
                    d2 = {'ID': pd.Series(sp[0]),
                          'Name': pd.Series(sp[1]),
                          'Date of Birth': pd.Series(sp[2]),
                          'Date of Death': pd.Series(sp[3]),
                          'YrOfBirth': pd.Series(dateOfBirth.split("-")[2])}
                    if len(dateOfDeath.strip()) > 0:
                        d2['YrOfDeath'] = pd.Series(dateOfDeath.split("-")[2].strip())
                    df_temp = pd.DataFrame(data=d2)
                    df = df.append(df_temp, sort=False)

            if df.empty:
                return 0
            else:
                minYrOfBirth = df['YrOfBirth'].min()
                maxYrOfBirth = df['YrOfBirth'].max()

                c = 0
                for yr in range(int(minYrOfBirth), int(maxYrOfBirth) + 1, 1):
                    c = list(df['YrOfBirth']).count(str(yr))
                    self.dict_noOfBirth[str(yr)] = c

                maxYrOfDeath = df.iloc[:, 5].dropna().max()
                minYrOfDeath = df.iloc[:, 5].dropna().min()

                d = 0
                for yr in range(int(minYrOfDeath), int(maxYrOfDeath) + 1, 1):
                    d = list(df.iloc[:, 5]).count(str(yr))
                    self.dict_noOfDeaths[str(yr)] = d

                minYear = min(minYrOfBirth, minYrOfDeath)
                maxYear = max(maxYrOfBirth, maxYrOfDeath)

                sum = 0
                for yr in range(int(minYear), int(maxYear) + 1, 1):
                    sum = sum + self.dict_noOfBirth.get(str(yr), 0) - self.dict_noOfDeaths.get(str(yr), 0)
                    self.dict_noOfAlive[str(yr)] = sum

                return df.shape[0]
        except FileNotFoundError as fnf_error:
            self.printOutput(fnf_error)
        except AssertionError as error:
            self.printOutput(error)


    def readFromPromptsFile(self):
        """
            Reads data from prompts file and print relevant data
        """
        try:
            with open(self.prompts_file) as g:
                for line in g:
                    key = line.split(":")[0].strip().upper()
                    value = line.split(":")[1].strip()

                    # To find number of people died in given year
                    if key == "bornin".upper():
                        str_to_print = self.countBorn(self.dict_noOfBirth, value)
                        self.printOutput(str_to_print)

                    # To find number of people died in given year
                    if key == "diedin".upper():
                        str_to_print = self.countDied(self.dict_noOfDeaths, value)
                        self.printOutput(str_to_print)

                    # To find year with max population
                    if key == "maxPopulation".upper():
                        str_to_print = self.maxPop(self.dict_noOfAlive)
                        self.printOutput(str_to_print)

                    # To find year with min population
                    if key == "minPopulation".upper():
                        str_to_print = self.minPop(self.dict_noOfAlive)
                        self.printOutput(str_to_print)

                    # To find year with max birth
                    if key == "maxBirth".upper():
                        str_to_print = self.maxBirth(self.dict_noOfBirth)
                        self.printOutput(str_to_print)

                    # To find year with max deaths
                    if key == "maxDeath".upper():
                        str_to_print = self.maxDeath(self.dict_noOfDeaths)
                        self.printOutput(str_to_print)
        except FileNotFoundError as fnf_error:
            self.printOutput(fnf_error)
        except AssertionError as error:
            self.printOutput(error)

    def countBorn(self, dict_no_of_birth, year):
        """
        :param dict_no_of_birth: dict
        :param year: str
        :return: str
            Returns a formatted string with number of births in that year
        """
        return "No. of people born in {}: {}".format(year, str(
            dict_no_of_birth.get(year, "Data for this year not available")))

    def countDied(self, dict_no_of_deaths, year):
        """

        :param dict_no_of_deaths: dict
        :param year: str
        :return: str
            Returns a formatted string with number of deaths in that year
        """
        return "No. of people died in {}: {}".format(year, str(
            dict_no_of_deaths.get(year, "Data for this year not available")))

    def maxPop(self, dict_no_of_alive):
        """
        :param dict_no_of_alive: dict
        :return: str
            Returns a formatted string, the year of maximum population
        """
        v = list(dict_no_of_alive.values())
        popMax = max(v)
        k = list(dict_no_of_alive.keys())
        yearMax = k[v.index(popMax)]

        return "Maximum population was in {} with {} people alive".format(yearMax, popMax)

    def minPop(self, dict_no_of_live):
        """
        :param dict_no_of_live: dict
        :return: str
            Returns a formatted string, the year of least population
        """
        v = list(dict_no_of_live.values())
        popMin = min(v)
        k = list(dict_no_of_live.keys())
        yearMin = k[v.index(popMin)]

        return "Minimum population was in {} with {} people alive".format(yearMin, popMin)

    def maxBirth(self, dict_no_of_birth):
        """
        :param dict_no_of_birth: dict
        :return: str
            Returns a formatted string, the year with max number of births
        """
        v = list(dict_no_of_birth.values())
        birthMax = max(v)
        k = list(dict_no_of_birth.keys())
        yearMaxbirth = k[v.index(birthMax)]

        return "Maximum births were in {} with {} people born".format(yearMaxbirth, birthMax)

    def maxDeath(self, dict_no_of_death):
        """
        :param dict_no_of_death: dict
        :return: str
            Returns a formatted string, the year with max number of deaths
        """
        v = list(dict_no_of_death.values())
        deathMax = max(v)
        k = list(dict_no_of_death.keys())
        yearMaxDeath = k[v.index(deathMax)]

        return "Maximum deaths were in {} with {} people dead".format(yearMaxDeath, deathMax)

    def printOutput(self, stringToPrint=""):
        """
        Writes the formatted string to output file
        :param stringToPrint: str
        """
        with open(self.output_file, 'a+') as j:
            j.write("\n" + stringToPrint)


"""
    Change the filename/s if necessary and check the output
"""
dir_path = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(dir_path, "inputPS3.txt")
prompts_file = os.path.join(dir_path, "promptsPS3.txt")
output_file = os.path.join(dir_path, "outputPS3.txt")
dateTimeObj = datetime.now()
timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
census = Census(input_file=input_file, prompts_file=prompts_file, output_file=output_file)
census.printOutput("\nRunning census assignment PS3 by Group 219 on {}".format(timestampStr))
total_records = census.readInputData()
census.printOutput("{} records captured".format(total_records))
if total_records > 0:
    census.readFromPromptsFile()
else:
    census.printOutput("Cannot perform any analysis since there are no records in input file")


