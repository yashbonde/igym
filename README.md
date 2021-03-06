# internet-gym

Gym for your AI to connect with the internet and play around. This framework is written with language models in mind as the actions are described in natural language and agent has to understand that in order to get to target. Read [how](#how) below.

## Installation

Install using pipy as:
```
pip install igym
```

## Usage

The syntax is same as OpenAI gym while the internals are completely different.
```python
from igym import InternetEnv, DefaultActions

# initialise the environment
env = InternetEnv("path/to/chromedriver")

target = "Google Elon Musk"  # type instruction and send to your model
while True:
  action = model(target, DefaultActions, env.state)
  env.step(action)
  
  if target_achieved:
    break
```

There are ofcourse challenges here such as open-ended generations and no rewards. Still confused, check out this [notebook](./notebooks/Task%20#1.ipynb).

## How?

At the core of this framework is `igym.core.Action` which has two attributes and one method:
* `Action.text`: Template string that explains the purpose of this Action in natural language
* `Action.args`: This dictionary is automatically extracted from the `text` and before calling each action user has to fill this using `Action.fill_values()` method. Any discrepancy is automatically caught
* `Action.step()`: This method recieves the `selenium WebDriver` object and it performs the action on the driver.

The `text` of `Action` and `step()` are thus a pair and agent has to navigate this to complete the objective.

### Sample

A sample using Language models can be found in this [notebook](./notebooks/Task%20#1%20with%20GPT2XL.ipynb).

## Why?

There are a tonne of good ideas and philosophy of what intelligence exactly is, some of the things:
* [Machine Learning Street Talk - Francois Chollet - On the Measure Of Intelligence](https://www.youtube.com/watch?v=mEVnu-KZjq4)
* [ARC Challenge](https://arxiv.org/pdf/1911.01547.pdf)
* [Intelligence Wikipedia](https://en.wikipedia.org/wiki/Intelligence)
* [AGI Wiki](https://en.wikipedia.org/wiki/Artificial_general_intelligence)

and on ... and on ... and on. However only a few people write about the use the AI as a **tool** and when they do mention it, it is usually as the assumption and focus is on generalisation or solving a specific problem / benchmark.

> I am arguing that form follows function and thus the building blocks of AGI should be based on function.

This project aims to test the ability of language models to travel the internet and answer questions. If it can travel the internet, then it can answer questions far better than any human individual can based on the amount of cached information on Google.

<!-- ### Benchmarking

Since there are no datasets available for this, obvio., we can check what siri does. Attached is the screenshot from Siri:

<img src="./assets/wiki_elon_siri.png" height=400px>

Note that the reason it gives such a beautiful response is because it is calling an API that does things. -->
