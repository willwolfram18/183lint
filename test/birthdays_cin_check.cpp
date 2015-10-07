/* 
 * calculates the day of the week your birthday was on
 */


#include <iostream>
#include <string>

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
 * Prompts:
****************************************************
      Thanks for using the Birthday Calculator
****************************************************
 */
void printCloser();


/**
 * Requires: nothing
 * Modifies: nothing
 * Effects: prints the menu
 * Prompts:  "1) Determine day of birth"
 *           "2) Determine birthdays for the next 10 years"
 *           "3) Finished"
 *           "Choice --> "
 */
void printMenu();


/**
 * Requires: nothing
 * Modifies: nothing
 * Effects:  prints the menu
 *           returns the users choice
 */
int getMenuChoice();


/**
 * Requires: year is a Gregorian year
 * Modifies: nothing
 * Effects: returns 'true' if the year is a leap year
 *          otherwise returns 'false'
 */
bool isLeapYear (int year);


/**
 * Requires: month, day, year may represent a date
 * Modifies: nothing
 * Effects:  returns 'true' if the date is valid
 *           otherwise returns 'false'
 *           see the spec for definition of "valid"
 */
bool isValidDate(int month, int day, int year);


/**
 * Requires: month, day, year is a valid date
 * Modifies: nothing
 * Effects:  returns the value that Zeller's formula calculates
 */
int determineDay ( int month, int day, int year);


//

/**
 * Requires: day (0 represents Sunday, 1 Monday, 2 Tuesday, etc)
 * Modifies: nothing
 * Effects:  prints the day you were born on
 *           Sunday, Monday, ..., Saturday
 */
void printDayOfBirth(int day);


/**
 * Requires: nothing
 * Modifies: nothing
 * Effects:  Asks for the Month/day/year of their birth
 *           If the date is valid, it will print the day
 *              of the week you were born on
 *           Otherwise, it will return
 */
void determineDayOfBirth();


/**
 * S'more version of this function
 * Requires: nothing
 * Modifies: nothing
 * Effects:  reads the month and day of birthday
 *           loops through 10 years printing the day of the week
 *              the birthday falls on
 *            if the month/day is not valid, it prints nothing
 */
void print10Years();




 int main() {
    printHeading();
    
    bool done = false;
    
    while (!done) {
        int choice = getMenuChoice();
        
        if (choice == 1) {
            determineDayOfBirth();
        } else if (choice == 2) {
            print10Years();
        } else {
            done = true;
        }
    }
    printCloser();
    
    
    return 0;
}



void printHeading() {
    cout << "*******************************" << endl
         << "      Birthday Calculator         " << endl
         << "*******************************" << endl << endl;
}

void printCloser() {
    cout << endl;
    cout << "****************************************************" << endl
         << "      Thanks for using the Birthday Calculator" << endl
         << "****************************************************" << endl << endl;
}

void printMenu() {
    cout << endl << endl;
    cout << "Menu Options" << endl
         << "------------" << endl;
    cout << "1) Determine day of birth" << endl;
    cout << "2) Determine birthdays for the next 10 years" << endl;
    cout << "3) Finished" << endl << endl;
    
    cout << "Choice --> ";
}

int getMenuChoice() {
    printMenu();
    
    int choice;
    cin >> choice;
    
    while (choice < 1 || choice > 3 || !cin) {
        if (cin.fail()) {
           cin.clear();
           string str;
           getline(cin, str);
           //cout << "str is: " << str ;
        }
        //cout << "val is: " << choice ;
        cout << endl << "Invalid menu choice" << endl << endl << endl;
        printMenu();
        cin >> choice;
    }
    return choice;
}


bool isLeapYear (int year)
{
   bool val;

   if (year % 100 == 0)      // century
      if (year % 400 == 0)   // leap year
          val = true;
      else                   // not leap year
          val = false;
   else if (year % 4 == 0)   // check the others divisible by 4
      val = true;
   else
      val = false;
   return val;
}


bool isValidDate(int month, int day, int year) {
// will take month, day, year as value parameters and will return
// "true" if the date is valid, "false" if the date is not valid

   bool value = true;

   if (month < 1 || month > 12 || year < 1752 || day < 1 || day > 31 || !cin) {
       value = false;
    
       return value;
   }
   
   if ((month < 9 && year == 1752) || (month == 9 && day <= 13 && year == 1752)) {
       value = false;
       return value;
   }


         
   if ((month == 1 || month ==  3 || month ==  5 || month == 7 ||
        month == 8 || month == 10 || month == 12 ) && day <= 31)
     value = true;
   else if (( month == 2 && !isLeapYear(year)) && day <= 28)
     value = true;
   else if (( month == 2 && isLeapYear(year)) && day <= 29)
     value = true;
   else if (( month == 4 || month == 6 || month == 9 || month == 11) && day <= 30)
     value = true;
   else
     value = false;

   return value;
}


int determineDay (int month, int day, int year) {
// will take month, day, year as value parameters and will return
// the value that Zeller's formula calculates


//Day = (floor((13 * M + 13) / 5) + D + Y + floor(Y / 4) + floor(C / 4) + 5 * C) MOD 7
//where:
//M is the number of the month.  Months have to be counted specially for Zeller's Rule:
//    March is 3, April is 4, and so on
//    January is 13, February is 14.
//    (This makes the formula simpler, because on leap years February 29 is counted
//     as the last day of the year.)
//    Because of this rule, January and February are always counted as the
//    13th and 14th months of the previous year.
//D is the day,
//Y is the last two digits of the year number and
//C is the century (the first two digits of the year number).
//Integer division is used. The result will be a value between 0 and 6, where
//0 means Sunday, 1 means Monday, . . . 6 means Saturday.
//Things are made slightly more complicated by the fact that months
//have to be numbered starting with March as month 1;
//January and February are treated as months 13 and 14 of the previous year.
    
    int dayOfWeek;
    int Y;   // the last two digits of the year number
    int C;   // the century
    
    if (month < 3) {
        year  = year - 1;       // subtract 1 from year number
        month = month + 12;     // convert 1 and 2 to 13 and 14
    }
    
    Y = year % 100;
    C = year / 100;
    
    dayOfWeek = (( 13 * month + 13) / 5 + day + Y + Y / 4 + C / 4 + 5 * C) % 7;
    
    if (dayOfWeek < 0)           // take care of dayOfWeek being negative
        dayOfWeek += 7;           // equivalent congruence class
    
    
    return dayOfWeek;
}


void printDayOfBirth(int day)
// will take integer day and print 
// "You were born on a: "
// "Sunday, Monday, ..., or Saturday"
{
    if (day == 0)
        cout << "Saturday";
    else if (day == 1)
        cout << "Sunday";
    else if (day == 2)
        cout << "Monday" ;
    else if (day == 3)
        cout << "Tuesday" ;
    else if (day == 4)
        cout << "Wednesday";
    else if (day == 5)
        cout << "Thursday";
    else if (day == 6)
        cout << "Friday";
    cout << endl;

}


void determineDayOfBirth() {
    int month, day, year;
    char ch;
    string str;
    
    cout << endl;
    cout << "Enter your date of birth" << endl;
    cout << "format:  month / day / year  --> ";
    cin >> month >> ch >> day >> ch >> year;
   
    
    if (!cin || !isValidDate(month, day, year)) {
        cout << endl << "Invalid date" << endl << endl << endl;
        cin.clear();
        string str;
        getline(cin, str);
        return;
    }
    
    int dayOfWeek = determineDay (month, day, year);
    cout << endl << "You were born on a: ";
    printDayOfBirth(dayOfWeek);
    cout << endl << "Have a great birthday!!!" << endl << endl;
    return;
}


void print10Years() {
    cout << "Under Construction" << endl;
/*
    cout << "Enter the month and day of your birth " << endl;
    cout << "format:  month / day    --> ";
    int month, day;
    char ch;
    cin >> month >> ch >> day;
    
    int dayOfWeek;
    bool error = true;
    
    for (int i = 0; i < 10 && cin; i++) {
        if (isValidDate(month, day, CURRENT_YEAR + i)) {
            dayOfWeek = determineDay(month, day, CURRENT_YEAR + i);
            cout << "Birthday in " << CURRENT_YEAR + i << " is on a: ";
            printDayOfBirth(dayOfWeek);
            error = false;
        }
    }
    
    // concerned that this condition is too difficult for P2
    if (error) {
        cout << endl << "Invalid date" << endl << endl << endl;
        cin.clear();
        string str;
        getline(cin,str);
        return;
    }
*/
}


