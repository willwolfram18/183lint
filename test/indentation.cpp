using namespace std;

int main() {
    int x = 0;
    if (true)
        x++;
    if (true) {
        x++;
    }
    if (true)
    {
        x++;
    }
    switch(x) {
        case 1:
            x++;
            break;
        default:
            x = x + 2;
            break;
    }
}