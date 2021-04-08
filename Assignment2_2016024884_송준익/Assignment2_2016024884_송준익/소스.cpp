#include <stdio.h>
#include <time.h>
#include <Windows.h>

#define MAX 5
const float FUNC[MAX] = { -23.4824832, 24.161472, 15.85272, -22.4, 5.0 };
#define limit 0.00001

using namespace std;

float square(float x, int n) //xÀÇ nÁ¦°ö x^n
{
	float val = 1;
	if (n == 0) return 1;

	for (int i = 1; i <= n; i++)
	{
		val = val * x;
	}

	return val;
}

float function(float x) //Calculate given function
{
	float val = 0.0;
	for (int i = 0; i < MAX; i++)
	{
		val += FUNC[i] * square(x, i);

	}
	return val;
}

float abs(float x) //Absolute value
{
	if (x >= 0) return x;
	else return (-1) * x;
}

float deriv(float x) //Get Derivative
{
	float val = 0;
	for (int i = 1; i < MAX; i++)
	{
		val += FUNC[i] * square(x, i - 1) * i;
	}
	return val;
}

float double_deriv(float x) //Get Second Derivative
{
	float val = 0;
	for (int i = 2; i < MAX; i++)
	{
		val += FUNC[i] * square(x, i - 2) * i * (i - 1);
	}
	return val;
}

float newton(float start) //Newton Method
{
	float a, b, n;
	while (abs(deriv(start)) > limit)
	{
		// y = ax + b

		a = double_deriv(start);
		b = deriv(start) - double_deriv(start) * start;

		n = (-1) * (b / a);

		start = n;
	}

	return start;
}

float approx(float x, float h)
{
	float val;
	val = (function(x + h) -  function(x)) / h;
	return val;

}

float d_approx(float x, float h)
{
	float val;
	val = (function(x + h) - 2*function(x) + function(x - h)) / (h*h);
	return val;

}

float approx_newton(float start, float h) //Newton Method with approximation
{
	float a, b, n;
	while (abs(approx(start, h)) > limit)
	{
		// y = ax + b

		a = d_approx(start, h);
		b = approx(start, h) - d_approx(start, h) * start;

		n = (-1) * (b / a);

		start = n;
	}

	return start;
}


int main()
{
	printf("\n");


	float answer1, answer2;
	clock_t newstart, newend;
	double newtime;

	printf("Start Newton Method...\n");
	newstart = clock();
	answer1 = newton(-10.0);
	answer2 = newton(10.0);
	newend = clock();
	newtime = (double)(newend - newstart);
	printf("Newton Method Complete! \nGlobal Minimum = %f when x = %f\nLocal Minimum = %f when x = %f\n",
		function(answer1), answer1, function(answer2), answer2);
	printf("Time took: %d\n", &newtime);

	printf("\n----------------------------------------\n\n");

	clock_t astart, aend;
	double atime;
	

	Sleep(10);

	printf("Start Newton Method with Approximation...\n");
	float h = 0.001;
	astart = clock();
	answer1 = approx_newton(-10.0 , h);
	answer2 = approx_newton(10.0 , h);
	aend = clock();
	atime = (double)(aend - astart);
	printf("Newton Method with Approximation Complete! \nGlobal Minimum = %f when x = %f\nLocal Minimum = %f when x = %f\n",
		function(answer1), answer1, function(answer2), answer2);
	printf("Time took: %d\n", &atime);
	

	return 0;


}