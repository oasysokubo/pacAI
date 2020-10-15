## Pacman

A modified version of the Pacman project from the [Berkeley AI Lab](http://ai.berkeley.edu/project_overview.html) using reinforcement learning.

### 1  Introduction

In this project, we designed an agent that competed against other teams in the Capture the Flag Tournamentto achieve the most victories out of the entire class of CSE-140.  One fundamental issue that we encounteredat the start of the project was that we were still unfamiliar with the codebase in terms of integrating thecomplex algorithms that were introduced to us in the previous assignments.  The second fundamental issuearose after we solved the first problem, and it was a matter of generating useful data for our features beforethe due date of the project.  In the rest of this paper,  we elaborate on how we modeled and representedthese fundamental problems (Section 2), discuss the strategies and algorithmic choices we made to solve andimplement each problem (Section 3),  note the obstacles that we encountered during this project (Section4), and evaluate the performance of our agent and review the lessons learned after the completion of thisproject (Section 5).

### 2  Models and Representations of the Fundamental Problems

We modeled the problem of understanding how to integrate the complex algorithms from previous assign-ments as a case of trial and error. The algorithms that we tried to integrate into the codebase was Alpha-BetaPruning on Minimax and Approximate QLearning algorithms. We tried out a bunch of different ideas, such aschanging the search ply ofMinimaxfrom Pacman’s turn and all other ghost’s turn to Pacman’s turn all otheradversaries (including Pacman’s teammate) taking an action.  However, after implementing Alpha-Beta, werealized that it was too computationally intensive and we could not explore more than a single depth in the tree.  As a result, we moved on to trying to implementApproximateQLearning, but after implementing thealgorithm we were met with the same issue asAlpha-beta—it was too computationally expensive.  Fromthis, we changed our approach to design better features instead of trying to implement the complex algo-rithms from our previous assignments.  This resulted in the idea of generating useful data that allowed us to design better features.  

We modeled the problem of generating useful data as a series of simpler problems:

1.  Find all points in the grid that is not a wall.
2.  Find all dead-ends.
3.  Infer choke points from all dead-ends.

This model that we determined allowed us to represent each subproblem with a different approach, whichallowed us to reach the solution more efficiently.


### 3  Computational Strategy and Algorithmic Choices

The computational strategy that we designed to solve the problem of generating useful data was essentiallya filtered search through the entire layout of the grid.  To solve the problem of finding all choke points, weattempted to run depth-first search from the starting point of each team. However, we realized that thiswould be extremely difficult because we were trying to use a search algorithm to find the choke points whenwe did not know when we have found all choke points (our goal test).  Next, we tried to solve this problem by using a bottom-up approach, which required us to determine the dead-ends D in the grid and infer asmuch choke points as possible from each dead-end.  The computational strategy used to determineDwas toperform a line sweep across the entire grid G, and for each point pin G, if p consisted of only one legal action, then we appended p to D. After we determined D, we implemented a brute force algorithm that inferred almost all choke points C from each dead-end.  After generating the choke point data-set, we designed an offensive feature that evaluated the utility of entering the corridor of dead-ends whenever our agent is atthe entrance of this corridor.  This feature used the information of how many steps the corridor required forour agent to traverse the corridor and exit the corridor safely.  We evaluated the safeness of traversing thecorridor by calculating the minimum distance from the enemy to our agent and if the enemy distance was lessthan the required number of steps to traverse the corridor, then it is safe for our agent to enter the corridor.

### 4  Obstacles Encountered

Initially, we  did not work on generating  useful  data  using  the  choke  point  algorithm. Since we realized this concept late in the tournament, we did not have enough time to implement all of our ideas.  After weimplemented the choke point algorithm and designed a feature using the choke point data, we faced a new problem where Pacman was stuck on the choke point—Pacman never enters the corridor until a is ghost nearit.  Furthermore, we spent a long time designing the “map gravity”, which provides a score for every gridpoint on the map, where the area that has a higher concentration of foods has a higher score.  We wantedPacman to follow the highest value grid around it,  but this is the wrong approach to achieve our goal ofwinning  the  match  since  Pacman  needed  to  dodge  ghosts,  and  we  could  not  generate  the  optimal  scoresbefore the start of the game.  Additionally, we debated for a long time about when our agents should defendor attack.  As a result, we went back to improve the Baseline Agents instead of redesigning a combinationagent on the final day of the tournament.  Since we did not have enough time, we improved our defense agentby telling the agent to always stay near the midpoint of the map.  However, in the final minutes, we realizedthat our agent still had a crashing error due to getting a wall as a midpoint and attempting to calculate themaze distance to a wall, thus we submitted an agent that would crash depending on the random map thatwas generated.

### 5  Performance Evaluation and Lessons Learned

In this section, we will elaborate on our discoveries in terms of how our agent performed and what we learned as a result of completing this project.

#### 5.1  Performance

After we implemented an offensive feature that utilized the choke point data, we noticed that our agent onlyhad a slight improvement from the backup agent we were implementing, which was on average a 55% win-rate over the baseline agent.  As a result, we decided that we should also design a feature for our defensive agent, which was to focus on preventing the enemy from entering our side of the map.  By having our agentdefend near the midpoint of the map, we improved our 55% win-rate to a 96% win-rate on the default layoutand averaged a 90% win-rate on random layouts against the baseline agent.  Against double offensive agents,we noticed that our agents performed well against enemies that charged through the middle of the map.However, the performance of our agents were mediocre when the enemy agents charged through the top andbottom parts of the map simultaneously

#### 5.2  Lessons Learned

We  learned that  we  should have designed a feature that accounted  for  the  part  of  the  map  the  ene-mies  were  charging  through,  and  defend  that  area instead of only  telling our agent to defend the mid-point.  Unfortunately, due to the late realization of this problem, we were not able to implement a feature that allowed our agent to play better defense. Additionally, we learned that Alpha-Beta Pruning and Approximate QLearning performed extremely bad when there are a lot of varying constraints in the prob-lem. Overall, from this project, we learned that the simplest approaches to solving a problem was often thebest approach given the constraints of the Capture the Flag Tournament.  If we had realized that generatinguseful data such as choke points would allow us to design smarter features, we would have started imple-menting methods to generate the data instead of wasting time on implementing a complex algorithm thatwas doomed from the start.

### In Action

![](https://github.com/oasysokubo/pacAI/blob/master/img/000.gif)
![](https://github.com/oasysokubo/pacAI/blob/master/img/001.gif)
![](https://github.com/oasysokubo/pacAI/blob/master/img/002.gif)
![](https://github.com/oasysokubo/pacAI/blob/master/img/003.gif)
![](https://github.com/oasysokubo/pacAI/blob/master/img/004.gif)
![](https://github.com/oasysokubo/pacAI/blob/master/img/005.gif)
![](https://github.com/oasysokubo/pacAI/blob/master/img/006.gif)
![](https://github.com/oasysokubo/pacAI/blob/master/img/007.gif)
![](https://github.com/oasysokubo/pacAI/blob/master/img/008.gif)
![](https://github.com/oasysokubo/pacAI/blob/master/img/009.gif)
![](https://github.com/oasysokubo/pacAI/blob/master/img/010.gif)
![](https://github.com/oasysokubo/pacAI/blob/master/img/011.gif)
![](https://github.com/oasysokubo/pacAI/blob/master/img/012.gif)
![](https://github.com/oasysokubo/pacAI/blob/master/img/013.gif)
![](https://github.com/oasysokubo/pacAI/blob/master/img/014.gif)

### FAQ

**Q:** What version of Python does this project support?  
**A:** Python >= 3.5.
The original version of this project was written for Python 2, but it has since been updated.

**Q:** What dependencies do I need for this project?  
**A:** This project has very limited dependencies.
The pure Python dependencies can be installed via pip and are all listed in the requirements file.
These can be installed via: `pip3 install --user -r requirements.txt`.
To use a GUI, you also need `Tk` installed.
The process for installing Tk differs depending on your OS, instructions can be found [here](https://tkdocs.com/tutorial/install.html).

**Q:** How do I run this project?  
**A:** All the binary/executables for this project are located in the `pacai.bin` package.
You can invoke them from this repository's root directory (where this file is located) using a command like:
```
python3 -m pacai.bin.pacman
```


#### Pulling Changes from This Repo Into Your Fork

Occasionally, you may need to pull changes/fixes from this repository.
Doing so is super easy.
Just do a `git pull` command and specify this repository as an argument:
```
git pull https://github.com/linqs/pacman.git
```

### Acknowledgements

This project has been built up from the work of many people.
Here are just a few that we know about:
 - The Berkley AI Lab for starting this project. Primarily John Denero and Dan Klein.
 - Barak Michener for providing the original graphics and debugging help.
 - Ed Karuna for providing the original graphics and debugging help.
 - Jeremy Cowles for implementing an initial tournament infrastructure.
 - LiveWires for providing some code from a Pacman implementation (used / modified with permission).
 - The LINQS lab from UCSC.

 Fucntionalities Added:
 - Added tests.
 - Fixed several bugs.
 - Generalized and reorganized several project elements.
 - Replaced the graphics systems.
 - Added the ability to generate gifs from any pacman or capture game.
