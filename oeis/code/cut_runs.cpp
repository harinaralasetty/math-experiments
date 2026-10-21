// Independent binary cuts and right-to-left subsequence matching.
#include <chrono>
#include <cstdint>
#include <iostream>
using namespace std;
int main(int argc,char**argv) {
    if(argc!=2) return 2;
    int limit=stoi(argv[1]); if(limit<0 || limit>40) return 2;
    for(int n=0;n<=limit;++n) {
        auto t=chrono::steady_clock::now(); uint64_t count=0;
        if(n==0) count=1;
        else for(uint64_t mask=0;mask<(uint64_t(1)<<(n-1));++mask) {
            int word[40],runs[40],len=0,groups=0,last=0;
            uint64_t cuts=mask;
            while(cuts) {
                int end=__builtin_ctzll(cuts)+1;
                word[len++]=end-last;last=end;cuts&=cuts-1;
            }
            word[len++]=n-last;
            for(int k=0;k<len;++k) {
                if(k==0 || word[k]!=word[k-1]) runs[groups++]=1;
                else ++runs[groups-1];
            }
            int want=groups-1;
            for(int k=len-1;k>=0 && want>=0;--k) if(word[k]==runs[want]) --want;
            count+=want<0;
        }
        cout<<"{\"n\":"<<n<<",\"value\":"<<count<<",\"seconds\":"
            <<chrono::duration<double>(chrono::steady_clock::now()-t).count()<<"}"<<endl;
    }
}
