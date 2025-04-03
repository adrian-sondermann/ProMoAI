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
├── notebooks               <- Jupyter notebooks. Naming convention is a number (for ordering)
│                               and a short `-` delimited description.
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

You can run GPT4Gov-ProMoAI locally by cloning this repository, setting up the required environment and packages, and copying [.env.example](.env.example) to `.env`.
```shell
cp .env.example .env
```

This `.env` file contains all configuration parameters for the project. Update it with the necessary environment variable values (e.g., API keys). For better type hinting and validation, these variables are wrapped using Pydantic in [promoai/general_utils/config.py](promoai/general_utils/config.py).

Afterwards, execute the application:
```shell
streamlit run app.py
```


# Requirements

## Environment:

Python 3.10 is recommended for running ProMoAI. The project can be configured by

### Virtual environment using Poetry

All required dependencies are listed in [pyproject.toml](pyproject.toml) in the list `dependencies`. Dependencies only required during development are listed in section `[tool.poetry.group.dev.dependencies]`. In order to install the dependencies run and activate the virtual environment run
```shell
pip install poetry
# Configure .venv locally within this project directory
poetry config virtualenvs.in-project true

poetry lock
poetry install
poetry install --with dev
# prints the activate command of the python .venv. Afterwards, execute the displayed command manually 
poetry env activate
```

## LLM Connection

The connection and inference with LLMs is managed in [promoai/general_utils/llm_connection.py](promoai/general_utils/llm_connection.py).

### Azure OpenAI
For Azure OpenAI endpoints, ensure that the necessary configuration is provided in the `.env` file with prefix `AZURE_OPENAI_`. Please set a valid `base_url` (i.e. ending in .azure.com), which refers to a valid endpoint, the `model_name` and `model_version`. Using the configuration parameters, the target-URI is assembled in the scheme
```python
api_url = f"{base_url}/openai/deployments/{model_name}/chat/completions?api-version={model_version}"
```
Additionally, please provide the `api_key`.

### LangChain AI Portal Wheel

Not yet implemented!


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