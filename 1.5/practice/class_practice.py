# Define Date Class
class Date(object):
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

# Create an inherience of Date as an object
first_moon_landing = Date(20, 7, 1969)

# Access data in object with dot notation
print("Initial values of first_moon_landing")
print(first_moon_landing.day)
print(first_moon_landing.month)
print(first_moon_landing.year)

# Try modifying some of the values using dot notation again
first_moon_landing.day = 25
first_moon_landing.month = 11
first_moon_landing.year = 1800

# Print out the modified contents
print("Modified values in first_moon_landing -")
print(first_moon_landing.day)
print(first_moon_landing.month)
print(first_moon_landing.year)