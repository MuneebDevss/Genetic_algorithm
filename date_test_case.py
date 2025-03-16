from utility_functions import is_valid_date
import random

class TestCase:
    def __init__(self, dateString, uniqueCasesCovered,duplicates, isValid):
        self.dateString = dateString
        self.uniqueCasesCovered = uniqueCasesCovered
        self.duplicates=duplicates
        self.isValid = isValid
def duplicates(testCases):
    duplicates=dict()
    for testCase in testCases:
        if testCase.dateString in duplicates:
            duplicates[testCase.dateString]=duplicates[testCase.dateString]+1
        else:
            duplicates[testCase.dateString]=1
    for testCase in testCases:
        testCase.duplicates=duplicates[testCase.dateString]

def unique_classes_covered(testCases):
    valid_equivalence_classes_covered = {
        "M1": False,  # [1, 3, 5, 7, 8, 10, 12]
        "M2": False,  # [4, 6, 9, 11]
        "M3": False,  # [2]
        "D1": False,  # 1 <= day <= 28
        "D2": False,  # [29]
        "D3": False,  # [30]
        "D4": False,  # [31]
        "Y1": False,  # Leap year
        "Y3": False   # 0 <= year <= 9999 and year % 4 != 0 (Normal year)
    }
    invalid_equivalence_classes_covered = {
        "M4": False,  # month < 1
        "M5": False,  # month > 12
        "D5": False,  # day < 1
        "D6": False,  # day > 31
        "Y4": False,  # year < 0
        "Y5": False   # year > 9999
    }
    for testCase in testCases:
        day = int(testCase.dateString[0:2])
        month = int(testCase.dateString[3:5])
        year = int(testCase.dateString[6:10])
        if testCase.isValid:
            if day>=1 and day<=28: 
                if not valid_equivalence_classes_covered["D1"]: 
                    valid_equivalence_classes_covered["D1"]=True 
                    testCase.uniqueCasesCovered+=1 
            elif day==29: 
                if not valid_equivalence_classes_covered["D2"]: 
                    valid_equivalence_classes_covered["D2"]=True 
                    testCase.uniqueCasesCovered+=1 
            elif day==30: 
                if not valid_equivalence_classes_covered["D3"]: 
                    valid_equivalence_classes_covered["D3"]=True 
                    testCase.uniqueCasesCovered+=1 
            elif day==31: 
                if not valid_equivalence_classes_covered["D4"]: 
                    valid_equivalence_classes_covered["D4"]=True 
                    testCase.uniqueCasesCovered+=1
            if month in [1, 3, 5, 7, 8, 10, 12]:
                if not valid_equivalence_classes_covered["M1"]:
                    valid_equivalence_classes_covered["M1"] = True
                    testCase.uniqueCasesCovered += 1
            elif month in [4, 6, 9, 11]:
                if not valid_equivalence_classes_covered["M2"]:
                    valid_equivalence_classes_covered["M2"] = True
                    testCase.uniqueCasesCovered += 1
            elif month == 2:
                if not valid_equivalence_classes_covered["M3"]:
                    valid_equivalence_classes_covered["M3"] = True
                    testCase.uniqueCasesCovered += 1

            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):  # Leap year
                if not valid_equivalence_classes_covered["Y1"]:
                    valid_equivalence_classes_covered["Y1"] = True
                    testCase.uniqueCasesCovered += 1
            else:
                if not valid_equivalence_classes_covered["Y3"]:
                    valid_equivalence_classes_covered["Y3"] = True
                    testCase.uniqueCasesCovered += 1
            

    else:
        if month < 1:
            if not invalid_equivalence_classes_covered["M4"]:
                invalid_equivalence_classes_covered["M4"] = True
                testCase.uniqueCasesCovered += 1
        elif month > 12:
            if not invalid_equivalence_classes_covered["M5"]:
                invalid_equivalence_classes_covered["M5"] = True
                testCase.uniqueCasesCovered += 1

        if day < 1:
            if not invalid_equivalence_classes_covered["D5"]:
                invalid_equivalence_classes_covered["D5"] = True
                testCase.uniqueCasesCovered += 1
        elif day > 31:
            if not invalid_equivalence_classes_covered["D6"]:
                invalid_equivalence_classes_covered["D6"] = True
                testCase.uniqueCasesCovered += 1

        if year < 0:
            if not invalid_equivalence_classes_covered["Y4"]:
                invalid_equivalence_classes_covered["Y4"] = True
                testCase.uniqueCasesCovered += 1
        elif year > 9999:
            if not invalid_equivalence_classes_covered["Y5"]:
                invalid_equivalence_classes_covered["Y5"] = True
                testCase.uniqueCasesCovered += 1

        


def print_test_cases(testCases):
    for testCase in testCases:
        print(f"Test Case: {testCase.dateString}, Unique Cases Covered: {testCase.uniqueCasesCovered}, is valid {testCase.isValid}" )


#function tp generate the population of dates
def populate():
    test_cases=[]
    for i in range(10):
        day = random.randint(0, 31)
        day = '0' + str(day) if day < 10 else str(day)
        month = random.randint(1, 12)
        month = '0'+str(month) if month < 10 else str(month)
        year = random.randint(0, 9999)
        year = ('0'*(4-len(str(year))))+str(year)
        if is_valid_date(f"{day}/{month}/{year}"):
            test_cases.append(TestCase(f"{day}/{month}/{year}",0, 0, True))
        else:
            test_cases.append(TestCase(f"{day}/{month}/{year}",0, 0, False))
    return test_cases

def main():
    testCases=populate()
    unique_classes_covered(testCases=testCases)
    duplicates(testCases=testCases)
    print_test_cases(testCases=testCases)

if __name__ == "__main__":
    main()

