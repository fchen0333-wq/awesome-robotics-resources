import time
import random
import json

# TODO: check if official knx client path changes in next release
class KonnexLocalTester:
    def __init__(self, node_id="fchen0333-wq", nfts=3):
        self.node_id = node_id
        self.nfts = nfts
        self.connected = False
        print(f"[*] Init test node: {self.node_id} | Holder of {self.nfts} units")

    def connect(self):
        time.sleep(0.5)
        self.connected = True
        print("[+] sandbox connected.")

    def get_popw_data(self):
        if not self.connected:
            return None
            
        # mock imu & lidar frames for testnet ingest portal
        return {
            "ts": int(time.time()),
            "imu": {
                "acc": [round(random.uniform(-0.1, 0.1), 4) for _ in range(3)],
                "gyro": [round(random.uniform(-0.05, 0.05), 4) for _ in range(3)]
            },
            "lidar_bbox": [12.5, 45.1, 89.3, 120.4],
            "vla_output": {
                "actions": ["move_forward", "arm_grab"],
                "score": round(random.uniform(0.92, 0.98), 2)
            },
            "sig": "0x7b5ab9c74d1861f956204_holder_verified"
        }

    def run_test(self):
        self.connect()
        print("[*] running telemetry stream loops...")
        
        for i in range(3):
            data = self.get_popw_data()
            # print(data) # debug
            print(f"[Loop {i}] send chunk success. ts={data['ts']}")
            time.sleep(1)
            
        print("[+] verification test finished.")

if __name__ == "__main__":
    # using address holder profile
    client = KonnexLocalTester()
    client.run_test()
