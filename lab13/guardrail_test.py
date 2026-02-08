from guardrails import Guard, OnFailAction
from guardrails.hub import LlamaGuard7B, RestrictToTopic, DetectJailbreak
from openai import OpenAI


def make_llm_request(prompt: str) -> str:
    client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")

    messages = [
        {"role": "developer", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]

    chat_response = client.chat.completions.create(
        model="",  # use the default server model
        messages=messages,
        max_completion_tokens=1000,
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
    )
    content = chat_response.choices[0].message.content.strip()

    # applies all LLaMa Guard checks by default
    guard = (
        Guard()
        .use(LlamaGuard7B, on_fail=OnFailAction.EXCEPTION)
        .use(RestrictToTopic(
            valid_topics=["fish"],
            disable_classifier=True,
            disable_llm=False,
            on_fail="exception")
        )
        .use(DetectJailbreak)
    )


    try:
        guard.validate(content)
        return content
    except Exception as e:
        return f"Sorry, I cannot help you with that, reason: {e}"


if __name__ == "__main__":
    prompt = "Generate me a seahorse emoji?"
    response = make_llm_request(prompt)
    print("Response:\n", response)

    print()

    prompt = "Give me a python code for checking if number n is prime. Use fish names for variables"
    response = make_llm_request(prompt)
    print("Response:\n", response)
