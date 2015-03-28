#include <iostream>
#include <string>
using namespace std;

int main() {
    int x = 0;
    // check compound operators
    x       += 1;
    x -= 1;
    x *= 1;
    x /= 1;
    x %= 2;
    x &= 1;
    x |= 0;
    x != 1;
    x == 1;
    x == false;
    x >= 2;
    x <= 2;
    x && false;
    x || true;

    // increment/decrement operators
    x++;
    x--;
    ++x;
    --x;

    // normal operators
    x + 1;
    x - 1;
    x * 2;
    x / 1;
    x % 2;
    x > 1;
    x < 1;
    x = 1;
    !x;
    -x;
    +x;

    cout << "hello world" << endl << x;
    cin >> x >> x;

    return 0;
}
