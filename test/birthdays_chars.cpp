/**
 * birthdays.cpp
 *
 * Maxim Aleksa
 * maximal@umich.edu
 *
 * EECS 183: Project 2
 *
 * Determines the day of someone's birthday.
 */

#include <iostream>
#include <string>
#include <cmath>

using namespace std;


/**
 * Requires: Nothing.
 * Modifies: cin.
 * Effects:  Clears cin and removes input for current line.
 */
void clearInput();


/**
 * Requires: nothing
 * Modifies: cout
 * Effects: prints out the initial heading for the program
 */
void printHeading();


/**
 * Requires: nothing
 * Modifies: cout
 * Effects:  prints out the final greeting for the program
 */
void printCloser();


/**
 * Requires: nothing
 * Modifies: cout 
 * Effects: prints the menu
 */
void printMenu();


/**
 * Requires: nothing
 * Modifies: cout, cin
 * Effects:  prints the menu
 *           reads the input from the user
 *           checks to make sure the input is within range for the menu
 *           If not prints "Invalid menu choice"
 *           continues to print the menu and read an input until a valid one is entered
 *           returns the users choice of menu options

 */
int getMenuChoice();


/**
 * Requires: year is a Gregorian year
 * Modifies: nothing
 * Effects: Returns 'true' if the year is a leap year
 *          otherwise returns 'false'
 */
bool isLeapYear(int year);


/**
 * Requires: month, day, year may represent a date.
 * Modifies: Nothing.
 * Effects:  Returns true if the date is on or after September 14, 1752,
 *           otherwise returns false.
 */
bool isGregorian(int month, int day, int year);


/**
 * Requires: month, day, year may represent a date
 * Modifies: cin 
 * Effects:  Returns 'true' if the date is valid
 *           otherwise returns 'false'
 *           see the spec for definition of "valid"
 */
bool isValidDate(int month, int day, int year);


/**
 * Requires: month, day, year is a valid date
 *           i.e., the date passed to this function has already passed isValidDate()
 * Modifies: nothing
 * Effects:  Returns the value that Zeller's formula calculates
 */
int determineDay(int month, int day, int year);


/**
 * Requires: day (0 represents Saturday, 1 Sunday, 2 Monday, 3 Tuesday, etc)
 * Modifies: cout
 * Effects:  prints the day you were born on
 *           Sunday, Monday, ..., Saturday
 */
void printDayOfBirth(int day);


/**
 * Requires: nothing
 * Modifies: cout, cin
 * Effects:  Asks for the Month/day/year of their birth
 *           If the date is valid, it will print the day
 *              of the week you were born on
 *           Otherwise, it will print "Invalid date" prompt
 */
void determineDayOfBirth();


/**
 * Base Project
 * Requires: nothing
 * Modifies: cout
 * Effects: prints "Under Construction"
 *
 * S'more version of this function
 * Requires: nothing
 * Modifies: cout, cin 
 * Effects:  reads the month and day of birthday
 *           loops through 10 years printing the day of the week
 *              the birthday falls on
 *            if the month/day is not valid, it prints nothing
 */
void print10Years();


int main() {
    
    const int DAY_MENU_CHOICE = 1;
    const int NEXT_10_MENU_CHOICE = 2;
    const int EXIT_MENU_CHOICE = 3;
    
    printHeading();
    
    // read menu choices from user until user finishes
    int menuChoice = 0;
    do
    {
        menuChoice = getMenuChoice();
        
        if (menuChoice == DAY_MENU_CHOICE)
        {
            determineDayOfBirth();
        }
        else if (menuChoice == NEXT_10_MENU_CHOICE)
        {
            print10Years();
        }
    }
    while (menuChoice != EXIT_MENU_CHOICE);
    
    printCloser();
}


void clearInput()
{
    cin.clear();
    
    // remove the rest of input on the line
    string ignoredInput;
    getline(cin, ignoredInput);
}


void printHeading()
{
    cout << "*******************************" << endl
         << "      Birthday Calculator      " << endl
         << "*******************************" << endl << endl;
}


void printCloser()
{
    cout << endl;
    cout << "****************************************************" << endl
         << "      Thanks for using the Birthday Calculator      " << endl
         << "****************************************************" << endl << endl;
}


void printMenu()
{
    cout << endl << endl;
    cout << "Menu Options" << endl
         << "------------" << endl;
    cout << "1) Determine day of birth" << endl;
    cout << "2) Determine birthdays for the next 10 years" << endl;
    cout << "3) Finished" << endl << endl;
    
    cout << "Choice --> ";
}

int getMenuChoice()
{
    
    const int MIN_VALID_CHOICE = 1;
    const int MAX_VALID_CHOICE = 3;
    
    int choice = 0;

    printMenu();
    cin >> choice;
    
    // check if choice is valid
    while (choice < MIN_VALID_CHOICE || choice > MAX_VALID_CHOICE)
    {
        cout << "Invalid menu choice" << endl;
        printMenu();
        
        // clear input
        if (!cin)
        {
            clearInput();
        }
        
        cin >> choice;
    }
    
    return choice;
}


bool isLeapYear(int year)
{
    
    // leap year is divisible by 400
    if (!(year % 400))
    {
        return true;
    }
    // year divisible by 100 is not a leap year
    else if (!(year % 100))
    {
        return false;
    }
    // year divisible by 4 is a leap year
    else if (!(year % 4))
    {
        return true;
    }
    else
    {
        return false;
    }
}


bool isGregorian(int month, int day, int year)
{
    // on or after Septeber 14, 1752
    if (year >= 1753)
    {
        return true;
    }
    else if (year == 1752)
    {
        if (month > 9)
        {
            return true;
        }
        else if (month == 9)
        {
            if (day >= 14)
            {
                return true;
            }
            else
            {
                return false;
            }
        }
        else
        {
            return false;
        }
    }
    else
    {
        return false;
    }
}

bool isValidDate(int month, int day, int year)
{
    
    // Gregorian calendar
    if (!isGregorian(month, day, year))
    {
        return false;
    }
    
    // lower bound for day
    if (day < 1)
    {
        return false;
    }
    
    // upper bound for day (also validates month)
    int daysInMonth = 0;
    
    switch (month)
    {
        case 1:
        case 3:
        case 5:
        case 7:
        case 8:
        case 10:
        case 12:
            daysInMonth = 31;
            break;
            
        case 4:
        case 6:
        case 9:
        case 11:
            daysInMonth = 30;
            break;
            
        case 2:
            if (isLeapYear(year))
            {
                daysInMonth = 29;
            }
            else
            {
                daysInMonth = 28;
            }
            
        default:
            break;
    }
    
    if (day > daysInMonth)
    {
        return false;
    }
    else
    {
        return true;
    }
}


int determineDay(int month, int day, int year)
{
    
    // adjust January and February
    if (month == 1 || month == 2)
    {
        month += 12;
        year -= 1;
    }
    
    int century = year / 100;
    year %= 100;
    
    // Zeller's formula
    int result = (int) (day + floor(13.0 * (month + 1) / 5) + year +
                        floor(year / 4.0) + floor(century / 4.0) + 5 * century) % 7;
    
    return result;
}


void printDayOfBirth(int day)
{
    string dayOfTheWeek;
    
    // week is 0-indexed starting on Saturday
    switch (day) {
        case 0:
            dayOfTheWeek = "Saturday";
            break;
            
        case 1:
            dayOfTheWeek = "Sunday";
            break;
            
        case 2:
            dayOfTheWeek = "Monday";
            break;
            
        case 3:
            dayOfTheWeek = "Tuesday";
            break;
            
        case 4:
            dayOfTheWeek = "Wednesday";
            break;
            
        case 5:
            dayOfTheWeek = "Thursday";
            break;
            
        case 6:
            dayOfTheWeek = "Friday";
            break;
            
        default:
            break;
    }
    
    cout << dayOfTheWeek << endl;
}


void determineDayOfBirth()
{
    
    cout << "Enter your date of birth" << endl;
    cout << "format: month / day / year  --> ";
    
    char slash;
    int month;
    int day;
    int year;
    
    cin >> month >> slash >> day >> slash >> year;
    
    // check if date is valid
    if (!cin || !isValidDate(month, day, year))
    {
        
        cout << "Invalid date" << endl;
        
        // clear input
        clearInput();
    }
    else
    {
        // print day of the week
        int dayIndex = determineDay(month, day, year);
        
        cout << "You were born on a: ";
        printDayOfBirth(dayIndex);
        
        cout << endl << "Have a great birthday!!!" << endl;
    }
}


void print10Years()
{
    cout << "Under Construction" << endl;
}
