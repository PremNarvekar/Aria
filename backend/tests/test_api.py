"""
End-to-end client test for the ARIA research API.

Starts a research task, polls the API, and prints
the status changes as they are saved to PostgreSQL.

Run: backend\\.venv\\Scripts\\python -m backend.tests.test_api
"""

import asyncio
import httpx


async def main():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000", timeout=60.0) as client:
        # Step 1: Start research
        print("Starting research task...")
        response = await client.post(
            "/api/research",
            json={"question": "What are the latest developments in quantum computing?"}
        )
        
        if response.status_code != 202:
            print(f"Failed to start: {response.status_code} {response.text}")
            return
            
        data = response.json()
        research_id = data["research_id"]
        print(f"Started successfully. ID: {research_id}")
        print(f"Initial status: {data['status']}\n")
        
        # Step 2: Poll for status
        print("Polling status...")
        last_status = None
        
        while True:
            resp = await client.get(f"/api/research/{research_id}")
            if resp.status_code != 200:
                print(f"Error fetching status: {resp.status_code} {resp.text}")
                break
                
            session = resp.json()
            current_status = session["status"]
            
            if current_status != last_status:
                print(f"Status changed: {last_status} -> {current_status}")
                last_status = current_status
                
            if current_status in ("completed", "failed"):
                print("\nResearch finished!")
                if current_status == "completed":
                    print(f"Report keys: {list(session.get('report', {}).keys())}")
                else:
                    print(f"Error: {session.get('error')}")
                break
                
            await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())
