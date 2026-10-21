// Reference composition generation and forward greedy subsequence matching.
// Fixed local arrays avoid allocating a run vector for every composition.
#include <chrono>
#include <cstdint>
#include <iostream>
using namespace std;
int main(int argc,char**argv) {
    if(argc!=2) return 2;
    int limit=stoi(argv[1]); if(limit<0 || limit>40) return 2;
    for(int n=0;n<=limit;++n) {
        auto started=chrono::steady_clock::now();
        uint64_t count=0; int parts[40];
        auto visit=[&](int length) {
            int lengths[40],groups=0;
            for(int i=0;i<length;++i) {
                if(i==0 || parts[i]!=parts[i-1]) lengths[groups++]=1;
                else ++lengths[groups-1];
            }
            int next=0;
            for(int i=0;i<length && next<groups;++i)
                if(parts[i]==lengths[next]) ++next;
            count+=next==groups;
        };
        auto generate=[&](auto&& self,int remaining,int length)->void {
            if(remaining==0) {visit(length);return;}
            for(int x=1;x<=remaining;++x) {
                parts[length]=x;self(self,remaining-x,length+1);
            }
        };
        generate(generate,n,0);
        cout<<"{\"n\":"<<n<<",\"value\":"<<count<<",\"seconds\":"
            <<chrono::duration<double>(chrono::steady_clock::now()-started).count()<<"}"<<endl;
    }
}
