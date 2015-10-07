/** 
 *  calculates the day of the week your birthday was on
 */


#include <iostream>
#include <string>
#include <cmath>

using namespace std;

const int CURRENT_YEAR = 2015;


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
 * Requires: day (0 represents Saturday, 1 Sunday, 2 Monday, etc)
 * Modifies: cout
 * Effects:  prints the day you were born on
 *           Sunday, Monday, ..., Saturday
 * Prompts: "Saturday", "Sunday", "Monday", "Tuesday"
 *         "Wednesday", "Thursday", "Friday"
 */
void printDayOfBirth(int day);


/**
 * Requires: nothing
 * Modifies: cout, cin
 * Effects:  Asks for the Month/day/year of their birth
 *           If the date is valid, it will print the day
 *              of the week you were born on
 *           Otherwise, it will return
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

void test_getMenuChoice() {
    int choice;
    while ((choice = getMenuChoice()) != 3) {
        cout << "Choice is: " << choice << endl;
    }
}

void test_isLeapYear() {
    int testCases[] = { 1800, 1991, 1904, 2100, 2200, 2400,
                        2531, 2624, 3000, 4000, 3997, 4996 };
    bool expectedResult[] = { false, false, true, false, false, true,
                              false, true, false, true, false, true };
    for (int i = 0; i < 12; i++) {
        if (isLeapYear(testCases[i]) != expectedResult[i]) {
            cout << "Error: expected isLeapYear(" << testCases[i]
                 << ") == " << expectedResult[i] << endl;
        }
    }
}

void test_isValidDate() {
    // Given test cases.
    cout << "isValidDate(13, 20, 1980) == "
         <<  isValidDate(13, 20, 1980) << endl;
    cout << "isValidDate(1, 32, 1980) == "
         <<  isValidDate(1, 32, 1980) << endl;
    cout << "isValidDate(4, 21, 2015) == "
         <<  isValidDate(4, 21, 2015) << endl;
    cout << "isValidDate(5, 23, 1300) == "
         <<  isValidDate(5, 23, 1300) << endl;

    // Edge cases.
    cout << "isValidDate(9, 13, 1752) == "
         <<  isValidDate(9, 13, 1752) << endl;
    cout << "isValidDate(9, 14, 1752) == "
         <<  isValidDate(9, 14, 1752) << endl;
    cout << "isValidDate(8, 14, 1752) == "
         <<  isValidDate(8, 14, 1752) << endl;
    cout << "isValidDate(9, 14, 1751) == "
         <<  isValidDate(9, 14, 1751) << endl;
    cout << "isValidDate(9, 14, 1753) == "
         <<  isValidDate(9, 14, 1753) << endl;

    // Leap years.
    cout << "isValidDate(2, 29, 1996) == "
         <<  isValidDate(2, 29, 1996) << endl;
    cout << "isValidDate(2, 29, 1995) == "
         <<  isValidDate(2, 29, 1995) << endl;

    // Non-positive numbers.
    cout << "isValidDate(-2, 19, 1995) == "
         <<  isValidDate(-2, 19, 1995) << endl;
    cout << "isValidDate(2, -19, 1995) == "
         <<  isValidDate(2, -19, 1995) << endl;
    cout << "isValidDate(2, 19, -1995) == "
         <<  isValidDate(2, 19, -1995) << endl;

    // End of month.
    cout << "isValidDate(1, 31, 1995) == "
         <<  isValidDate(1, 31, 1995) << endl;
    cout << "isValidDate(2, 28, 1995) == "
         <<  isValidDate(2, 28, 1995) << endl;
    cout << "isValidDate(3, 31, 1995) == "
         <<  isValidDate(3, 31, 1995) << endl;
    cout << "isValidDate(4, 30, 1995) == "
         <<  isValidDate(4, 30, 1995) << endl;
    cout << "isValidDate(5, 31, 1995) == "
         <<  isValidDate(5, 31, 1995) << endl;
    cout << "isValidDate(6, 30, 1995) == "
         <<  isValidDate(6, 30, 1995) << endl;
    cout << "isValidDate(7, 31, 1995) == "
         <<  isValidDate(7, 31, 1995) << endl;
    cout << "isValidDate(8, 31, 1995) == "
         <<  isValidDate(8, 31, 1995) << endl;
    cout << "isValidDate(9, 30, 1995) == "
         <<  isValidDate(9, 30, 1995) << endl;
    cout << "isValidDate(10, 31, 1995) == "
         <<  isValidDate(10, 31, 1995) << endl;
    cout << "isValidDate(11, 30, 1995) == "
         <<  isValidDate(11, 30, 1995) << endl;
    cout << "isValidDate(12, 31, 1995) == "
         <<  isValidDate(12, 31, 1995) << endl;

    // Past end of month.
    cout << "isValidDate(1, 32, 1995) == "
         <<  isValidDate(1, 32, 1995) << endl;
    cout << "isValidDate(2, 29, 1995) == "
         <<  isValidDate(2, 29, 1995) << endl;
    cout << "isValidDate(2, 30, 1996) == "
         <<  isValidDate(2, 30, 1996) << endl;
    cout << "isValidDate(3, 32, 1995) == "
         <<  isValidDate(3, 32, 1995) << endl;
    cout << "isValidDate(4, 31, 1995) == "
         <<  isValidDate(4, 31, 1995) << endl;
    cout << "isValidDate(5, 32, 1995) == "
         <<  isValidDate(5, 32, 1995) << endl;
    cout << "isValidDate(6, 31, 1995) == "
         <<  isValidDate(6, 31, 1995) << endl;
    cout << "isValidDate(7, 32, 1995) == "
         <<  isValidDate(7, 32, 1995) << endl;
    cout << "isValidDate(8, 32, 1995) == "
         <<  isValidDate(8, 32, 1995) << endl;
    cout << "isValidDate(9, 31, 1995) == "
         <<  isValidDate(9, 31, 1995) << endl;
    cout << "isValidDate(10, 32, 1995) == "
         <<  isValidDate(10, 32, 1995) << endl;
    cout << "isValidDate(11, 31, 1995) == "
         <<  isValidDate(11, 31, 1995) << endl;
    cout << "isValidDate(12, 32, 1995) == "
         <<  isValidDate(12, 32, 1995) << endl;
}

void test_determineDay() {
    cout << "determineDay(1, 29, 2064) == "
         <<  determineDay(1, 29, 2064) << endl;
}

void test_printDayOfBirth() {
    printDayOfBirth(0);
    cout << endl;
    printDayOfBirth(1);
    cout << endl;
    printDayOfBirth(2);
    cout << endl;
    printDayOfBirth(3);
    cout << endl;
    printDayOfBirth(4);
    cout << endl;
    printDayOfBirth(5);
    cout << endl;
    printDayOfBirth(6);
    cout << endl;
}

void test_determineDayOfBirth() {
    determineDayOfBirth();
}

void test() {
    test_getMenuChoice();
    test_isLeapYear();
    test_isValidDate();
    test_determineDay();
    test_printDayOfBirth();
    test_determineDayOfBirth();
}

// These are used in main() and getMenuChoice().
const int DAY_OF_BIRTH_MENU_CHOICE           = 1;
const int BIRTHDAYS_FOR_10_YEARS_MENU_CHOICE = 2;
const int FINISHED_MENU_CHOICE               = 3;

int main() {
    printHeading();

    int choice = getMenuChoice();
    while (choice != FINISHED_MENU_CHOICE) {
        if (choice == DAY_OF_BIRTH_MENU_CHOICE) {
            determineDayOfBirth();
        } else if (choice == BIRTHDAYS_FOR_10_YEARS_MENU_CHOICE) {
            print10Years();
        } else {
            cout << "Error: internal error" << endl;
        }

        choice = getMenuChoice();
    }

    printCloser();
    return 0;
}


void printHeading() {
    cout << "*******************************" << endl
         << "      Birthday Calculator      " << endl
         << "*******************************" << endl << endl;
}

void printCloser() {
    cout << endl;
    cout << "****************************************************" << endl
         << "      Thanks for using the Birthday Calculator      " << endl
         << "****************************************************" << endl << endl;
}

void printMenu() {
    cout << endl <<endl;
    cout << "Menu Options" << endl
    << "------------" << endl;
    cout << "1) Determine day of birth" << endl;
    cout << "2) Determine birthdays for the next 10 years" << endl;
    cout << "3) Finished" << endl << endl;
    
    cout << "Choice --> ";
}

int getMenuChoice() {
    const int MIN_VALID_CHOICE = DAY_OF_BIRTH_MENU_CHOICE;
    const int MAX_VALID_CHOICE = FINISHED_MENU_CHOICE;

    int choice;
    printMenu();
    cin >> choice;
    while (choice < MIN_VALID_CHOICE || choice > MAX_VALID_CHOICE) {
        // Check for end of file, return finished option if so to exit
        if (cin.eof()) {
            cout << "Error: end of file reached" << endl;
           return FINISHED_MENU_CHOICE;
#ifndef NO_ERROR_CHECKING
        } else if (cin.fail()) {
            // Clear error and discard rest of line
            string restOfLine;
# ifndef NO_FAIL_STATE_CLEAR
            cin.clear();
# endif
            getline(cin, restOfLine);
#endif
        }
        cout << "Invalid menu choice" << endl;
        printMenu();
        cin >> choice;
    }

    return choice;
}


bool isLeapYear(int year) {
    return (year % 4 == 0 &&
            (year % 100 != 0 || year % 400 == 0));
}


bool isValidDate(int month, int day, int year) {
    // First check if date falls within valid Gregorian range.
    const int FIRST_GREGORIAN_YEAR  = 1752;
    const int FIRST_GREGORIAN_MONTH = 9;
    const int FIRST_GREGORIAN_DAY   = 14;
    if (year < FIRST_GREGORIAN_YEAR ||
        (year == FIRST_GREGORIAN_YEAR &&
         (month < FIRST_GREGORIAN_MONTH ||
          (month == FIRST_GREGORIAN_MONTH &&
           day < FIRST_GREGORIAN_DAY)))) {
        return false;
    }

    // Now check valid month.
    const int MIN_VALID_MONTH = 1;
    const int MAX_VALID_MONTH = 12;
    if (month < MIN_VALID_MONTH || month > MAX_VALID_MONTH) {
        return false;
    }

    // Now check validity of day in month. Ugly without arrays!
    const int NUM_DAYS_IN_MONTH_1              = 31;
    const int NUM_DAYS_IN_MONTH_2_REGULAR_YEAR = 28;
    const int NUM_DAYS_IN_MONTH_2_LEAP_YEAR    = 29;
    const int NUM_DAYS_IN_MONTH_3              = 31;
    const int NUM_DAYS_IN_MONTH_4              = 30;
    const int NUM_DAYS_IN_MONTH_5              = 31;
    const int NUM_DAYS_IN_MONTH_6              = 30;
    const int NUM_DAYS_IN_MONTH_7              = 31;
    const int NUM_DAYS_IN_MONTH_8              = 31;
    const int NUM_DAYS_IN_MONTH_9              = 30;
    const int NUM_DAYS_IN_MONTH_10             = 31;
    const int NUM_DAYS_IN_MONTH_11             = 30;
    const int NUM_DAYS_IN_MONTH_12             = 31;
    // First ensure day is positive.
    if (day <= 0) {
        return false;
    }
    // Now check individual months.
    if ((month == 1  && day > NUM_DAYS_IN_MONTH_1) ||
        (month == 2  &&
         ((!isLeapYear(year) && day > NUM_DAYS_IN_MONTH_2_REGULAR_YEAR) ||
          ( isLeapYear(year) && day > NUM_DAYS_IN_MONTH_2_LEAP_YEAR))) ||
        (month == 3  && day > NUM_DAYS_IN_MONTH_3)  ||
        (month == 4  && day > NUM_DAYS_IN_MONTH_4)  ||
        (month == 5  && day > NUM_DAYS_IN_MONTH_5)  ||
        (month == 6  && day > NUM_DAYS_IN_MONTH_6)  ||
        (month == 7  && day > NUM_DAYS_IN_MONTH_7)  ||
        (month == 8  && day > NUM_DAYS_IN_MONTH_8)  ||
        (month == 9  && day > NUM_DAYS_IN_MONTH_9)  ||
        (month == 10 && day > NUM_DAYS_IN_MONTH_10) ||
        (month == 11 && day > NUM_DAYS_IN_MONTH_11) ||
        (month == 12 && day > NUM_DAYS_IN_MONTH_12)) {
        return false;
    }

    // All is good!
    return true;
}


int determineDay(int month, int day, int year) {
    // Adjust month and year.
    const int MIN_ZELLER_MONTH = 3;
    const int ZELLER_MONTH_ADJUSTMENT = 12;
    const int ZELLER_YEAR_ADJUSTMENT = -1;
    int adjustedMonth = month;
    int adjustedYear = year;
    if (month < MIN_ZELLER_MONTH) {
        adjustedMonth += ZELLER_MONTH_ADJUSTMENT;
        adjustedYear += ZELLER_YEAR_ADJUSTMENT;
    }

    // Compute last 2 digits of the adjusted year.
    int lastTwoOfYear = adjustedYear % 100;

    // Compute the century, i.e. first 2 digits of adjusted year.
    int century = adjustedYear / 100;

    // Now compute Zeller's formula.
    return
      (day +
       static_cast<int>(floor(static_cast<double>(13 *
                                                  (adjustedMonth + 1)) / 5)) +
       lastTwoOfYear +
       static_cast<int>(floor(static_cast<double>(lastTwoOfYear) / 4)) +
       static_cast<int>(floor(static_cast<double>(century) / 4)) +
       5 * century) %
      7;
}


void printDayOfBirth(int day) {
    const int SATURDAY  = 0;
    const int SUNDAY    = 1;
    const int MONDAY    = 2;
    const int TUESDAY   = 3;
    const int WEDNESDAY = 4;
    const int THURSDAY  = 5;
    const int FRIDAY    = 6;

    const string SATURDAY_STRING  = "Saturday";
    const string SUNDAY_STRING    = "Sunday";
    const string MONDAY_STRING    = "Monday";
    const string TUESDAY_STRING   = "Tuesday";
    const string WEDNESDAY_STRING = "Wednesday";
    const string THURSDAY_STRING  = "Thursday";
    const string FRIDAY_STRING    = "Friday";

    if (day == SATURDAY) {
        cout << SATURDAY_STRING;
    } else if (day == SUNDAY) {
        cout << SUNDAY_STRING;
    } else if (day == MONDAY) {
        cout << MONDAY_STRING;
    } else if (day == TUESDAY) {
        cout << TUESDAY_STRING;
    } else if (day == WEDNESDAY) {
        cout << WEDNESDAY_STRING;
    } else if (day == THURSDAY) {
        cout << THURSDAY_STRING;
    } else if (day == FRIDAY) {
        cout << FRIDAY_STRING;
    }

    return;
}


void determineDayOfBirth() {
    cout << "Enter your date of birth\n"
         << "format: month / day / year --> ";

    // Input date.
    int month;
    int day;
    int year;
    char slash1;
    char slash2;
    cin >> month >> slash1 >> day >> slash2 >> year;

    // Check validity of date format and range.
    if (cin.eof()) {
        cout << "Error: end of file reached" << endl;
        return;
#ifndef NO_ERROR_CHECKING
    } else if (cin.fail()) {
        cout << "\nInvalid date" << endl;
        // Make sure to clear line.
        string restOfLine;
# ifndef NO_FAIL_STATE_CLEAR
        cin.clear();
# endif
        getline(cin, restOfLine);
        return;
#endif
    } else if (slash1 != '/' || slash2 != '/' ||
               !isValidDate(month, day, year)) {
        cout << "\nInvalid date" << endl;
        return;
    }

    cout << "\nYou were born on a: ";
    printDayOfBirth(determineDay(month, day, year));
    cout << "\n\nHave a great birthday!!!" << endl;
}


void print10Years() {
#ifndef SMORE
    cout << "Under Construction" << endl;
#else
    cout << "Enter the month and day of your birth:\n"
         << "format: month / day --> ";

    // Input date.
    int month;
    int day;
    char slash;
    cin >> month >> slash >> day;

    // Check validity of date format.
    if (cin.eof()) {
        cout << "Error: end of file reached" << endl;
        return;
#ifndef NO_ERROR_CHECKING
    } else if (cin.fail()) {
        cout << "\nInvalid date" << endl;
        // Make sure to clear line.
        string restOfLine;
# ifndef NO_FAIL_STATE_CLEAR
        cin.clear();
# endif
        getline(cin, restOfLine);
        return;
#endif
    } else if (slash != '/') {
        cout << "\nInvalid date" << endl;
        return;
    }

    const int CURRENT_YEAR = 2015;
    bool foundValidBirthday = false;
    for (int i = 0; i < 10; i++) {
        int year = CURRENT_YEAR + i;
        if (isValidDate(month, day, year)) {
            foundValidBirthday = true;
            cout << "Birthday in " << year << " is on a: ";
            printDayOfBirth(determineDay(month, day, year));
            cout << endl;
        }
    }

    if (!foundValidBirthday) {
        cout << "Invalid date" << endl;
    }
#endif // SMORE
}
