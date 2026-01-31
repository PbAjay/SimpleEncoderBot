import asyncio

QUEUE = asyncio.Queue()

async def enqueue(task):
    await QUEUE.put(task)

async def start_worker():
    while True:
        task = await QUEUE.get()
        try:
            await task()
        except Exception as e:
            print("Job error:", e)
        QUEUE.task_done()
