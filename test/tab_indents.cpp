void foo();

void bar(int &x) {
	x++;
}

int main() {
	int x = 0;
	int y = 10;

	foo();
	bar(y);
	if (y != 11) {

	}
	return 0;
}

void foo()
{
	// empty
}