int func(int x, int y){
	return (x + y);
}

int main(){
	int a;
	float b = 10.5;

	a = func(10);
	a = func(10,20,30);
	a = func(10.5,20);
	a = func(10.5,b);
}
