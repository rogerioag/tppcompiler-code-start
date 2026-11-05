// gcc -Wall -Wextra -Wconversion -Warith-conversion -Wmain -Wunused-function sema-015.c

float a;
int b;

int func(){
  a = 10.2;
  return(a);
}

int main(){
	b = func();
}
