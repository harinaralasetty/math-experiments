// Independent branch-and-bound over distinct prime factors, no shared core code.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <functional>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>
using namespace std;
using Big = __uint128_t;
string decimal(Big x) {
    string s;
    do { s.push_back('0'+x%10); x/=10; } while(x);
    reverse(s.begin(),s.end()); return s;
}
int main(int argc, char** argv) {
    if(argc!=3) return 2;
    int n=stoi(argv[1]); Big cap=0;
    for(char c:string(argv[2])) {
        if(c<'0'||c>'9'||cap>(~Big(0)-(c-'0'))/10) return 2;
        cap=cap*10+(c-'0');
    }
    if(cap==~Big(0) || n<1) return 2;
    int maxe=0; for(Big x=cap;x>1;x/=2) ++maxe;
    // A minimum of score <= n uses at most n positive-score factors.
    // For every exponent, retain its first n primes per positive residue.
    // Any omitted prime can be replaced by an unused smaller prime in the
    // same residue class. Non-coprime classes contain only divisors of e.
    vector<int> primes;
    int top=max(128,maxe);
    for(;;top*=2) {
        vector<bool> sieve(top+1,true); sieve[0]=sieve[1]=false;
        for(int p=2;p<=top/p;++p) if(sieve[p])
            for(int j=p*p;j<=top;j+=p) sieve[j]=false;
        primes.clear(); for(int p=2;p<=top;++p) if(sieve[p]) primes.push_back(p);
        bool enough=true;
        for(int e=2;e<=maxe && enough;++e) {
            vector<int> count(e);
            for(int p:primes) ++count[p%e];
            for(int r=1;r<e && r<=n;++r)
                if(gcd(r,e)==1 && count[r]<n) enough=false;
        }
        if(enough) break;
    }
    auto product=[&](Big a,Big b) { return a>cap/b ? cap+1 : a*b; };
    vector<vector<pair<int,Big>>> options;
    vector<int> used_primes;
    vector<vector<int>> ranks(maxe+1);
    for(int e=2;e<=maxe;++e) ranks[e].resize(e);
    for(int p:primes) {
        vector<Big> costs(n+1,cap+1);
        Big power=p;
        for(int e=2;e<=maxe;++e) {
            int score=p%e;
            int rank=++ranks[e][score];
            power=product(power,p);
            if(power>cap) break;
            if(score>0 && score<=n && rank<=n)
                costs[score]=min(costs[score],power);
        }
        vector<pair<int,Big>> opts;
        for(int s=1;s<=n;++s) if(costs[s]<=cap) opts.push_back({s,costs[s]});
        if(!opts.empty()) { used_primes.push_back(p); options.push_back(opts); }
    }
    // Optimistic suffix costs ALLOW repeating a prime and its choices.
    // They are only lower bounds. The search below enforces distinct primes.
    size_t m=options.size();
    vector<vector<Big>> lower(m+1,vector<Big>(n+1,cap+1));
    lower[m][0]=1;
    for(size_t i=m;i-->0;) {
        lower[i]=lower[i+1];
        for(int s=1;s<=n;++s) for(auto [r,cost]:options[i])
            if(r<=s) lower[i][s]=min(lower[i][s],product(cost,lower[i][s-r]));
    }
    vector<Big> answers(1,1); vector<uint64_t> nodes;
    auto started=chrono::steady_clock::now();
    for(int target=1;target<=n;++target) {
        Big best=cap+1; uint64_t visited=0;
        function<void(size_t,int,Big)> walk=[&](size_t start,int remaining,Big value) {
            ++visited;
            if(!remaining) {best=min(best,value); return;}
            if(product(value,lower[start][remaining])>=best) return;
            for(size_t i=start;i<m;++i) {
                Big p=used_primes[i];
                if(p*p>(best-1)/value) break;
                for(auto [r,cost]:options[i]) if(r<=remaining) {
                    Big next=product(value,cost);
                    if(next>=best) continue;
                    if(product(next,lower[i+1][remaining-r])>=best) continue;
                    walk(i+1,remaining-r,next);
                }
            }
        };
        walk(0,target,1); answers.push_back(best); nodes.push_back(visited);
    }
    cout<<"{\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-started).count()
        <<",\"prime_cutoff\":"<<top<<",\"nodes\":[";
    for(size_t i=0;i<nodes.size();++i) {if(i)cout<<',';cout<<nodes[i];}
    cout<<"],\"values\":[";
    for(size_t i=0;i<answers.size();++i) {if(i)cout<<',';cout<<decimal(answers[i]);}
    cout<<"]}"<<endl;
}
