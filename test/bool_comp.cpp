int main() {
    bool x = true;
    // True equalities
    if (x == true) {
        x = true;
    }
    while (x == true) {}
    if (true == x) {

    }
    if (x != true) {

    }
    if (true != x) {

    }

    // False equalities
    if (x == false) {

    }
    while (x == false) {}
    if (false == x) {

    }
    if (x != false) {

    }
    if (false != x) {

    }
    return 0;
}
