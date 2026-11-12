import os #reads your settings
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)  # Load environment variables from .env file
client = OpenAI(api_key=os.getenv("API_KEY"), 
                base_url=os.getenv("BASE_URL"))
MODEL = os.getenv("MODEL")

PRICE_IN,PRICE_OUT,INR = 0.075,0.30,95.0# $/1M tokens.(For Groq)
history = [{"role":"system",
            "content":"You are concise retail-banking assistant."}]

def ask(question):
    history.append({"role":"user","content":question})
    response = client.chat.completions.create(
        model=MODEL,
        messages=history,
        temperature=0.2,
        max_tokens=200
    )
    answer = response.choices[0].message.content
    history.append({"role":"assistant","content":answer})
    u = response.usage
    cost = (u.prompt_tokens*PRICE_IN +
             u.completion_tokens*PRICE_OUT)/1000000*INR
    return answer,u,cost


if __name__ == "__main__":
    total_cost = 0.0
    while True:
        question = input("> ")
        if question.strip().lower() == "quit":
            break

        answer, usage, cost = ask(question)
        total_cost += cost
        print(answer)
        print(
            f"{usage.prompt_tokens} · {usage.completion_tokens} · "
            f"₹{cost:.6f} · ₹{total_cost:.6f}"
        )
