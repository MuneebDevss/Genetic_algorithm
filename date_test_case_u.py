from utility_functions import is_valid_date
import random
import csv
from utility_functions import get_date_category_with_explanation 
class TestCase:
    def __init__(self, dateString, fitness, isValid):
        self.dateString = dateString
        self.fitness=fitness
        self.isValid = isValid
def get_date_category(day, month, year,isValid):
    categories = []
    if isValid:
        if 1 <= day <= 28:
            categories.append("D1")
        elif day == 29:
            categories.append("D2")
        elif day == 30:
            categories.append("D3")
        elif day == 31:
            categories.append("D4")

        if month in [1, 3, 5, 7, 8, 10, 12]:
            categories.append("M1")
        elif month in [4, 6, 9, 11]:
            categories.append("M2")
        elif month == 2:
            categories.append("M3")
        
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            categories.append("Y1")  # Leap year
        
        else:
            categories.append("Y3")
    else:
        if day>31:
             categories.append("D6")
        if month > 12:
            categories.append("M5")
        if year>9999:
            categories.append("Y5")
    return categories

def get_date_category_by_boundry(day, month, year):
    categories = []
    if (day == 30 and month in [1, 3, 5, 7, 8, 10, 12]) or (day == 31 and month in [4, 6, 9, 11]) or ((day == 29 and month == 2)):
            categories.append("B1")
    if year==0000 and month==1 and day==1:
        categories.append("B2")
    if year == 0 and month == 1 and day == 1:
        categories.append("B3")
    return categories

def fitness(testCases,valid_equivalence_classes_covered,invalid_equivalence_classes_covered,boundry_classes_covered):    
    redundantCases=0
    for testCase in testCases:
        day,month,year = map(int,(testCase.dateString.split('/')))
        uniqueClassesCovered=0
        for category in get_date_category(day,month,year,testCase.isValid):
            if testCase.isValid:
                uniqueClassesCovered,redundantCases=isUniqueClass(valid_equivalence_classes_covered,category,uniqueClassesCovered=uniqueClassesCovered,redundantCases=redundantCases)
            else:            
                uniqueClassesCovered,redundantCases=isUniqueClass(invalid_equivalence_classes_covered,category,uniqueClassesCovered=uniqueClassesCovered,redundantCases=redundantCases)

        for category in get_date_category_by_boundry(day,month,year):
            uniqueClassesCovered,redundantCases=isUniqueClass(boundry_classes_covered,category,uniqueClassesCovered=uniqueClassesCovered,redundantCases=redundantCases)
        testCase.fitness=uniqueClassesCovered/(1+redundantCases)
        
        

def isUniqueClass(equivalence_classes_covered,key,uniqueClassesCovered,redundantCases):

    if not equivalence_classes_covered[key]: 
        equivalence_classes_covered[key]=True 
        uniqueClassesCovered+=1
    else:
        redundantCases+=1
    return uniqueClassesCovered,redundantCases

def print_test_cases(testCases,coverage):
    valid_cases = []
    invalid_cases = []
    boundary_cases = []

    for testCase in testCases:
        day, month, year = map(int, testCase.dateString.split("/"))  # Extract day, month, and year
        categories = get_date_category_with_explanation(day, month, year, testCase.isValid)  # Get categories

        if testCase.isValid:
            valid_cases.append((testCase.dateString, categories))
        else:
            invalid_cases.append((testCase.dateString, categories))

        # Check if it's a boundary case
        if "Boundary Case" in categories or "Boundry Case (Minimum)" in categories or "Boundry Case (Maximum)" in categories:
            boundary_cases.append((testCase.dateString, categories))

    # Print best test cases
    print("\nBest Test Cases:")

    # Print valid cases in required format
    print("Valid:", "".join(f"\n{date} ({', '.join(categories)})" for date, categories in valid_cases[:10]))
    print("\n")
    # Print invalid cases in required format
    print("Invalid:", "".join(f"\n{date} ({', '.join(categories)})" for date, categories in invalid_cases[:10]))
    print("\n")

    # Print boundary cases in required format
    print("Boundary:", "".join(f"\n{date} ({', '.join(categories)})" for date, categories in boundary_cases[:5]))
    print("\n")

    
    #writing data into the file
    
    if coverage > 0.7:
        with open('university_records.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(["Type", "Date", "Categories"])
            
            # Write valid cases
            for date, categories in valid_cases[:10]:
                writer.writerow(["Valid", date, ", ".join(categories)])
            
            # Write invalid cases
            for date, categories in invalid_cases[:10]:
                writer.writerow(["Invalid", date, ", ".join(categories)])
            
            # Write boundary cases
            for date, categories in boundary_cases[:5]:
                writer.writerow(["Boundary", date, ", ".join(categories)])


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
            day, month, year = map(int, testCases[i].dateString.split("/"))
            day+=3
            month+=1
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

def calculate_coverage(testCases,valid_equivalence_classes_covered,invalid_equivalence_classes_covered,boundry_classes_covered):
    uniqueValidClasses = sum(1 for unique in valid_equivalence_classes_covered.values() if unique)
    uniqueInvalidClasses = sum(1 for unique in invalid_equivalence_classes_covered.values() if unique)
    uniqueBoundryClasses = sum(1 for unique in boundry_classes_covered.values() if unique)
    return (uniqueValidClasses+uniqueInvalidClasses+uniqueBoundryClasses)/15

def main():
    
        genetic_algorithm()

def genetic_algorithm():
    valid_equivalence_classes_covered = {
        "M1": False,  # [1, 3, 5, 7, 8, 10, 12]
        "M2": False,  # [4, 6, 9, 11]
        "M3": False,  # [2]
        "D1": False,  # 1 <= day <= 28
        "D2": False,  # [29]
        "D3": False,  # [30]
        "D4": False,  # [31]
        "Y1": False,  # Leap year
        "Y3": False,   # 0 <= year <= 9999 and year % 4 != 0 (Normal year)
    }
    invalid_equivalence_classes_covered = {
        "M5": False,  # month > 12
        "D6": False,  # day > 31
        "Y5": False   # year > 9999
    }
    boundry_classes_covered={
        "B1":False,
        "B2":False,
        "B3":False,
    }
    populationLength=50
    testCases=populate(populationLength)
    numOfGenerations=0
    coverage=0.0
    while(numOfGenerations<100 and coverage<0.96):
        fitness(testCases,valid_equivalence_classes_covered,invalid_equivalence_classes_covered,boundry_classes_covered)
        select_survivors(testCases,populationLength=populationLength)
        randomly_vary_individual(testCases,populationLength)
        numOfGenerations+=1
        coverage=calculate_coverage(testCases,valid_equivalence_classes_covered,invalid_equivalence_classes_covered,boundry_classes_covered)
        valid_equivalence_classes_covered = {key: False for key in valid_equivalence_classes_covered}
        invalid_equivalence_classes_covered = {key: False for key in invalid_equivalence_classes_covered}
        boundry_classes_covered = {key: False for key in boundry_classes_covered}
    print("Generations:",numOfGenerations)
    print("Final coverage: ",coverage*100,"%")
    print_test_cases(testCases,coverage)


if __name__ == "__main__":
    main()