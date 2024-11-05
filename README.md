# chess_ai
My attempt at making a Chess AI. I have an idea for a custom DNN with piece specific convolutions that I want to try.

I will be using some chess openings books to make custom openings tables, writing a Deep Convolutional Neural Network to evaluate positions, and a minimax tree search.

So far I have:

    agent.py - Simple agent for making moves

    eval.py - For scoring games (including those that hit the turn limit)

    gym.py - Simple gym for running games

    opening_tree.py - My first attempt at an opening system. (will be revamped to use the opening_db)

    utils.py - Utility functions mostly to transform board states between different representational formats

    test.ipynb - Jupyter Notebook for quick iteration

    gui.py - Currently mostly a copy-paste from a tutorial. I will incorporate it with my other components for ease of interaction with the system.


What I'm working on:

    - Custom openings tables from chess books representing my personal opening system.

    - Custom Deep Convolutional Neural Network to evaluate positions

    - minimax tree search and all the tricks to improve efficiency

    - Incorporating into a personal website on GitHub Pages (coming soon)
