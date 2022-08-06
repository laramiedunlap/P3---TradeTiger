import pandas as pd
import time
from datetime import datetime
def list_to_string(inputList):
    outString = ""
    count = 0
    limit = len(inputList)-1
    for item in inputList:
        if type(item) == datetime:
            outString += item.strftime("%m/%d/%Y, %H:%M:%S")
        else:
            outString += str(item)
        outString
        if (count < limit):
            outString += ", "
        count+=1
    return outString

def string_to_list_end_dateTime(inputString):
    # splitList = inputString.split(", ")
    # outList = []
    # for item in splitList:
    #     if (item != splitList[len(splitList)-1]):
    #         outList.append(item)
    #     else:
    #         outList.append(pd.to_datetime(item))
    # return outList
    return inputString.split(", ")

def input_date_string(date):
    """
    Converts a date string to a unix timestamp int
    """
    return int(time.mktime(pd.to_datetime(date).timetuple()))