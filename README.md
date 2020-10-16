# PID Tunning Model

In this assignment, you will use what you have learned in PID tutorials and write an actual PID module inside the skeleton simulator we have provided. Note that this assignment will be conducted with __Python__. The reason is Python provides better and easier plot library and it is generally a good language for data visualization. __Note that python skills are almost not required, we only need you to write few equations, and that is basically same as what you would do in C++__.

> You don't have to study python for this assignment since you are only going to implement a few equations and arithmetic calculations.

## Overview

- [PID Tunning Model](#pid-tunning-model)
  - [Overview](#overview)
  - [Instruction](#instruction)
  - [Environment set up](#environment-set-up)
  - [Code structure](#code-structure)
  - [System Model Feature](#system-model-feature)
  - [Assignment Submission](#assignment-submission)
  - [Grading](#grading)

## Instruction

1. Clone this repository to your local.
2. Follow the [Environment set up guide](#environment-set-up) to set up the environment (dependencies).
3. __Modify `PID.py` (ONLY) and impelement INTEGRAL term and DIFFERENTIAL term of a PID controller__.
4. More specifically, you only need to modify the function `update(self, setPoint, actualValue, lastActualValue)`, ignore the `self` parameter if you don't know what it means (is analogous to `this` in C++). Note that __PROPORTIONAL term__ is already implemented.
5. After you finished implementing the function, run `python ./plot.py` OR `python3 ./plot.py` to run the simulator, you can play with it to see how your implementation performs.
6. Ask us if you have any confusion that want us to clear out for you.

## Environment set up

This project use pyqtgraph as GUI tool so you need to make sure your computer support these requirements.

- Python 2.7, or 3.x
- numpy
- PyQt 4.8+/PySide/PyQt5/PySide2

It's convienient for you to install the last two package using pip

```bash
pip install numpy
pip install PyQt5
```

It's not neccessary to install pyqtgraph since this repository include its library.

## Code structure

- Source files:
  - `Model.py`: class of system model, you can find the formula of the system to help you understand but not neccessary.
  - `PID.py`: class of PID controller
  - `Plot.py`: plot the data and run the main task
- Use `python3 plot.py` to run the program.
- You only need to modify `PID.py`.
- You can read other codes if you are interested, but sorry the code is such a mess.

## System Model Feature

- actual value decay
- delay

Understand the feature of the system may be helpful when you tune the parameters.

## Assignment Submission

- As usual, push your code to your private repo. (First create a directory named `5_PID`)
- Please make sure your code can run without any error. (you can have bugs/incorrect implementation, but at least your code should be runnable)

## Grading

- Has implemented __INTEGRATION term and DIFFERENTIAL__ term and your code is runnable. (50%)
- Your implementation is correct. (50%)
