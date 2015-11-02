#include <string>
using namespace std;

class MyInt {
public:
    MyInt(int value=0)
    {
        _data = value;
    }
    
    friend MyInt operator-(const MyInt &val) {
        return MyInt(-val._data);
    }
    
    MyInt operator-(const MyInt rh)
    {
        return MyInt(this->_data - rh._data);
    }
    
    operator bool()
    {
        return _data;
    }
    
    bool operator!() {
        return !_data;
    }
    
    friend MyInt operator+=(const MyInt lh, const MyInt rh)
    {
        return MyInt(lh._data + rh._data);
    }

    int operator()() {
        return _data;
    }
//private:
    int _data;
};

int main() {
    MyInt x, y(5);
    
    x =-y;
    x = y - y;
    if (x) {
        
    }
    if (!x) {
        
    }
    x +=y;
    int z = 4;
    z<<= 4;
    z+x();

    string s = "a", s2 = "a";
    s +s;
    return 0;
}
