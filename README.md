# Table of Contents
1. [GPT4Gov-ProMoAI](#gpt4gov-promoai)
2. [Project Organization](#project-organization)
3. [Getting Started](#getting-started)
4. [Requirements](#requirements)
    1. [Environment](#environment)
    2. [LLM Connection](#llm-connection)
    3. [Packages](#packages)
4. [Conventions](#conventions)
    1. [Pre-Commit Hooks](#pre-commit-hooks)
    2. [Linting and Formatting](#linting-and-formatting)

# GPT4Gov-ProMoAI

GPT4Gov-ProMoAI is a fork of [ProMoAI](https://github.com/humam-kourani/ProMoAI).

## ProMoAI

ProMoAI was initially designed and developed by Humam Kourani and Allesandro Berti at the _Fraunhofer Institute for Applied Information Technology FIT_. For more details on its development and applications, refer to the paper published at IJCAI 2024: [ProMoAI – Process Modeling with AI](https://www.ijcai.org/proceedings/2024/1014.pdf).

ProMoAI is a Streamlit app that leverages Large Language Models (currently OpenAI's models) for the automatic generation of process models. ProMoAI transforms textual descriptions of processes into process models that can be exported in the BPMN and PNML formats. It also supports user interaction by providing feedback on the generated model to refine it.

# Project Organization
```
├── benchmarking            <- Benchmarking and evaluation resources.
│
├── example_online_shop     <- Example process from Kourani et al.
├── examples                <- Examples processes, including user process descriptions,
│                               engineered prompts, user feedback and generated responses.
│
├── notebooks               <- Jupyter notebooks. Naming convention is a version number │                               (for ordering) and a short `-` delimited description.
│
├── promoai                 <- Source code for use in this project.
│   │
│   ├── general_utils       <- Utility functions and helpers used across the project.
│   │   └── config.py           <- Pydantic configuration classes utilizing .env file.
│   │   └── llm_connection.py   <- Iterative inference utilizing LLMs.
│   │
│   ├── model_generation    <- Generating and validating process models from various descriptions.
│   │   ├── code_extraction.py  <- Extracting and executing python code from LLM response.
│   │   └── generator.py        <- Class ModelGenerator for the LLM to utilize in model generation.
│   │
│   ├── pn_to_powl          <- Converting Petri Nets to Partially Ordered Workflow Language (POWL).
│   │                           Not used for model generation from text description. Only used when
│   │                           process models are generated from existing BPMN, Petri net files,
│   │                           or from an event log.
│   │
│   ├── prompting           <- Prompt engineering techniques to guide the LLM to understand the
│   │   │                       process descriptions and the class ModelGenerator accurately.
│   │   └── prompt_engineering.py   <- Entry point to the conversation and prompt assembly.
│   │
│   └── main.py             <- Entry point for generating process models.
│
├── scripts                 <- Scripts that are not part of the Python module.
│
├── wheels                  <- Python Wheels, e.g. LangChain AI Portal API.
│
├── .env                    <- Environment variables.
├── .env.example            <- Template for environment variables.
│
├── app.py                  <- Entry point for the streamlit application and user interface.
│
├── packages.txt            <- Required packages for this project.
│
├── pyproject.toml          <- Project configuration file with package metadata and configuration.
│
├── README.md               <- The top-level README for developers using this project.
│
├── requirements.txt        <- The requirements file for reproducing the analysis environment, e.g.
│                               generated with `pip freeze > requirements.txt`
│
└── setup.py
```


# Getting Started

## Launching the App

To run GPT4Gov-ProMoAI locally, follow these steps:

1. **Set Up Configuration**: Copy the template file [.env.example](.env.example) to `.env`:
    ```shell
    cp .env.example .env
    ```
    Update the `.env` file with the required environment variable values (e.g., API keys). These variables are validated and type-hinted using Pydantic in [promoai/general_utils/config.py](promoai/general_utils/config.py).

2. **Install Requirements**: Prepare the Python environment, LLM Connections and install the necessary packages as outlined in the [Requirements](#requirements) section.

3. **Launch the Application**: Once all requirements are met, start the application using:
    ```shell
    streamlit run app.py
    ```

# Requirements

## Environment:

Python 3.11 is required for running ProMoAI, due to the langchain_ai_portal wheel requiring Python 3.11. Initially, [humam-kourani/ProMoAI](https://github.com/humam-kourani/ProMoAI) was tested on both Python 3.9 and 3.10.

### Virtual environment using Poetry

In order to activate the virtual environment and install all dependencies run
```shell
pip install --upgrade poetry
# Configure .venv locally within this project directory
poetry config virtualenvs.in-project true

poetry lock
poetry install
# Prints the activate command of the python .venv. Afterwards, execute the displayed command manually
poetry env activate
# For example using bash on Linux:
source .venv/bin/activate
```

**Poetry** is used to manage all Python dependencies in your project. It simplifies adding, updating, and removing dependencies while ensuring compatibility. Dependencies are defined in the [pyproject.toml](pyproject.toml) file in the list `dependencies`, and Poetry handles their installation and versioning. Dependencies only required during development are listed in section `[tool.poetry.group.dev.dependencies]`.

The `poetry add <package>` command is used to add a new dependency *package* to your project. This updates the [pyproject.toml](pyproject.toml) file automatically. Adding dependencies, which are not required during production or demos, to the development (dev) group is done by using `poetry add <package> -G dev`. 


## LLM Connection

The connection and inference with LLMs is managed in [promoai/general_utils/llm_connection.py](promoai/general_utils/llm_connection.py).

### Azure OpenAI
For Azure OpenAI endpoints, ensure that the necessary configuration is provided in the `.env` file with prefix `AZURE_OPENAI_`. Please set a valid `AZURE_OPENAI_BASE_URL` (i.e. ending in .azure.com), which refers to a valid endpoint, the `AZURE_OPENAI_MODEL_NAME` and `AZURE_OPENAI_MODEL_VERSION`. Using the configuration parameters, the target-URI is assembled following the scheme
```python
base_url = config.azure_openai.base_url             # ending in ".azure.com"
model_name = config.azure_openai.model_name         # e.g. "gpt-4o"
model_version = config.azure_openai.model_version   # e.g. "2025-01-01-preview"
api_url = f"{base_url}/openai/deployments/{model_name}/chat/completions?api-version={model_version}"
```
Additionally, please provide the `api_key`.

### LangChain AI Portal Wheel

Before continuing, please ensure you have access to an AI Portal supporting the `App-Entwicklung` app, and its administration. First, copy the latest **langchain_ai_portal .whl** into the folder `./wheels/`.

In order to ensure the correct version is installed, remove and re-add the latest wheel:
```shell
poetry remove langchain-ai-portal
# replace {MAJOR.MINOR.PATCH} with latest version
poetry add --lock ./wheels/langchain_ai_portal-{MAJOR.MINOR.PATCH}-py3-none-any.whl

# shell script to convert absolute paths added to pyproject.toml with relative paths
# only for the first time per system run
chmod +x scripts/relativize-dependencies.sh
# execute script
scripts/relativize-dependencies.sh

# lock an reinstall
poetry lock
poetry install
```

With the python module `langchain_ai_portal` you can access LLMs currently hosted on-prem in the AI Portal. In the [.env](.env) set the `PORTAL_API_HOST`, provide your `PORTAL_API_API_KEY` and set the default completion model `PORTAL_API_MODEL_NAME`, formatted as `organization/model_name`.


## Packages:

All required packages are listed in the file 'packages.txt'.

### [Graphviz](https://graphviz.org/download/)

<details>
<summary>Linux</summary>

- Debian, Ubuntu:
    ```
    sudo apt install graphviz
    ```
- Fedora project, Rocky Linux, Redhat Enterprise Linux, or CentOS:
    ```
    sudo dnf install graphviz
    ```

</details>

<details>
<summary>Windows</summary>

- https://graphviz.org/download/#windows

</details>

<details>
<summary>Mac</summary>

- Homebrew has a Graphviz port:
    ```
    brew install graphviz
    ```

</details>


# Conventions

## Pre-Commit Hooks

Pre-commit hooks are automated tools that run before each commit to ensure your code adheres to predefined quality standards. These hooks are configured in the `.pre-commit-config.yaml` file, which outlines the checks to be executed.

1. **Update Hooks**: Regularly update the hooks to their latest versions by running:
    ```bash
    pre-commit autoupdate
    ```

2. **Run Hooks Manually**: To execute all hooks on all files in the repository, use:
    ```bash
    pre-commit run --all-files
    ```

## Linting and Formatting

Ruff is a fast Python linter and formatter configured in [pyproject.toml](pyproject.toml). Run it with `ruff check` or fix issues automatically using `ruff check --fix`.

Optional: Integrate Ruff into your editor.
<details open>
<summary>VS Code</summary>

Install the Ruff extension (identifier: charliermarsh.ruff). In the extension settings, set *Ruff: Configuration Preference* to *filesystemFirst* to prioritize ".toml" configurations.
</details>

Ruff is also set up as a pre-commit hook via ruff-pre-commit.