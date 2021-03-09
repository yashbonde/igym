# internet-gym

Gym for your AI to connect with the internet and play around. This framework is written with language models in mind as the actions are described in natural language and agent has to understand that in order to get to target. Read [usage](#usage) and [what](#what) below.

## Installation

Install using pipy as:
```
pip install igym
```

Want to know what you can do, see a list of [tasks](./tasks.md).

## Usage

Since this is an open framework, there is no hard limit on how to complete one task. The end state of the task will have to be manually checked. In a very high level abstraction, this is how it looks like:
```python
from igym import InternetEnv, DefaultActions

# initialise the environment
env = InternetEnv("path/to/chromedriver")

target = "Google Elon Musk"  # type instruction and send to your model
while True:
  action = model(target, DefaultActions, env)
  env.step(action)
  
  if target_achieved: # <-- define your target here
    break
```

You can also build your own decision tree style search while manually curating the options, "how"?. Check out this [notebook](./notebooks/Task%20#1.ipynb).

## What?

At the core of this framework is `igym.core.Action` which has two attributes (`text` and `args`) and one method (`step`). The `text` and `step()` are thus a pair of natural language to program and agent has to navigate this to complete the objective. Consider the following example:
```python
class TypeInputAndPressEnter(Action):
  def __init__(self, text="Type the following '{text}' in the input box and press Enter"):
    ### 1 ###
    # text: Template string that explains the purpose of this Action in natural language
    # you can see how easy it is for any person / AI to understand what is the purpose of this
    # action
    super().__init__(text = text)

  def step(self, driver):
    ### 2 ###
    # step(): This method recieves the `selenium WebDriver` object and it performs the
    # action on the driver. We explicitly provide driver because there are all kinds of
    # nuances on the internet and so it's better if human programs this.

    ### 3 ###
    # This dictionary is automatically extracted from the `text` and before
    # calling each action user has to fill this using `Action.fill_values()` method.
    # Any discrepancy during filling is automatically caught!
    args = self.args

    curr_url = driver.current_url
    if "google" in curr_url: # weird subroutine for google
      ele = driver.find_element_by_name("q")
    else:
      ele = driver.find_element_by_tag_name("input")
    ele.send_keys(args["text"]) # <-------- args "text" from the template
    ele.send_keys(Keys.ENTER)
```

### Sample

Since this is designed with langauge models in mind, a sample can be found in this [notebook](./notebooks/Task%20%231%20with%20GPT2.ipynb).

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
