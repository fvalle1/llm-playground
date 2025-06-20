from nltk.corpus import gutenberg as corpus
import requests as req
import os
from ollama import OLLAMA
from qdrant import QDrant
import numpy as np
import string
import nltk
nltk.data.path.append(os.getcwd())


def get_prompt(N):
    book = np.random.choice(corpus.fileids(), size=1)[0]
    text = corpus.raw(book)
    text = ''.join(ch for ch in text if ch not in string.punctuation)
    text = text.lower().split()
    M = N
    i = np.random.randint(0, len(text)-M)
    return book.replace(".txt", "").replace("-", " "), ' '.join(text[i:i+M])


if __name__ == "__main__":
    DEBUG = False

    if DEBUG:
        try:
            model = OLLAMA()
            qdrant = QDrant()
            print("Available models:", model.list_models())
            model_info = model.get_model_info()
            print("Model info:", model_info["model_info"])
            # embedding = model.embed("Hello")
            # print(embedding, len(embedding))
            collections = qdrant.list_collections()
            print(collections)
            qdrant.put_point([1, 0, 0], color="red")
            qdrant.put_point([0, 1, 0], color="green")
            qdrant.put_point([0, 0, 1], color="blue")
            print(qdrant.describe_collection())
            points = qdrant.query_random()
            print(qdrant.describe_points(points))
            points = qdrant.query_positive_negative(
                positive_vector=[[5, 0, 0]])
            print(qdrant.describe_points(points))
            points = qdrant.query([5, 10, 0])
            print(qdrant.describe_points(points))
        except req.RequestException as e:
            print(f"An error occurred: {e}")
    else:
        try:
            model = OLLAMA()
            embedding = model.embed("Hello")
            qdrant = QDrant(size=len(embedding))
            print(qdrant.describe_collection())

            def test_with_prompts_and_sentences(prompts, sentences):
                for sentence in sentences:
                    qdrant.put_point(
                        model.embed(sentence[1]),
                        text=sentence[1],
                        title=sentence[0]
                    )
                for prompt in prompts:
                    print("----------------------")
                    # print("Prompt: ", prompt)
                    # embedding = model.embed(prompt)
                    # print(model.generate(prompt))
                    # print("******************")
                    # context = qdrant.generate_context(qdrant.query(embedding))
                    # print("Best context: ", context)
                    # print(model.generate_with_knoledge(prompt, context))
                    # print("******************")
                    # context = qdrant.generate_context(qdrant.query_positive_negative(positive_vector=[
                    #                                   model.embed(sentence[1]) for sentence in sentences], negative_vector=[embedding]))
                    # print("Context: ", context)
                    # print(model.generate_with_knoledge(prompt, context))
                    # print("******************")
                    # context = qdrant.generate_context(qdrant.query_random())
                    # print("Random context: ", context)
                    # print(model.generate_with_knoledge(prompt, context))
                    print("******************")
                    context = qdrant.generate_context(qdrant.query_filter(filters=[{
                        "key": "title",
                        "match": {
                            "any": [
                                "austen-emma.txt",
                                'austen-persuasion.txt',
                                'austen-sense.txt'
                            ]
                        }
                    }]))
                    print("Austen context: ", context)
                    print(model.generate_with_knoledge(prompt, context))
                print("----------------------")

            # test_with_prompts_and_sentences(
            #     ["Hello, how are you?",
            #      "Ciao, come stai?"],
            #     sentences=[
            #         "Hello world",
            #         "Ciao mondo"
            #     ]
            # )
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            test_with_prompts_and_sentences(
                ["Hello, how are you?"],
                sentences=[get_prompt(10) for i in range(100)]
            )
        except req.RequestException as e:
            print(f"An error occurred: {e}")
