// Compile com gcc -Wall -Wextra -Wconversion -Warith-conversion sema-012.c

float a;
int b;

int func(){
	return(1);
}

int main(){
	b = 18;
	a = b;

	a = b + 25;

	a = 15;

	a = func();
}
