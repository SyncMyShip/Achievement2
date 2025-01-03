# Define Date Class
class Date(object):
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    def get_date(self):
        output = str(self.day) + "/" + str(self.month) + "/" + str(self.year)
        return output
    
    # Custom method to determine if it's a leap year
    def is_leap_year(self):
        return self.year % 4 == 0
    
    # Function to check if the date is valid or not
    def is_valid_date(self):
        # First, check if values are all integers
        if not (type(self.day) == int and type(self.month) == int and type(self.year) == int):
            return False
        
        # Next, make sure that the year isn't negative
        if self.year < 0:
            return False
        
        # Next, check if the given month is between 1 and 12
        if self.month < 1 or self.month > 12:
            return False
        
        # Next, verify if the day is valid for a given month
        # List out the last dates for each month in a dictionary
        last_dates = {
            1: 31,
            2: 29 if self.is_leap_year() else 28,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31
        }

        # Finally, verify if the day is valid for the given month
        if self.day < 1 or self.day > last_dates.get(self.month):
            return False
        
        # If no 'return False' statement is triggered, return True
        return True
    

date1 = Date(29, 2, 2000) # valid - leap year
date2 = Date(29, 2, 2001) # invalid - not a leap year
date3 = Date('abc', 'def', 'ghi') # invalid - incorrect data type

# Call is_valid_date() method for each object
print(str(date1.get_date()) + ": " + str(date1.is_valid_date()))
print(str(date2.get_date()) + ": " + str(date2.is_valid_date()))
print(str(date3.get_date()) + ": " + str(date3.is_valid_date()))