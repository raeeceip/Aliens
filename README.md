# Alien Invasion PC Game

This is a realisation of Space Invaders Project from Eric Matthes' Python Crash Course, 2nd Edition, with some improvements.

## Installation

1. ```git clone https://github.com/kseniaglivko/Alien_Invasion_Game.git```

2. ```cd  /path/to/main.py```

3. ```python3 main.py```

## Instructions:

- P or Right mouse button click Play Button to start game.
- Right arrow, left arrow to move the ship.
- Space to fire a bullet (five bullets are allowed on the screen at the same time).
- Right Shift to fire a superbullet (one superbullet allowed on the screen).
- Left Shift or Press mute/unmute buttons to turn the sound on and off.
- Q or ESC to quit.

- You may see the number of your lives left in the upper left corner of the screen.
- In the upper left part of the screen there is also a **mute** button.

### Features, added to the original project:

1. Randomly generated starry sky as background.
2. Added one superbullet* that can stay active even after destroing an alien. 
3. Explosion animation; scale of explosion depends on bullet/collision type.
4. Sound effects.
5. Mute and unmute buttons.
6. Modified movement mechanics for aliens: row system changed to random spawn.
7. Aliens shoot lazers.
8. Spaceship health bar added. Health descrease as alien lazers collide with the spaceship.

*Amount of points, given for destroying an alien with a superbullet, is half as much as for destroying an alien with a simple bullet, due to its increased power.
