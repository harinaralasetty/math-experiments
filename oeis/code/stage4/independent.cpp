// Independent C++ implementations. No Python core code or published values.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <functional>
#include <iostream>
#include <map>
#include <numeric>
#include <queue>
#include <set>
#include <string>
#include <vector>
using namespace std;
using U=unsigned long long;
using V=vector<int>;
string target;V p;U answer;

bool flow_feasible(const V& d){
 int m=d.size(),s=2*m,t=s+1,N=t+1;vector<V> c(N,V(N)),adj(N);
 auto edge=[&](int a,int b,int cap){c[a][b]=cap;adj[a].push_back(b);adj[b].push_back(a);};
 for(int i=0;i<m;++i){edge(s,i,d[i]);edge(m+i,t,d[i]);for(int j=0;j<m;++j)edge(i,m+j,1);}
 int total=0;
 while(true){V parent(N,-1);parent[s]=s;queue<int> q;q.push(s);
  while(!q.empty()&&parent[t]<0){int a=q.front();q.pop();for(int b:adj[a])if(parent[b]<0&&c[a][b]){parent[b]=a;q.push(b);}}
  if(parent[t]<0)break;
  for(int b=t;b!=s;b=parent[b]){--c[parent[b]][b];++c[b][parent[b]];}++total;
 }
 return total==accumulate(d.begin(),d.end(),0);
}
bool mult_ok(V d){
 while(d.size()>1){map<int,int> hist,required;for(int x:d)++hist[x];V next;for(auto [x,c]:hist){next.push_back(c);++required[c];}
  for(auto [x,c]:required)if(hist[x]<c)return false;
  d=next;
 }
 return true;
}
U segments(const V& d){
 // Enumerate boundaries with a streaming current sum. Each gap is cut or joined.
 function<U(int,int,U)> rec=[&](int pos,int current,U sums)->U{
  if(pos==(int)d.size())return current==0?1:!(sums&(1ULL<<current));
  int v=current+d[pos];U out=rec(pos+1,v,sums);
  if(pos+1<(int)d.size() && !(sums&(1ULL<<v)))out+=rec(pos+1,0,sums|(1ULL<<v));
  return out;
 };
 return d.empty()?1:rec(0,0,0);
}
V factor_support(int x){V a;for(int d=2;d*d<=x;++d)if(x%d==0){a.push_back(d);while(x%d==0)x/=d;}if(x>1)a.push_back(x);return a;}
bool incidence_tree(const V& d){
 if(d.size()==1)return true;
 for(int i=0;i<(int)d.size();++i)for(int j=i+1;j<(int)d.size();++j)if(d[i]%d[j]==0)return false;
 map<int,int> primes;vector<V> fac;for(int x:d){fac.push_back(factor_support(x));for(int v:fac.back())if(!primes.count(v))primes[v]=primes.size()+d.size();}
 V parent(d.size()+primes.size());iota(parent.begin(),parent.end(),0);
 function<int(int)> root=[&](int x){while(parent[x]!=x){parent[x]=parent[parent[x]];x=parent[x];}return x;};
 for(int i=0;i<(int)d.size();++i)for(int v:fac[i]){int a=root(i),b=root(primes[v]);if(a==b)return false;parent[a]=b;}
 for(int i=1;i<(int)parent.size();++i)if(root(i)!=root(0))return false;
 return true;
}
// Direct canonical block-multiplicity enumeration for A320052.
// At most one omitted submultiset is represented by leftovers.
bool product_sum_unique(const V& d){
 map<int,int> counts;for(int x:d)++counts[x];V vals,remaining;for(auto [x,c]:counts){vals.push_back(x);remaining.push_back(c);}
 vector<V> blocks;V b(vals.size());
 function<void(int)> gen=[&](int i){if(i==(int)b.size()){if(accumulate(b.begin(),b.end(),0)>0)blocks.push_back(b);return;}for(b[i]=0;b[i]<=remaining[i];++b[i])gen(i+1);};gen(0);
 set<U> seen;bool good=true;
 function<void(int,U)> walk=[&](int first,U product){
  if(!seen.insert(product).second){good=false;return;}
  for(int j=first;j<(int)blocks.size()&&good;++j){bool fits=true;int sum=0;for(int k=0;k<(int)vals.size();++k){if(blocks[j][k]>remaining[k])fits=false;sum+=blocks[j][k]*vals[k];}
   if(!fits)continue;for(int k=0;k<(int)vals.size();++k)remaining[k]-=blocks[j][k];walk(j,product*sum);for(int k=0;k<(int)vals.size();++k)remaining[k]+=blocks[j][k];
  }
 };
 walk(0,1);return good;
}
void visit(){
 if(target=="A321728")answer+=!flow_feasible(p);
 else if(target=="A336131")answer+=segments(p);
 else if(target=="A353426")answer+=mult_ok(p);
 else if(target=="A304382")answer+=incidence_tree(p);
 else if(target=="A320052")answer+=product_sum_unique(p);
 else throw runtime_error("unknown target");
}
void enumerate(int rem,int hi){if(rem==0){visit();return;}for(int x=min(rem,hi);x>=1;--x){p.push_back(x);enumerate(rem-x,x-int(target=="A304382"));p.pop_back();}}
int main(int,char**argv){target=argv[1];int first=stoi(argv[2]),last=stoi(argv[3]);if(last>62&&target=="A336131")return 2;for(int n=first;n<=last;++n){auto t=chrono::steady_clock::now();answer=0;p.clear();enumerate(n,n);cout<<"{\"n\":"<<n<<",\"value\":"<<answer<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-t).count()<<"}"<<endl;}}
