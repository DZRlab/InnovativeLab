from chatbot.bedrock import generate_conversation

question_prompt = "Hvilke paragrafer i bokføringsloven omtaler Ikrafttredelse?"

completion = generate_conversation(question_prompt, ["aaa", "bbb"])

print(completion)