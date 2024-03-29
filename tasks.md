# Tasks

This is an exhaustive list of tasks that I know how to do using `igym`:

- Search bing for "Elon Musk"
- Open wikipedia entry for "artificial general intelligence"
- Open any wikipedia page via google
- Open Google News and then go to "Business" Section
- How many people have been vaccinated in Covid-19?

# Relevant Research

There has been some interesting research that can be helpful:
- Divide-and-Conquer Monte Carlo Tree Search For Goal-Directed Planning ([pdf](https://arxiv.org/pdf/2004.11410.pdf)): In real life: *“the order in which we construct a plan does not have to coincide with the order in which we execute it”*, authors propose a framework for the same.

# Datasets (WIP)

First step to creation of such an agent is to have a tonne of simulation dataset ie. different variations of humans doing different a few tasks from above. Below is a sample, note this is WIP and don't consider this final:
```json
{
  "target": "Search bing for 'Elon Musk'",
  "actions": [
    {
      "id": 0, // OpenLink
      "action_args": {
        "url": "https://www.bing.com"
      }
    },
    {
      "id": 2, // TypeInputAndPressEnter
      "action_args": {
        "text": "Elon Musk"
      }
    }
  ]
}

```

Something like this can be generated programatically and also by adding random noise in terms of:
- random actions before this
- adding noise to the first input token of then model as if there is already some noisy prior
