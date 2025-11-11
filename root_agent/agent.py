import os
import json
from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from google.cloud import storage

# Load environment variables from .env file.
# This ensures that credentials set in the .env file are available to all agents.
load_dotenv()

# --- Tool Definitions ---
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

# --- Sub-Agent Definitions ---

# 1. Claim Validator Agent
claim_validator_agent = Agent(
    model='gemini-2.5-flash',
    name='claim_validator',
    description="Validates claim data from text or images, extracts fields into JSON. Use this agent first to process raw claim information.",
    instruction=(
        "You are a claim validator agent. Your primary function is to read image or text and extract claim fields into a JSON response. "
        "If required fields are missing from the input, you must ask the user to provide them. "
        "If the user provides a GCS bucket, use the 'save_to_gcs' tool to save the JSON output."
    ),
    tools=[save_to_gcs],
)

# 2. Formatter Agent
formatter_agent = Agent(
    model='gemini-2.5-flash',
    name='formatter_agent',
    description="Formats a JSON object of claim fields into a valid EDI 837 claim format. Use this after a claim has been successfully validated.",
    instruction="You are a Formatter agent. Your purpose is to take a JSON object of claim fields and format them into a valid EDI 837 claim.",
)

# 3. Post-Adjudication Check Agent
post_adjudication_agent = Agent(
    model='gemini-2.5-flash',
    name='post_adjudication_check_agent',
    description="Evaluates a fully adjudicated healthcare claim based on a set of plain-language instructions.",
    instruction=(
        "You are a Post-adjudication check agent. Your purpose is to take a full healthcare claim and a set of plain-language instructions, and evaluate the claim based on those instructions. "
        "If the claim status code indicates an issue a member can resolve (e.g., an address mismatch), output an email to the member explaining the issue and how to fix it. "
        "If the issue is something they cannot address on their own (e.g., a Provider Taxonomy code mismatch), output a summary of the claim and the issue that needs to be addressed by a claims operations team."
    ),
)


# --- Root Agent Definition ---
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="The main orchestrator for the claims processing workflow. It delegates tasks to validator, formatter, and post-adjudication agents.",
    instruction=(
        "You are the root agent for a claims processing system. Your job is to manage the workflow by delegating to your sub-agents. "
        "1. For new claims, first delegate to the 'claim_validator' agent. "
        "2. If the claim is validated successfully, delegate the JSON output to the 'formatter_agent' to create an EDI 837 claim. "
        "3. If the user wants to check an already processed claim, delegate to the 'post_adjudication_check_agent'. "
        "Do not perform these tasks yourself; always delegate to the appropriate sub-agent."
    ),
    sub_agents=[
        claim_validator_agent,
        formatter_agent,
        post_adjudication_agent,
    ]
)
