# YELPENATOR

> **Yelpenator cannot be bargained with. It cannot be reasoned with.
> It doesn't feel pity, remorse, or fear. And it absolutely will not
> stop until you are satisfied with your restaurant choice!**

---
## Running Yelpenator

Yelpenator is a command-line restaurant recommendation agent written in Python.

From the project directory, launch the application using:

```bash
python yelpenator.py
```

On Windows systems configured to associate `.py` files with the Python interpreter, Yelpenator can also be launched directly:

```cmd
yelpenator.py
```

This second method depends on the local Windows file association and execution configuration. If it does not work, use the standard `python yelpenator.py` command.

Once launched, Yelpenator loads the restaurant dataset and customer reviews, then prompts the user to describe their dining preferences.

For example:

```text
Yelpenator-> Find me an Italian restaurant with a quiet atmosphere, romantic setting, and good service.
```

The agent searches eligible restaurants, retrieves relevant customer review evidence, analyzes the requested preferences, and displays ranked recommendations.

To exit the application, enter `quit`, `exit`, or `q`. Pressing Enter without typing a request simply returns to the prompt.

And yes, Yelpenator even lets you change your mind before asking your first question!

## Minimum Requirements

Yelpenator runs locally using Python and Ollama. It does not require access to the commercial Yelp API because restaurant information and customer reviews are loaded from the Yelp Open Dataset.

The following components are required:

1. **Python 3.10.4 or later** — Used to execute the application and its supporting modules.
2. **Python dependencies** — Install the required packages, including PyTorch, Transformers, Sentence Transformers, FAISS, and other dependencies listed in `requirements.txt`, if provided.
3. **Ollama** — Must be installed and running locally to provide language model inference.
4. **Qwen3 model** — The Ollama model used by Yelpenator must be downloaded before executing the application.
5. **Yelp dataset files** — The processed Tampa restaurant and customer review files must be accessible at the paths expected by `yelpenator.py`.

### Installing and Preparing Ollama

Install Ollama from:

https://ollama.com/download

After installation, download the required Qwen3 model:

```bash
ollama pull qwen3
```

Verify that the model is available:

```bash
ollama list
```

Ensure that the Ollama service is running before launching Yelpenator. On systems where Ollama is not already running as a background service, start it using:

```bash
ollama serve
```

The model name configured in Yelpenator must match the model installed in Ollama. If the project uses a specific Qwen3 model variant or tag, download that exact variant instead of the default.

### Installing Python Dependencies

From the project directory, if a `requirements.txt` file is included:

```bash
python -m pip install -r requirements.txt
```

The first execution may require additional time to download the sentence embedding model and initialize the local language model.

### Dataset Location

The application expects the following processed Yelp dataset files:

```text
Yelp_JSON/
    tampa_restaurants.json
    tampa_restaurant_reviews.jsonl
```

These files must be placed in a `Yelp_JSON` directory one level above the project directory, matching the relative paths used by `yelpenator.py`.

The application currently loads 2,967 Tampa restaurants from the processed dataset.

### Hardware Considerations

A dedicated GPU is recommended for faster local language model inference, although the ability to run entirely on a CPU depends on the installed model, available system memory, and software configuration. Execution times may vary substantially between systems.

An internet connection may be required for initial software and model downloads, but the recommendation workflow uses local dataset files and locally hosted model inference.
