#include <bits/stdc++.h>
using namespace std;

typedef unsigned long long ULL;

#define AC

#ifdef TLE
ULL fibo(int n)
{
	if(n == 0 || n == 1) return n;
	else
		return fibo(n-1) + fibo(n-2);
}
#endif

#ifdef AC
#define N 1000000
ULL a[N+5];
ULL fibo2(int n)
{
	if(n == 0 || n == 1) return n;
	else if(!a[n])
		return (a[n] = fibo2(n-1) + fibo2(n-2));
	else
		return a[n];
}
#endif

int n;
int main()
{
	#ifdef AC
	while(cin >> n)
		cout << fibo2(n) << '\n';
	#endif

	#ifdef TLE
	while(cin >> n)
		cout << fibo(n) << '\n';
	#endif
	return 0;
}