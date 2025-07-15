# Reasoning Engine Starter Pack via Github Action

This repository provides a starter pack for deploying custom reasoning engines to Vertex AI using source code or a GitHub repository. It includes a basic agent that retrieves exchange rates using the Frankfurter API as an example.

## Structure

```
starter-pack/
├── .github/
│   └── workflows/
│       └── deploy.yaml         # GitHub Actions workflow for deployment
├── app/
│   └── app.py                  # Main application code (Agent definition)
├── utils.py                    # Utility functions for deployment
├── tests/
│   └── unit/
│       └── test_app.py         # Unit tests for the agent
├── dependencies/
|   └── requirements.txt        # Project dependencies
│   └── extra_packages.txt      # Project extra packages
├── README.md                   # Project README
└── LICENSE                     # Apache 2.0 License
```

## Prerequisites

1.  **Google Cloud Project:** You need a Google Cloud project with billing enabled.
2.  **Vertex AI API:** Enable the Vertex AI API in your project.
3.  **Cloud Storage Bucket:** Create a Cloud Storage bucket to be used as the staging bucket for Vertex AI.

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
