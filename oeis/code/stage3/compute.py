"""Clean method subprocess. Never reads b-files or expected term values."""
import argparse,json,resource,time
from datetime import datetime,timezone

def main():
    p=argparse.ArgumentParser();p.add_argument('id');p.add_argument('method',choices=['reference','independent']);p.add_argument('limit',type=int);args=p.parse_args()
    wall=time.perf_counter();cpu=time.process_time();rows=[]
    if args.id in ['A374680','A374681','A374682']:
        if args.method=='reference':from anti_dp import counts
        else:from anti_series import counts
        relation={'A374680':'down','A374681':'upweak','A374682':'downweak'}[args.id]
        values=counts(args.limit,relation)
    elif args.id in ['A383710','A383711']:
        if args.method=='reference':from partition_reference import count
        else:from partition_independent import count
        values=[]
        for n in range(args.limit+1):
            t=time.perf_counter();values.append(count(n,args.id=='A383711'))
            rows.append(dict(n=n,seconds=time.perf_counter()-t))
    else:raise ValueError(args.id)
    print(json.dumps(dict(id=args.id,method=args.method,limit=args.limit,values=values,timings=rows,wall_seconds=time.perf_counter()-wall,cpu_seconds=time.process_time()-cpu,maxrss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,finished_utc=datetime.now(timezone.utc).isoformat())))
if __name__=='__main__':main()
