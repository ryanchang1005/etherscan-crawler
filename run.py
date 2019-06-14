import etherscan_crawler as crawler
import json
import time

start_time = time.time()
arr = crawler.async_get_trans_list(0)
print(json.dumps(arr, indent=4))
print(f'total time = {time.time() - start_time} seconds')
