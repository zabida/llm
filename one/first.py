from openai import OpenAI

import mlflow

mlflow.set_experiment("genai_example")

client = OpenAI()
question = "What is MLflow?"

# register a prompt so we can link it when logging the model
system_prompt = mlflow.register_prompt(
    name="chatbot_prompt",
    template="You are a chatbot that can answer questions about IT. Answer this question: {{question}}",
    commit_message="Initial version of chatbot",
)

print(
    client.completions.create(
        prompt=system_prompt.format(question=question),
        model="gpt-3.5-turbo-instruct",
        temperature=0.1,
        max_tokens=2000,
    )
    .choices[0]
    .text
)