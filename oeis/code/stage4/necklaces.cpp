#include <algorithm>
#include <chrono>
#include <iostream>
#include <vector>
using namespace std;
vector<int> p; unsigned long long linear_count,circular_count;
bool canonical(){for(int k=1;k<(int)p.size();++k){for(int j=0;j<(int)p.size();++j){int a=p[j],b=p[(j+k)%p.size()];if(a<b)break;if(a>b)return false;}}return true;}
void rec(int rem,int first,__uint128_t used){
 if(rem==0){if(!canonical())return;++linear_count;int d=p.front()-p.back()+64;if(!(used&((__uint128_t(1)<<d))))++circular_count;return;}
 for(int x=first;x<=rem;++x){int d=x-p.back()+64;if(used&((__uint128_t(1)<<d)))continue;p.push_back(x);rec(rem-x,first,used|((__uint128_t(1)<<d)));p.pop_back();}
}
int main(int,char**argv){int last=stoi(argv[1]);for(int n=1;n<=last;++n){auto t=chrono::steady_clock::now();linear_count=circular_count=0;for(int f=1;f<=n;++f){p={f};rec(n-f,f,0);}double s=chrono::duration<double>(chrono::steady_clock::now()-t).count();cout<<"{\"n\":"<<n<<",\"linear\":"<<linear_count<<",\"circular\":"<<circular_count<<",\"seconds\":"<<s<<"}"<<endl;}}
