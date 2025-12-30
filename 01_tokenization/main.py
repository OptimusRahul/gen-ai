import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")
text = "Hello, world! This is a test of the tokenization engine."
tokens = enc.encode(text)

# [13225, 11, 2375, 0, 1328, 382, 261, 1746, 328, 290, 6602, 2860, 6018, 13]
print(tokens)
print(enc.decode(tokens))