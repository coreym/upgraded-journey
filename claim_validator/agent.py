from google.adk.agents.llm_agent import Agent
from google.cloud import storage
import json

def save_to_gcs(bucket_name: str, file_name: str, data: dict) -> dict:
    """Saves the given data to a file in the specified GCS bucket."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_string(json.dumps(data, indent=2))
        return {"status": "success", "message": f"Successfully saved to gs://{bucket_name}/{file_name}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

root_agent = Agent(
    model='gemini-2.5-flash',
    name='claim_validator',
    description="A claim validator agent responsible for reading image or text and returning a JSON response with the claim fields contained.",
    instruction="You are a claim validator agent. Your primary function is to read image or text and extract claim fields into a JSON response. If required fields are missing, you must ask the user to provide them. If a GCS bucket is provided, use the 'save_to_gcs' tool to save the JSON output. Example output: {\"Name\":\"corey Maher\", \"MemberID\":\"MEM1234553\"}",
    tools=[save_to_gcs],
)
