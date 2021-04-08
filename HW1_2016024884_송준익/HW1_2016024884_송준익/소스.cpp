#include <stdio.h>
#include <time.h>

#define MAX 5
const float FUNC[MAX] = { -23.4824832, 24.161472, 15.85272, -22.4, 5.0 };
#define limit 0.00001


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

float bisection(float start, float end)
{
	float answer, mid;

	while (abs(function(start)) > limit && abs(function(end)) > limit)
	{
		mid = (start + end) / 2;
		if (function(start) * function(mid) < 0) end = mid;
		else start = mid;
	}

	if (abs(function(start)) <= limit) answer = start;
	else answer = end;

	return answer;


}

float newton(float start) //Newton-Raphson Method
{
	float a, b, n;
	while (abs(function(start)) > limit)
	{
		// y = ax + b
		
		a = deriv(start);
		b = function(start) - deriv(start) * start;

		n = (-1) * (b / a);

		start = n;
	}

	return start;
}

int main()
{
	float answer1, answer2, answer3;
	clock_t bistart, biend, newstart, newend;
	double bitime, newtime;

	printf("f(1.2) = %f, f(1.200537) = %f, and %f\n", function(1.2), function(1.200537), function((1.20+1.200537)/2));
	printf("Start Bisection...\n");
	bistart = clock();
	answer1 = bisection(-2.0, 0.0);
	answer2 = bisection(2.0, 4.0);
	biend = clock();
	bitime = (double)(biend - bistart);
	printf("Bisection Complete! Answer:%f and %f\n", answer1, answer2);
	printf("Time took: %d\n", &bitime);

	printf("\n----------------------------------------\n");

	printf("Start Newton-Raphson Method...\n");
	newstart = clock();
	answer1 = newton(-2.0);
	answer2 = newton(2.0);
	answer3 = newton(4.0);
	newend = clock();
	newtime = (double)(newend - newstart);
	printf("Newton-Raphson Method Complete! Answer:%f, %f and %f\n", answer1, answer2, answer3);
	printf("Time took: %d\n", &newtime);

	return 0;
	

}