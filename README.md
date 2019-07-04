# Radar Task ABM-FCM

This model recreates the radar task that Carley and then Sun used to demonstrate cognitive architectures in Agent Based Modelling (ABM). Instead of the cognitive architecture used in the original papers, this model uses Fuzzy Cognitive Maps (FCM) as the Agent's cognitive architecture.

This project is just getting started, stay tuned for updates.

## Components

This uses [project mesa](https://github.com/projectmesa/mesa) and [jfcm](https://github.com/megadix/jfcm).

## How to run

You need to have [project mesa](https://github.com/projectmesa/mesa) first, so go get that. Then run the mesa server like this:

```python

mesa runserver

```

## Thoughts and TODOs

- A bunch of stuff in the agent
  - worker can act as a team or subordinate or manager
  - need a method to make a decision based on 3 inputs
  - manager gets inputs from agents to make a decision
  - add an FCM in here...
  - add a learning method for updating weights
- Model
  - add any other inputs that we need
  - Maybe each tick is a decision?
  - Method to generate random radar blip
  - Collect all the data
    - What was the decision?
    - Was it right or wrong?
- Server
  - param to make this team or hierarchy
  - Option for blocked or the other option
  - Save data to CSV or something
- I wonder if mesa is really the best choice, or maybe use Unity or Gym?
  - [ML-Agents](https://github.com/salepaun/ML-agents)
  - https://paperswithcode.com/paper/unity-a-general-platform-for-intelligent#code
  - [Gym](https://gym.openai.com/envs/#toy_text)
- Maybe I should go pure Python with [PyOpenFCM](https://github.com/cwhd/PyOpenFCM)

## References

Carley, Kathleen M., Michael J. Prietula, and Zhiang Lin. "Design versus cognition: The interaction of agent cognition and organizational design on organizational performance." Journal of Artificial Societies and Social Simulation 1.3 (1998): 1-19.

Sun, Ron. "Cognitive social simulation incorporating cognitive architectures." IEEE Intelligent Systems 22.5 (2007): 33-39.
