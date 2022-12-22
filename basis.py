#python3 -m pip install

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import pyarrow
import openpyxl

fileName = r"dataset.xlsx"
#fileName = r"smallData.xlsx"
featherFilePath = "./featherData.ftr"


class DataFrameProcessing:
    _currentDataFrame = pd.DataFrame()
    def __init__(self):
        self.dataset = pd.read_feather(featherFilePath, columns=None, use_threads=True)
        self.dataset["Scheduled start"] = self.dataset["Scheduled start"].astype('datetime64[ns]')
        self._currentDataFrame = self.dataset

    @property
    def currentDataFrame(self):
        return self._currentDataFrame
    
    @currentDataFrame.setter
    def currentDataFrame(self, new):
        self._currentDataFrame = new
        
    @staticmethod
    def excelToFeather(fileName):
        currentDataFrame = pd.read_excel(fileName)
        currentDataFrame = currentDataFrame.astype("category")
        currentDataFrame.to_feather(featherFilePath)

    def setCurrentDataFrameBasedOnCondition(self, condition, column = "Scheduled start"):
        self.currentDataFrame = self.currentDataFrame[
            self.currentDataFrame[column].apply(
                lambda var : eval(condition)
            )
        ]


class data(DataFrameProcessing):

    def __init__(self):
        super().__init__()

    def groupCountPlot(self, groupby, get):
        self._currentDataFrame.groupby(groupby).count().get(get).plot(kind = "bar", x = groupby, y = get)

    def columnsVersusBasedOnFrequency(self, indexColumn, column, throwawayColumn = "Order"):
        groupedData = self._currentDataFrame.groupby([indexColumn, column]).count().get(throwawayColumn).reset_index()

        result = pd.DataFrame()
        result[indexColumn] = groupedData.get(indexColumn).unique()

        groupedData.set_index(indexColumn, inplace= True)
        result.set_index(indexColumn, inplace= True)

        for obj in groupedData[column].unique():
            result[obj] = groupedData[groupedData.get(column) == obj].get(throwawayColumn)

        return result

    


test = data()
dataset = test.dataset
test.setCurrentDataFrameBasedOnCondition("var.year >= 2018")
test.currentDataFrame


plt.show()

#data.excelToFeather(fileName)


