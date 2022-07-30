def list_to_string(inputList):
    outString = ""
    for item in inputList:
        if type(item) == datetime:
            outString += int(time.mktime(item.timetuple()))
        else:
            outString += str(item)
        outString
        if (item != inputList[len(inputList)-1]):
            outString += ", "
    return outString

def string_to_list_end_dateTime(inputString):
    splitList = inputString.split(", ")
    outList = []
    for item in splitList:
        if (item != splitList[len(splitList)-1]):
            outList.append(float(item))
        else:
            outList.append(pd.to_datetime(item, unit='s'))
    return outList