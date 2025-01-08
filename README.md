# Reasoning Engine Starter Pack

This repository provides a starter pack for deploying custom reasoning engines to Vertex AI using source code or a GitHub repository. It includes a basic agent that retrieves exchange rates using the Frankfurter API as an example.

## Structure

```
agent-engine/
├── .github/
│   └── workflows/
│       └── deploy.yaml         # GitHub Actions workflow for deployment
├── app/
│   └── app.py                  # Main application code (Agent definition)
├── build/
│   ├── deploy.py               # Deployment script
│   └── utils.py                # Utility functions for deployment
├── tests/
│   └── unit/
│       └── test_app.py         # Unit tests for the agent
├── requirements.txt            # Project dependencies
├── README.md                   # Project README
└── LICENSE                     # Apache 2.0 License
```

## Prerequisites

1.  **Google Cloud Project:** You need a Google Cloud project with billing enabled.
2.  **Vertex AI API:** Enable the Vertex AI API in your project.
3.  **Service Account:** Create a service account with the necessary permissions to access Vertex AI and Cloud Storage. You can use workload identity federation for authentication in GitHub Actions.
4.  **Cloud Storage Bucket:** Create a Cloud Storage bucket to be used as the staging bucket for Vertex AI.
5. **Github Account**: You need a GitHub account to use GitHub Actions.

## Usage

1.  **Clone the Repository:**

    ```bash
    git clone <repository_url>
    cd agent-engine
    ```

2.  **Modify the Agent (app/app.py):**

    *   Replace the `get_exchange_rate` function with your custom tool.
    *   Update the `agent` definition with your desired model, tools, and other Langchain agent parameters.

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Environment Variables (Optional):**

    *   If you're not using GitHub Actions, set the following environment variables:

        ```bash
        export PROJECT_ID="your-project-id"
        export LOCATION="your-location"
        export STAGING_BUCKET="gs://your-staging-bucket"
        ```

5.  **Deploy (Manual):**

    ```bash
    python build/deploy.py --requirements=requirements.txt --extra_packages=app
    ```
    Or specify requirements and packages inline:
    ```bash
    python build/deploy.py --requirements="pkg1,pkg2" --extra_packages="file1.py,file2.py"
    ```

6. **Deploy (GitHub Actions):**
   * Set up secrets in your GitHub repository for `PROJECT_ID`, `LOCATION`, `STAGING_BUCKET`, `WORKLOAD_IDENTITY_PROVIDER` and `SERVICE_ACCOUNT`.
   * Push your code to the `main` branch to trigger the deployment workflow.

7. **Test (after deployment)**
    ```python
    import vertexai
    from vertexai.preview import reasoning_engines

    remote_agent = vertexai.preview.reasoning_engines.ReasoningEngine(
        'projects/your-project-id/locations/your-location/reasoningEngines/your-engine-id'
    )
    remote_agent.query(
        input="What's the exchange rate from US dollars to Swedish currency?",
    )
    ```

## CI/CD with GitHub Actions

The `.github/workflows/deploy.yaml` file defines a workflow that automatically deploys the agent to Vertex AI when changes are pushed to the `main` branch. It also supports manual triggering.

**To set up GitHub Actions:**

1.  **Workload Identity Federation:** Configure workload identity federation in your Google Cloud project to allow GitHub Actions to authenticate without using service account keys.
2.  **GitHub Secrets:** Create the following secrets in your GitHub repository settings:
    *   `PROJECT_ID`: Your Google Cloud project ID.
    *   `LOCATION`: The region where you want to deploy the agent (e.g., `us-central1`).
    *   `STAGING_BUCKET`: The Cloud Storage bucket for staging.
    *   `WORKLOAD_IDENTITY_PROVIDER`: The full resource name of your workload identity provider.
    *   `SERVICE_ACCOUNT`: The email address of your service account.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
