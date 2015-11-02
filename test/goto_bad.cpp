using namespace std;

int main() {
    int x;

    if (x) {
        goto end;
    }
    x = !x;
end:
    return 0;
}
