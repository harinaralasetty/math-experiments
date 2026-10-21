// SPDX-License-Identifier: MIT
// Standalone binary-tape simulator. No decider or reference-simulator code.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
#include <cmath>
struct Rule { int write,dir,next; };
uint64_t mix(uint64_t x) { x+=0x9e3779b97f4a7c15ULL; x=(x^(x>>30))*0xbf58476d1ce4e5b9ULL; x=(x^(x>>27))*0x94d049bb133111ebULL; return x^(x>>31); }
int main(int argc,char**argv) { try {
 if(argc<3) throw std::runtime_error("usage: fast_sim MACHINE STEPS [TAPE_RLE_FILE]");
 std::string machine=argv[1],s; for(char c:machine)if(c!='_')s+=c;
 for(size_t i=0;i<machine.size();i++)if((i%7==6)!=(machine[i]=='_'))throw std::runtime_error("invalid row separator");
 int n=(s.size()/6); if(n<1||n>6||s.size()!=size_t(n*6)||machine.size()!=size_t(n*7-1))throw std::runtime_error("invalid machine size");
 Rule rules[12]; for(int i=0;i<2*n;i++) {auto t=s.substr(3*i,3);if(t=="---") rules[i]={1,1,-1};else {if((t[0]!='0'&&t[0]!='1')||(t[1]!='L'&&t[1]!='R')||(t[2]!='Z'&&(t[2]<'A'||t[2]>='A'+n)))throw std::runtime_error("invalid transition");rules[i]={t[0]-'0',t[1]=='R'?1:-1,t[2]=='Z'?-1:t[2]-'A'};}}
 uint64_t limit=std::stoull(argv[2]),step=0,flips=0,turns=0,ones=0;int state=0,prevdir=0;long origin=1<<19,head=0,lo=0,hi=0;
 std::vector<uint8_t> tape(1<<20,0);std::vector<uint64_t> checkpoints={1000,10000,100000,1000000,10000000,100000000};checkpoints.push_back(limit); std::sort(checkpoints.begin(),checkpoints.end());checkpoints.erase(std::unique(checkpoints.begin(),checkpoints.end()),checkpoints.end());
 std::cout<<"{\"machine\":\""<<machine<<"\",\"samples\":[";bool first=true;
 for(uint64_t target:checkpoints) { if(target>limit)break;
 while(step<target&&state>=0) {
  long idx=head+origin; if(idx<0||idx>=long(tape.size())) {long old=tape.size();std::vector<uint8_t> next(old*2,0);std::copy(tape.begin(),tape.end(),next.begin()+old/2);tape.swap(next);origin+=old/2;idx=head+origin;}
  int read=tape[idx];const Rule &r=rules[2*state+read];if(read!=r.write){flips++;if(r.write)ones++;else ones--;};tape[idx]=r.write;
  turns+=prevdir!=0&&prevdir!=r.dir;prevdir=r.dir;head+=r.dir;lo=std::min(lo,head);hi=std::max(hi,head);state=r.next;step++;
 }
 if(!first)std::cout<<",";first=false;uint64_t runs=1,hash=0,pairs[4]={0,0,0,0};int last=0;
 for(long x=lo;x<=hi;x++){long i=x+origin;int b=(i>=0&&i<long(tape.size()))?tape[i]:0; if(x>lo){runs+=b!=last;pairs[2*last+b]++;}last=b;if(b)hash^=mix(uint64_t(x));}
 std::cout<<"{\"steps\":"<<step<<",\"state\":"<<state<<",\"head\":"<<head<<",\"min_head\":"<<lo<<",\"max_head\":"<<hi<<",\"width\":"<<hi-lo+1<<",\"ones\":"<<ones<<",\"runs\":"<<runs<<",\"flips\":"<<flips<<",\"turns\":"<<turns<<",\"tape_hash\":\""<<hash<<"\",\"pairs\":["<<pairs[0]<<","<<pairs[1]<<","<<pairs[2]<<","<<pairs[3]<<"]}";
 if(state<0)break;
 }
 std::cout<<"],\"halted\":"<<(state<0?"true":"false")<<",\"steps\":"<<step;
 if(argc>3) {std::ofstream out(argv[3]);if(!out)throw std::runtime_error("cannot write tape");out<<"# absolute_start symbol run_length; all unlisted cells are zero\n";long start=lo;int previous=(lo+origin>=0&&lo+origin<long(tape.size()))?tape[lo+origin]:0;for(long x=lo+1;x<=hi+1;x++){int b=(x+origin>=0&&x+origin<long(tape.size()))?tape[x+origin]:0;if(x==hi+1||b!=previous){out<<start<<" "<<previous<<" "<<x-start<<"\n";start=x;previous=b;}} std::cout<<",\"tape_rle_file\":\""<<argv[3]<<"\"";}
 std::cout<<"}\n";return 0;
 }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 2;}}
