#include <iostream>
using namespace std;
int main() {
    int x = 4;
    switch (x) {
        case 1:
            cout << '+';
            break;
        case 2:
            for (int i = 1; i <= x; i++)
            {
                cout << i;
                break;
            }
            break;
        case 3:
            while(true) {
                break;
            }
            break;
        case 4:
            if (x)
            {
                cout << "-";
                break;
            }
    }
    
    do {
        break;
    } while (true);
    
    if (x) {

    }
}