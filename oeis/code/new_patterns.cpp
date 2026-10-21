// Reference extension: enumerate prefixes once, update normalized suffixes
// in packed 4-bit lanes, and backtrack a set of already matched patterns.
#include <array>
#include <chrono>
#include <cstdint>
#include <functional>
#include <iostream>
#include <unordered_set>
#include <vector>
using namespace std;
using Key=__uint128_t;
struct Hash { size_t operator()(Key x) const { return uint64_t(x)^(uint64_t(x>>64)*0x9e3779b97f4a7c15ULL); } };
struct Suffix { uint32_t values=0; Key ranks=0; };
int main(int argc,char**argv) {
    if(argc!=2) return 2;
    int limit=stoi(argv[1]);
    // At weight <=31 there are at most seven distinct values and at most
    // 31 letters. Four-bit lanes plus a leading length marker fit 128 bits.
    if(limit<0 || limit>31) return 2;
    array<Key,32> ones{};
    for(int k=1;k<=31;++k) ones[k]=(ones[k-1]<<4)|1;
    vector<uint64_t> answer(limit+1);
    unordered_set<Key,Hash> found; found.insert(1);
    function<void(int,int,const array<Suffix,32>&)> visit;
    visit=[&](int weight,int length,const array<Suffix,32>& old) {
        answer[weight]+=found.size();
        for(int x=1;x<=limit-weight;++x) {
            array<Suffix,32> next{};
            vector<Key> added;
            uint32_t bit=uint32_t(1)<<x;
            next[1]={bit,1};
            for(int k=1;k<=length;++k) {
                auto s=old[k];
                int rank=__builtin_popcount(s.values&(bit-1))+1;
                if(!(s.values&bit)) {
                    // Lane d retains its guard bit in (d+8-rank) iff d>=rank.
                    Key high=ones[k]*8;
                    s.ranks+=(((s.ranks|high)-ones[k]*rank)&high)>>3;
                }
                next[k+1]={s.values|bit,(s.ranks<<4)|Key(rank)};
            }
            for(int k=1;k<=length+1;++k) {
                Key key=(Key(1)<<(4*k))|next[k].ranks;
                if(found.insert(key).second) added.push_back(key);
            }
            visit(weight+x,length+1,next);
            for(Key key:added) found.erase(key);
        }
    };
    auto started=chrono::steady_clock::now();
    visit(0,0,array<Suffix,32>{});
    double elapsed=chrono::duration<double>(chrono::steady_clock::now()-started).count();
    for(int n=0;n<=limit;++n)
        cout<<"{\"n\":"<<n<<",\"value\":"<<answer[n]<<",\"batch_seconds\":"<<elapsed<<"}"<<endl;
}
