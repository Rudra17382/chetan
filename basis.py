import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
class data:
    #fileName = r"dataset.xlsx"
    fileName = r"smallData.xlsx"
    def __init__(self):
        self.dataset = pd.read_excel(self.fileName)

    def groupCountPlot(self, groupby, get):
        self.dataset.groupby(groupby).count().get(get).plot(kind = "bar", x = groupby, y = get)

    def addColumnBasedOnCondition(self, columnName, condition, columnToApplyConditionOn):
        self.dataset[columnName] = self.dataset.get(columnToApplyConditionOn).apply(condition)

    def columnsVersusBasedOnFrequency(self, indexColumn, column, throwawayColumn = "Order"):
        groupedData = self.dataset.groupby([indexColumn, column]).count().get(throwawayColumn).reset_index()

        result = pd.DataFrame()
        result[indexColumn] = groupedData.get(indexColumn).unique()

        groupedData.set_index(indexColumn, inplace= True)
        result.set_index(indexColumn, inplace= True)

        for obj in groupedData[column].unique():
            result[obj] = groupedData[groupedData.get(column) == obj].get(throwawayColumn)

        result.plot(kind = "bar")


test = data()
dataset = test.dataset

#test.columnsVersusBasedOnFrequency("Functional Location", "Order Type")
#test.columnsVersusBasedOnFrequency("Functional Location", "Manufacturer")
#test.columnsVersusBasedOnFrequency("Manufacturer", "Functional Location")
#test.columnsVersusBasedOnFrequency("Functional Location", "Cause Code Text")
#test.columnsVersusBasedOnFrequency("Functional Location", "Activity Text")
#test.columnsVersusBasedOnFrequency("Discipline", "Functional Location")
#test.columnsVersusBasedOnFrequency("Cause Code Text", "Activity Text")

plt.show()