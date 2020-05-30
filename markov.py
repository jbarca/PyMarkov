"""
Author: Jacob Barca
Since: 26/5/20
Last Modified: 27/5/20
"""

# Code obtained from: http://www.decontextualize.com/teaching/rwet/n-grams-and-markov-chains/

import random


def build_model(tokens, n):
	model = dict()
	if len(tokens) < n:
		return model

	for i in range(len(tokens) - n):
		ngram = tuple(tokens[i:i+n])
		char_after = tokens[i+n]
		if ngram not in model:
			model[ngram] = []
		model[ngram].append(char_after)
	final_gram = tuple(tokens[len(tokens)-n:])
	if final_gram not in model:
		model[final_gram] = []
	model[final_gram].append(None)

	return model


def generate(model, n, seed=None, max_iterations=100):
	if seed is None:
		seed = random.choice(list(model.keys()))

	output = list(seed)
	current = tuple(seed)
	for i in range(max_iterations):
		if current in model:
			possible_next_tokens = model[current]
			next_token = random.choice(possible_next_tokens)
			if next_token is None:
				break
			output.append(next_token)
			current = tuple(output[-n:])
		else:
			break
	return ''.join(output)


def merge_models(models):
	merged = dict()
	for model in models:
		for key, val in model.items():
			if key not in merged:
				merged[key] = []
			merged[key].extend(val)

	return merged

# Implement update_model() function

def generate_from_token_lists(token_lines, n, count=14, max_iterations=100):
	pass


def char_level_generate():
	pass


def word_level_generate():
	pass


if __name__ == "__main__":
	model = build_model("hello world, how are you today? Hello there", 2)
	print(generate(model, 2, 'he'))