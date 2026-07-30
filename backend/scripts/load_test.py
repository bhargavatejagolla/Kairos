import asyncio
import httpx
import time
import sys

async def fetch(client, url):
    try:
        response = await client.get(url, timeout=10.0)
        return response.status_code
    except Exception as e:
        return str(e)

async def main():
    url = "http://api.kairos.local/health"
    print(f"🚀 Initiating KAIROS Enterprise Load Test against {url}")
    print("⚠️ WARNING: This will generate extreme traffic and trigger Kubernetes HPA scaling.")
    
    # 5000 requests to trigger CPU spikes
    total_requests = 5000
    batch_size = 250
    
    async with httpx.AsyncClient() as client:
        start = time.time()
        for i in range(0, total_requests, batch_size):
            tasks = [fetch(client, url) for _ in range(batch_size)]
            results = await asyncio.gather(*tasks)
            success = sum(1 for r in results if r == 200)
            print(f"⚡ Batch {i//batch_size + 1}/{(total_requests//batch_size)}: {success}/{batch_size} succeeded")
            
            # Tiny sleep to avoid completely overwhelming the local network interface
            await asyncio.sleep(0.05)
            
        duration = time.time() - start
        print(f"\n✅ Completed {total_requests} requests in {duration:.2f} seconds")
        print(f"📊 Average RPS: {total_requests/duration:.2f} req/s")

if __name__ == "__main__":
    asyncio.run(main())
