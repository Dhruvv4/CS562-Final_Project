# This is a helper file which includes all helper functions for the project.

def readFile(path: str):
    # Read the file of path provided and return the contents
    with open(path, 'r') as f:
        return f.read()


def readFileByLines(path: str):
    # Read the file by lines of path provided and return the contents
    with open(path, 'r') as f:
        return f.readlines()

def writeFile(path: str, data):
    # Write contents to the file
    with open(path, 'w') as f:
        f.write(data)
    print(f'Data successfully written to {path}')

def groupingVariables(number):
    return ": " + ", ".join([chr(i + 64) for i in range(1, number + 1)])

def getMaxOf(data):
    # Data should be a list to iterate and perform math 'max' operation
    return max(data)

def getMinOf(data):
    # Data should be a list to iterate and perform math 'min' operation
    return min(data)

def getSumOf(data):
    # Data should be a list to iterate and perform math 'sum' operation
    return sum(data)

def getAvgOf(data):
    # Data should be a list to iterate and perform math 'avg' operation
    return getSumOf(data) / len(data)

def isString(string):
    # Validation function to check if the passed argument is a string
    return type(string) == str and len(string.strip()) > 0

def isStringArray(stringArray):
    # Validation function to check if the passed argument is a string array
    return type(stringArray) == list and len(stringArray) > 0

def isNumber(number):
    # Validation function to check if the passed argument is a number/integer
    return type(number) == int