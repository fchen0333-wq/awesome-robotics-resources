import json
import time

def check_packet(raw):
    # Quick filter for netuid4 sim data stream
    try:
        d = json.loads(raw)
        
        # must have all 3 keys or drop it
        if not all(k in d for k in ["imu", "lidar_bbox", "timestamp"]):
            return None
            
        # fix: strip outlier telemetry from glitching engine
        acc = d["imu"].get("acc", [0,0,0])
        if any(abs(x) > 50.0 for x in acc):
            print(">>> [warn] simulation anomalous frame rejected")
            return None 
            
        d["ts_local"] = time.time()
        return d
        
    except Exception:
        return None

if __name__ == "__main__":
    # raw test frame from local log
    test_json = '{"imu": {"acc": [0.1, -0.2, 9.8], "gyro": [0.0, 0.01, 0.0]}, "lidar_bbox": [1.2, 3.4, 0.5], "timestamp": 1718716800}'
    out = check_packet(test_json)
    print("Done! Valid:", out is not None)
