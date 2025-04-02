import traceback
from typing import Any, Callable, Dict, List, Tuple, TypeVar

import requests
from pm4py.objects.powl.obj import POWL

from promoai.general_utils import constants
from promoai.general_utils.ai_providers import AIProviders
from promoai.general_utils.config import config
from promoai.prompting.prompt_engineering import (
    ERROR_MESSAGE_FOR_MODEL_GENERATION,
)

T = TypeVar('T')


def generate_result_with_error_handling(conversation: List[Dict[str, str]],
                                        extraction_function: Callable[[str, bool], Tuple[str, POWL]],
                                        api_key: str,
                                        llm_name: str,
                                        ai_provider: str,
                                        max_iterations: int = 5,
                                        additional_iterations: int = 5,
                                        standard_error_message: str = ERROR_MESSAGE_FOR_MODEL_GENERATION) \
        -> Tuple[str, POWL, List[Dict[str, str]]]:
    error_history = []
    for iteration in range(max_iterations + additional_iterations):
        if ai_provider == AIProviders.AZUREOPENAI.value:
            response = generate_response_with_history_azure_openai(conversation)
        elif ai_provider == AIProviders.GOOGLE.value:
            response = generate_response_with_history_google(conversation, api_key, llm_name)
        elif ai_provider == AIProviders.ANTHROPIC.value:
            response = generate_response_with_history_anthropic(conversation, api_key, llm_name)
        else:
            use_responses_api = False
            if ai_provider == AIProviders.DEEPINFRA.value:
                api_url = "https://api.deepinfra.com/v1/openai"
            elif ai_provider == AIProviders.OPENAI.value:
                api_url = "https://api.openai.com/v1"
                use_responses_api = True
            elif ai_provider == AIProviders.DEEPSEEK.value:
                api_url = "https://api.deepseek.com/"
            elif ai_provider == AIProviders.MISTRAL_AI.value:
                api_url = "https://api.mistral.ai/v1/"
            else:
                raise Exception(f"AI provider {ai_provider} is not supported!")
            response = generate_response_with_history(conversation, api_key, llm_name, api_url,
                                                      use_responses_api=use_responses_api)
        print_conversation(conversation, start=len(conversation)-2)
        try:
            conversation.append({"role": "assistant", "content": response})
            auto_duplicate = iteration >= max_iterations
            code, result = extraction_function(response, auto_duplicate)
            return code, result, conversation  # Break loop if execution is successful
        except Exception as e:
            error_description = str(e)
            error_history.append(error_description)
            if constants.ENABLE_PRINTS:
                print(f"Error detected in iteration {str(iteration + 1)}: {traceback.format_exc()}")
            new_message = (
                "Executing your code led to an error! " + standard_error_message + "This is the error"
                f" message: {error_description}"
            )
            conversation.append({"role": "user", "content": new_message})

    raise Exception(llm_name + " failed to fix the errors after " + str(max_iterations + 5) +
                    " iterations! This is the error history: " + str(error_history))


def print_conversation(conversation: List[Dict[str, str]], start: int = 0) -> None:
    if constants.ENABLE_PRINTS:
        print("\n\n")
        for index, msg in enumerate(conversation, start=start):
            print("\t%d: %s" % (index, str(msg).replace("\n", " ").replace("\r", " ")))
        print("\n\n")


def generate_response_with_history(
    conversation_history: List[Dict[str, str]],
    api_key: str,
    llm_name: str,
    api_url: str,
    use_responses_api: bool = False,
) -> str:
    """
    Generates a response from the LLM using the conversation history.

    :param conversation_history: The conversation history to be included
    :param api_key: API key
    :param llm_name: model to be used
    :param api_url: API URL to be used
    :param use_responses_api: set True for OpenAI models only
    :return: The content of the LLM response
    """
    import requests

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    messages_payload = []
    for message in conversation_history:
        role = message["role"]
        text = message["content"]
        if use_responses_api:
              processed_message = {
                "role": role,
                "content": [
                    {
                        "type": "input_text",
                        "text": text
                    }
                ]
            }
        else:
            processed_message = {
                "role": role,
                "content": text
            }

        messages_payload.append(processed_message)

    payload: Dict[str, Any] = {"model": llm_name}
    if use_responses_api:
        payload["input"] = messages_payload
    else:
        payload["messages"] = messages_payload

    if api_url.endswith("/"):
        api_url = api_url[:-1]


    if use_responses_api:
        response = requests.post(api_url + "/responses", headers=headers, json=payload).json()
    else:
        response = requests.post(api_url + "/chat/completions", headers=headers, json=payload).json()

    if "error" in response and response["error"]:
        raise Exception("Connection failed! This is the error message: " + response["error"]["message"])

    try:
        if use_responses_api:
            return response["output"][-1]["content"][0]["text"]
        else:
            return response["choices"][0]["message"]["content"]
    except Exception:
        raise Exception("Connection failed! This is the response: " + str(response))


def generate_response_with_history_azure_openai(conversation_history: List[Dict[str, str]]) -> str:
    # base_url = os.getenv("AZURE_OPENAI_BASE_URL")
    # model_name = os.getenv("AZURE_OPENAI_MODEL_NAME", "gpt-4o")
    # model_version = os.getenv("AZURE_OPENAI_MODEL_VERSION")
    # api_key = os.getenv("AZURE_OPENAI_API_KEY")
    base_url = config.azure_openai.base_url
    model_name = config.azure_openai.model_name
    model_version = config.azure_openai.model_version
    api_key = config.azure_openai.api_key

    api_url = (
        f"{base_url}/openai/deployments/{model_name}/chat/completions?api-version={model_version}"
    )
    print(f"calling {api_url}")
    headers = {"Content-Type": "application/json", "api-key": api_key}
    payload = {
        "messages": [
            {"role": msg["role"], "content": msg["content"]} for msg in conversation_history
        ],
        "temperature": 0.0,
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"]
    except Exception as e:
        raise Exception(f"Azure OpenAI request failed: {e}")


def generate_response_with_history_portal_api(conversation_history: List[Dict[str, str]]) -> str:
    # host = config.portal_api.host
    # port = config.portal_api.port
    # sdk_api_key = config.portal_api.sdk_api_key
    # use_ssl = config.portal_api.use_ssl

    # TODO
    raise Exception("LangChain AI Portal API request failed: Not yet implemented")


def generate_response_with_history_google(
    conversation_history: List[Dict[str, str]], api_key: str, google_model: str
) -> str:
    """
    Generates a response from the LLM using the conversation history.

    :param conversation_history: The conversation history to be included
    :param api_key: Google API key
    :param google_model: Google model to be used
    :return: The content of the LLM response
    """
    import google.generativeai as genai

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(google_model)
    response = model.generate_content(str(conversation_history))
    try:
        return response.text
    except Exception:
        raise Exception("Connection failed! This is the response: " + str(response))


def generate_response_with_history_anthropic(conversation: List[Dict[str, str]], api_key: str, llm_name: str) -> str:
    import anthropic

    client = anthropic.Anthropic(
        api_key=api_key,
    )
    message = client.messages.create(
        model=llm_name,
        max_tokens=8192,
        messages=conversation  # type: ignore[arg-type]
    )
    try:
        return message.content[0].text  # type: ignore[union-attr]
    except Exception:
        raise Exception("Connection failed! This is the response: " + str(message))
