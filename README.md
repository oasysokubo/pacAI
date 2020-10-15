## Pacman

A modified version of the Pacman project from the [Berkeley AI Lab](http://ai.berkeley.edu/project_overview.html) using reinforcement learning.

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
