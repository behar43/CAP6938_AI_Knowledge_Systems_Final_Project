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
