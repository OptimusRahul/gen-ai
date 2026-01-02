from fastapi import FastAPI, Query
from .client.rq_client import queue
from .queues.worker import process_query

app = FastAPI()

@app.get("/")
def root():
    return {"message": "RAG Queue Server is running"}

@app.post("/chat")
def chat(query: str = Query(..., description="The chat query of user")):
    job = queue.enqueue(process_query, query)
    return {"status": "queued", "job_id": job.id}

# {
#   "status": "queued",
#   "job_id": "7fcdecbe-4748-4cdc-904b-04c48415f9ae"
# }

@app.get('/job-status')
def get_result(job_id: str = Query(..., description="The job id of the job")):
    job = queue.fetch_job(job_id)
    result = job.return_value()

    return {"status": "completed", "result": result}