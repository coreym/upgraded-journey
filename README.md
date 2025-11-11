# Multi-Agent Claims Processing System

This project demonstrates a multi-agent system for processing healthcare claims using the Google Agent Development Kit (ADK). The system is composed of a root agent that orchestrates several specialized sub-agents to handle different parts of the claims workflow.

## Agents

The system consists of the following agents, all defined within `root_agent/agent.py`:

- **`root_agent`**: The main orchestrator that manages the overall workflow. It delegates tasks to the appropriate sub-agent based on the user's request.
- **`claim_validator`**: Responsible for reading raw claim data (from text or images), validating it, and extracting the information into a JSON format. It can also save the output to a Google Cloud Storage bucket.
- **`formatter_agent`**: Takes the validated JSON claim data and transforms it into a valid EDI 837 claim format.
- **`post_adjudication_check_agent`**: Evaluates an already adjudicated claim against a set of plain-language instructions and determines the next steps, such as notifying the member or a claims operations team.

## Setup

1.  **Prerequisites**:
    *   Python 3.10 or higher is strongly recommended.
    *   A Google Cloud project with the Vertex AI API enabled.

2.  **Install Dependencies**:
    Install the required Python packages using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**:
    The system requires Google Cloud credentials to interact with Vertex AI. The `root_agent` is configured to load these from a `.env` file.

    Create a file named `.env` in the `root_agent` directory (`root_agent/.env`) and add the following content, replacing the placeholder with your Google Cloud project ID:

    ```
    GOOGLE_GENAI_USE_VERTEXAI=1
    GOOGLE_CLOUD_PROJECT=your-gcp-project-id
    GOOGLE_CLOUD_LOCATION=us-central1
    ```

    The application will also attempt to use your local Google Cloud application default credentials.

## Running the System

To run the multi-agent system, execute the following command from the root of the project directory:

```bash
adk run root_agent
```

This will start the `root_agent` in an interactive command-line interface. You can now interact with the system to process claims.

### Example Usage

Here are a few examples of how you can interact with the running `root_agent`:

-   **Validate a new claim**:
    ```
    [user]: Validate the following claim: Name: Jane Doe, Member ID: M789012, Service Date: 2023-10-26
    ```

-   **Validate and save to GCS**:
    ```
    [user]: Validate this claim and save it to my-claims-bucket/jane_doe_claim.json: Name: Jane Doe, Member ID: M789012
    ```

-   **Check an adjudicated claim**:
    ```
    [user]: Review this adjudicated claim with the instruction 'check for provider signature': [Full EDI 837 claim text]
    ```

The `root_agent` will automatically delegate these tasks to the appropriate sub-agent and return the result.
