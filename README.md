Of course. Here is a `README.md` file suitable for GitHub, based on the Python script you provided. It explains the game's concept, setup instructions, how to play, and how to customize it.

-----

# Swipe Quest

A simple card-swiping adventure game built with Python and Pygame, inspired by the mechanics of the game *Reigns*. As a ruler, you are presented with a series of events and must make decisions by swiping left or right. Each choice has consequences, affecting your kingdom's core stats.

*(Note: You can replace this with a screenshot of your actual game)*

## About The Game

In Swipe Quest, you must balance three key resources: **Energy**, **Money**, and **Time**. Every card presents a scenario, and your choice will either increase or decrease these stats. The goal is to survive for as long as possible by making wise decisions. If any of your resource gauges become completely full or completely empty, your reign ends\!

## Features

  * **Simple, Engaging Gameplay**: Easy to learn, difficult to master. Just use the arrow keys to make your choice.
  * **Resource Management**: Carefully balance the three gauges to prolong your rule.
  * **Dynamic Previews**: Hover your mouse over the left or right side of the screen to see the potential outcome of your choice before you commit.
  * **Persistent High Score**: The game saves your best score, challenging you to beat your previous record.
  * **Image Support**: Each card can have a unique image to enhance the story.
  * **Easily Extensible**: Add your own cards, scenarios, and consequences by simply editing the `CARDS` list in the Python script.

## Requirements

  * Python 3.x
  * Pygame library

## Installation & Setup

1.  **Clone the repository (or download the files):**

    ```bash
    git clone https://github.com/your-username/SwipeQuest.git
    cd SwipeQuest
    ```

2.  **Install Pygame:**

    ```bash
    pip install pygame
    ```

3.  **Create the `images` folder:**
    The script expects a folder named `images` in the same directory as `PySwipe.py`. You must create this folder and place all the required `.png` image files inside it.

    The script references the following images:
    `dragon.png`, `merchant.png`, `king.png`, `mushroom.png`, `circus.png`, `duel.png`, `wizard.png`, `tavern.png`, `trade_route.png`, `famine.png`, `alchemist.png`, `bards.png`, `library.png`, `plague.png`, `diplomat.png`, `miners.png`, `philosophy.png`, `thief.png`, `sabotage.png`, `artifact.png`, `guard.png`, `artist.png`, `plot.png`, `technology.png`, `protest.png`, `box.png`, `explorer.png`, `ghost.png`, `comet.png`, `spring.png`, `university.png`, `society.png`, `prophecy.png`, `friend.png`, `shipwreck.png`, `nomads.png`, `beast.png`, `storm.png`, `leader.png`, `treasure.png`, `spies.png`, `celestial.png`, `gladiator.png`, `continent.png`, `hermit.png`, `taxes.png`, `blacksmith.png`, `guild.png`, `rebellion.png`.

    **Note:** If an image is missing, the game will still run, but the space for the image on the card will be blank.

## How to Play

1.  **Run the script from your terminal:**

    ```bash
    python PySwipe.py
    ```

2.  **Make choices:**

      * Press the **Left Arrow Key** to choose the left option ("Deny").
      * Press the **Right Arrow Key** to choose the right option ("Agree").

3.  **Survive:**
    Watch your gauges at the top of the screen. Your game ends if any of them drop to 0 or rise to 100. Try to last as many turns (cards) as possible\!

## Project Structure

Your project folder should look like this for the game to run correctly:

```
SwipeQuest/
├── PySwipe.py
├── highscore.txt      (This file is created automatically after your first game)
├── README.md
└── images/
    ├── dragon.png
    ├── merchant.png
    └── ... (and all other card images)
```

## Customization: Adding New Cards

You can easily add your own scenarios to the game. Open `PySwipe.py` and find the `CARDS` list. Each card is a Python dictionary with the following structure:

```python
{
    "text": "A new scenario for the player to read.",
    "right_effects": {"energy": 10, "money": -20, "time": 5},
    "left_effects": {"energy": -5, "money": 0, "time": -10},
    "image": "images/your_new_image.png"
}
```

  * `"text"`: The description of the event.
  * `"right_effects"`: A dictionary of stat changes if the player swipes right. Positive numbers increase the stat, negative numbers decrease it.
  * `"left_effects"`: A dictionary of stat changes if the player swipes left.
  * `"image"`: The path to the image for this card. Remember to add the corresponding image file to your `images` folder.

Simply add a new dictionary to the `CARDS` list to expand the game\!

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
