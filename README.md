# Radar Task ABM-FCM

This model recreates the radar task that Carley and then Sun used to demonstrate cognitive architectures in Agent Based Modelling (ABM). Instead of the cognitive architecture used in the original papers, this model uses Fuzzy Cognitive Maps (FCM) as the Agent's cognitive architecture.

## Components

This uses [project mesa](https://github.com/projectmesa/mesa) and [jfcm](https://github.com/megadix/jfcm).

## How to run

You need to have [project mesa](https://github.com/projectmesa/mesa) first, so go get that. Then run the mesa server like this:

```python

mesa runserver

```

or to run as a batch:

'''

python batch_run.py

'''

## Notes

This code accompanies a paper in the [SpringSim 2020 conference](https://scs.org/springsim/). The results from that paper can be found 
in the corresponding excel documents, and the ODD document is here in PDF format.

## Thoughts

- I used project Mesa, but perhaps Unity or Gym could be good choices for other models?
  - [ML-Agents](https://github.com/salepaun/ML-agents)
  - [Unity](https://paperswithcode.com/paper/unity-a-general-platform-for-intelligent#code)
  - [Gym](https://gym.openai.com/envs/#toy_text)
- Potentially one could try out [PyOpenFCM](https://github.com/cwhd/PyOpenFCM)

## References

Carley, Kathleen M., Michael J. Prietula, and Zhiang Lin. "Design versus cognition: The interaction of agent cognition and organizational design on organizational performance." Journal of Artificial Societies and Social Simulation 1.3 (1998): 1-19.

Sun, Ron. "Cognitive social simulation incorporating cognitive architectures." IEEE Intelligent Systems 22.5 (2007): 33-39.
