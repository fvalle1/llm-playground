from api import API
import requests as req


class OLLAMA(API):
    def __init__(self, base_url='http://localhost:11434/api/'):
        super().__init__(base_url)
        self.model = 'mistral'
        self.options = {'temperature': 0.7, 'top_p': 0.9, 'num_predict': 1000}

    def generate(self, prompt):
        data = {'model': self.model,
                'prompt': prompt,
                'options': self.options,
                'stream': False
                }
        return self.post("generate", data)["response"]

    def generate_with_knoledge(self, prompt, context):
        data = {'model': self.model,
                'prompt': f"Knowing that the text is similar to {context} reply to {prompt}",
                'options': self.options,
                'stream': False
                }
        return self.post("generate", data)["response"]

    def list_models(self):
        return [model["name"] for model in self.get("ps")["models"]]

    def get_model_info(self, model=None):
        return self.post("show", data={'model': model if model is not None else self.model})

    def embed(self, text):
        return self.post("embeddings", data={'model': self.model, 'prompt': text})["embedding"]
