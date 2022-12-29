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
        self.dataset["day"] = self.dataset["Scheduled start"].apply(lambda date : date.day)
        self.dataset["month"] = self.dataset["Scheduled start"].apply(lambda date : date.month)
        self.dataset["year"] = self.dataset["Scheduled start"].apply(lambda date : date.year)
        self.dataset["monthYear"] = self.dataset["month"].apply(str) + "/" + self.dataset["year"].apply(str)
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
test.setCurrentDataFrameBasedOnCondition("var.year >= 2022")

#test.currentDataFrame = test.currentDataFrame.groupby(["monthYear", "Critical"]).count()["Order"].reset_index()
#test.currentDataFrame["month"] = test.currentDataFrame["monthYear"].apply(lambda date : date.split("/")[0])
#test.currentDataFrame["year"] = test.currentDataFrame["monthYear"].apply(lambda date : date.split("/")[1])

print(test.columnsVersusBasedOnFrequency("monthYear", "Critical").sort_index(key= lambda index : index.map(lambda x : int(x.split("/")[0]))))
test.columnsVersusBasedOnFrequency("monthYear", "Critical").sort_index(key= lambda index : index.map(lambda x : int(x.split("/")[0]))).plot(kind= "bar")
print(test.currentDataFrame)
#test.currentDataFrame.plot(kind="bar")

plt.show()

#data.excelToFeather(fileName)


