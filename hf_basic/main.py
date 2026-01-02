from transformers import pipeline

# Create a text generation pipeline with Gemma model
pipe = pipeline("text-generation", model="google/gemma-3-270m-it")

# Define the conversation messages
messages = [
    {"role": "user", "content": "Who are you?"},
]

# Generate response
result = pipe(messages)

# Print the result
print(result)
print("\n--- Response ---")
print(result[0]['generated_text'][-1]['content'])