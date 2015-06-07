#include "MyClass.h"
using namespace std;

int main() {
    MyClass m;
    m.myFunc();
    int x;
    while (m.isTrue() == true) {
        if (x % 2 == 0) {
            break;
        } else {
            x--;
            continue;
        }
    }
    return 0;
}