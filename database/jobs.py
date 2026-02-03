import time
from database.mongo import jobs

def create_job(chat_id, file_id, settings):
    return {
        "chat_id": chat_id,
        "file_id": file_id,
        "settings": settings,
        "status": "queued",
        "created_at": time.time()
    }

async def save_job(job):
    result = await jobs.insert_one(job)
    job["_id"] = result.inserted_id

async def update_status(job_id, status):
    await jobs.update_one(
        {"_id": job_id},
        {"$set": {"status": status}}
    )

async def resume_jobs(enqueue_func, process_func):
    """
    enqueue_func  -> jobqueue.scheduler.enqueue
    process_func  -> telegram.processor.process_job
    """
    async for job in jobs.find({"status": {"$ne": "done"}}):
        async def task(j=job):
            await process_func(j)
        await enqueue_func(task)
