from utility_functions import is_valid_date
import random

class TestCase:
    def __init__(self, dateString, fitness, isValid):
        self.dateString = dateString
        self.fitness=fitness
        self.isValid = isValid

def fitness(testCases):
    eachTestCaseClassCoverage = []
    valid_equivalence_classes_covered = {
        "M1": 0,  # [1, 3, 5, 7, 8, 10, 12]
        "M2": 0,  # [4, 6, 9, 11]
        "M3": 0,  # [2]
        "D1": 0,  # 1 <= day <= 28
        "D2": 0,  # [29]
        "D3": 0,  # [30]
        "D4": 0,  # [31]
        "Y1": 0,  # Leap year
        "Y3": 0   # 0 <= year <= 9999 and year % 4 != 0 (Normal year)
    }
    invalid_equivalence_classes_covered = {
        "M5": 0,  # month > 12
        "D6": 0,  # day > 31
        "Y5": 0   # year > 9999
    }
    for testCase in testCases:
        day = int(testCase.dateString[0:2])
        month = int(testCase.dateString[3:5])
        year = int(testCase.dateString[6:10])
        classesCovered = []

        if testCase.isValid:
            if 1 <= day <= 28:
                classesCovered.append("D1")
            elif day == 29:
                classesCovered.append("D2")
            elif day == 30:
                classesCovered.append("D3")
            elif day == 31:
                classesCovered.append("D4")

            if month in [1, 3, 5, 7, 8, 10, 12]:
                classesCovered.append("M1")
            elif month in [4, 6, 9, 11]:
                classesCovered.append("M2")
            elif month == 2:
                classesCovered.append("M3")

            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):  # Leap year
                classesCovered.append("Y1")
            else:
                classesCovered.append("Y3")
        
        else:
            if month > 12:
                classesCovered.append("M5")
            if day > 31:
                classesCovered.append("D6")
                
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) and day == 29:
                classesCovered.append("Y5")
                
        eachTestCaseClassCoverage.append(classesCovered)
    
    for classesCovered in eachTestCaseClassCoverage:
        for classe in classesCovered:
            if classe in valid_equivalence_classes_covered:
                valid_equivalence_classes_covered[classe] += 1
            elif classe in invalid_equivalence_classes_covered:
                invalid_equivalence_classes_covered[classe] += 1

    
    for i in range(len(testCases)):
        valid_classes_covered = 0
        invalid_classes_covered = 0
        
        for classe in eachTestCaseClassCoverage[i]:
            if classe in valid_equivalence_classes_covered:
                valid_classes_covered += 1
            elif classe in invalid_equivalence_classes_covered:
                invalid_classes_covered += 1
        total_classes_covered = valid_classes_covered + invalid_classes_covered
        testCases[i].fitness = len(eachTestCaseClassCoverage[i]) / (1 + total_classes_covered)

def isUniqueClass(equivalence_classes_covered,key,uniqueClassesCovered):

    if not equivalence_classes_covered[key]: 
        equivalence_classes_covered[key]=True 
        uniqueClassesCovered+=1
    return uniqueClassesCovered

def isUniqueClassCoverage(equivalence_classes_covered,key):

    if not equivalence_classes_covered[key]: 
        equivalence_classes_covered[key]=True 

def print_test_cases(testCases):
    for testCase in testCases:
        print(f"Test Case: {testCase.dateString}, fitness: {testCase.fitness}, is valid {testCase.isValid}" )


#function tp generate the population of dates
def populate(populationLength):
    test_cases=[]
    for i in range(populationLength):
        day = random.randint(0, 31)
        day = '0' + str(day) if day < 10 else str(day)
        month = random.randint(1, 12)
        month = '0'+str(month) if month < 10 else str(month)
        year = random.randint(0, 9999)
        year = ('0'*(4-len(str(year))))+str(year)
        test_cases.append(TestCase(f"{day}/{month}/{year}", 0, is_valid_date(f"{day}/{month}/{year}")))
    return test_cases

#function to generate the next generation of dates
def select_survivors(testCases,populationLength):
    for i in range(1, populationLength):
        temp = testCases[i]
        y = i - 1
        while y >= 0 and temp.fitness > testCases[y].fitness:
            testCases[y + 1] = testCases[y]
            y -= 1
        testCases[y + 1] = temp
    reproduce(testCases, populationLength, int((populationLength*0.3)))

def reproduce(testCases, populationLength, survivors):
    for i in range(survivors,populationLength):
        randomValue=random.randint(0,survivors-1)
        testCases[i]=testCases[randomValue]
        
def randomly_vary_individual(testCases,populationLength):
    crossOver(testCases=testCases,populationLength=populationLength)
    mutate(testCases=testCases)

def mutate(testCases):
    for i in range(len(testCases)):
    
        if random.randrange(0,100) < 15:
            changeType=random.randrange(1,3)
            day = int(testCases[i].dateString[0:2])
            month = int(testCases[i].dateString[3:5])
            year = int(testCases[i].dateString[6:10])
            if changeType==1:
                day+=3
            elif changeType==2:
                month+=1
            else:
                year+=100
            day = '0' + str(day) if day < 10 else str(day)
            month = '0'+str(month) if month < 10 else str(month)
            year = ('0'*(4-len(str(year))))+str(year)
            
            testCases[i]=TestCase(f"{day}/{month}/{year}", 0, is_valid_date(f"{day}/{month}/{year}"))

def crossOver(testCases, populationLength):
    for i in range(0, populationLength - 1, 2):  
        parent_1_day, parent_1_month, parent_1_year = testCases[i].dateString.split('/')
        parent_2_day, parent_2_month, parent_2_year = testCases[i + 1].dateString.split('/')

        crossOverPosition = random.choice([1, 2])  

        if crossOverPosition == 1:
            new_date_1 = f"{parent_1_day}/{parent_2_month}/{parent_2_year}"
            new_date_2 = f"{parent_2_day}/{parent_1_month}/{parent_1_year}"
        else:
            new_date_1 = f"{parent_1_day}/{parent_1_month}/{parent_2_year}"
            new_date_2 = f"{parent_2_day}/{parent_2_month}/{parent_1_year}"
        testCases[i] = TestCase(new_date_1, 0, is_valid_date(new_date_1))
        testCases[i + 1] = TestCase(new_date_2, 0, is_valid_date(new_date_2))

def calculate_coverage(testCases):
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
            if day >= 1 and day <= 28:
                isUniqueClassCoverage(valid_equivalence_classes_covered, "D1")
            elif day == 29:
                isUniqueClassCoverage(valid_equivalence_classes_covered, "D2")
            elif day == 30:
                isUniqueClassCoverage(valid_equivalence_classes_covered, "D3")
            elif day == 31:
                isUniqueClassCoverage(valid_equivalence_classes_covered, "D4")

            if month in [1, 3, 5, 7, 8, 10, 12]:
                isUniqueClassCoverage(valid_equivalence_classes_covered, "M1")
            elif month in [4, 6, 9, 11]:
                isUniqueClassCoverage(valid_equivalence_classes_covered, "M2")
            elif month == 2:
                isUniqueClassCoverage(valid_equivalence_classes_covered, "M3")

            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):  # Leap year
                isUniqueClassCoverage(valid_equivalence_classes_covered, "Y1")
            else:
                isUniqueClassCoverage(valid_equivalence_classes_covered, "Y3")

    else:
        if month > 12:
            isUniqueClassCoverage(invalid_equivalence_classes_covered, "M5")
        if day > 31:
            isUniqueClassCoverage(invalid_equivalence_classes_covered, "D6")
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) and day == 29:
            isUniqueClassCoverage(invalid_equivalence_classes_covered, "Y5")
    
    uniqueValidClasses = sum(1 for unique in valid_equivalence_classes_covered.values() if unique)
    uniqueInvalidClasses = sum(1 for unique in invalid_equivalence_classes_covered.values() if unique)

    return (uniqueValidClasses+uniqueInvalidClasses)/12

def main():
    populationLength=50
    testCases=populate(populationLength)
    numOfGenerations=0
    coverage=0.0
    while(numOfGenerations<100 and coverage<0.96):
        fitness(testCases=testCases)
        select_survivors(testCases,populationLength=populationLength)
        randomly_vary_individual(testCases,populationLength)
        numOfGenerations+=1
        coverage=calculate_coverage(testCases)
    print("Generations:",numOfGenerations)
    print("Final coverage: ",coverage)
    


if __name__ == "__main__":
    main()