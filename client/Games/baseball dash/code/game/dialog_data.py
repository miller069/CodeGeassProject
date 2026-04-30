"""
dialog_data.py - NPC dialog tree definitions

Author: [Your Name]
Date:   [Date]
Lab:    Lab 7 - NPC Dialog with Graphs

TODO (Part 2)
-------------
Define at least THREE NPCs below, each with a meaningful dialog tree.

Requirements for full credit:
  * At least 3 distinct NPCs (different names, positions, sprites).
  * Each NPC must have at least 4 dialog nodes.
  * At least one NPC must have a BRANCHING tree (a node with 2+ choices
    leading to different destinations).
  * At least one NPC must have a LOOP (an edge that leads back to an
    earlier node, e.g. a merchant menu the player can revisit).
  * At least one NPC must use an AI node connected to Gemini (Part 4).

TODO (Part 4)
-------------
  * Create an AIHandler with a custom personality string.
  * Set at least one dialog node's type to "ai".
  * Add the handler to the matching entry in NPC_DATA.
  * Make sure your GEMINI_API_KEY is set (see ai_npc.py).

NPC_DATA format
---------------
Each entry is a dict with these keys:

    "name"       : str  — displayed in the dialog box header
    "grid_x"     : int  — tile column on the map
    "grid_y"     : int  — tile row on the map
    "sprite_name": str  — subfolder name under graphics/npcs/
    "dialog"     : DialogGraph instance (built by a helper function below)
    "ai_handler" : AIHandler | None  — set to an AIHandler for AI nodes

Adjust grid_x / grid_y so each NPC stands in a walkable area of YOUR map.
"""

from dialog_graph import DialogGraph
from ai_npc import AIHandler


# ---------------------------------------------------------------------------
# NPC 1 — Rival Manager
# ---------------------------------------------------------------------------

def _make_rival_manager():
    dg = DialogGraph("Rival Manager")

    dg.add_dialog_node("intro", "So you're the rookie everyone’s talking about. Think you can beat my team?")
    dg.add_dialog_node("strategy", "We play aggressive baseball—steals, bunts, and pressure every inning.")
    dg.add_dialog_node("taunt", "Hope you brought your best pitcher. You're going to need it.")
    dg.add_dialog_node("accept", "Good. I like confidence. Let’s see if you can back it up.")
    dg.add_dialog_node("decline", "Heh. Maybe you're smarter than you look.")
    dg.add_dialog_node("leave", "Game’s starting soon. Don’t be late.", node_type="end")

    dg.add_choice("intro", "strategy", "What’s your game plan?")
    dg.add_choice("intro", "taunt", "We’ll crush you.")
    dg.add_choice("intro", "leave", "I’ve got nothing to say.")

    dg.add_choice("strategy", "intro", "Got anything else to say?")
    dg.add_choice("taunt", "accept", "Bring it on.")
    dg.add_choice("taunt", "decline", "We’ll see.")

    dg.add_choice("accept", "leave", "See you on the field.")
    dg.add_choice("decline", "leave", "Whatever.")

    dg.set_start("intro")
    return dg


# ---------------------------------------------------------------------------
# NPC 2 — Pitcher (AI node)
# ---------------------------------------------------------------------------

def _make_pitcher():
    dg = DialogGraph("Ace Pitcher")

    dg.add_dialog_node("intro", "Hey, I’m starting today. You need anything before we take the field?")
    dg.add_dialog_node("tips", "Watch the batter’s stance. It tells you everything about their swing.")
    dg.add_dialog_node("warmup", "My arm feels good. Fastball’s got some extra heat today.")
    dg.add_dialog_node("advice", "Ask me anything about pitching.", node_type="ai")
    dg.add_dialog_node("leave", "Alright, time to focus. Let’s win this.", node_type="end")

    dg.add_choice("intro", "tips", "Got any tips?")
    dg.add_choice("intro", "warmup", "How are you feeling?")
    dg.add_choice("intro", "advice", "I need pitching advice.")
    dg.add_choice("intro", "leave", "Let’s play.")

    dg.add_choice("tips", "intro", "Anything else?")
    dg.add_choice("warmup", "intro", "Good to hear.")
    dg.add_choice("advice", "intro", "Thanks.")

    dg.set_start("intro")
    return dg


# ---------------------------------------------------------------------------
# NPC 3 — Vendor (Concessions Stand, LOOP example)
# ---------------------------------------------------------------------------

def _make_vendor():
    dg = DialogGraph("Concessions Vendor")

    dg.add_dialog_node("menu", "Hot dogs! Drinks! Peanuts! What’ll it be?")
    dg.add_dialog_node("hotdog", "Fresh off the grill. Best in the stadium.")
    dg.add_dialog_node("drink", "Ice cold soda to keep you cool.")
    dg.add_dialog_node("peanuts", "Classic ballpark snack.")
    dg.add_dialog_node("buy", "That’ll be a few bucks. Enjoy the game!")
    dg.add_dialog_node("leave", "Come back if you get hungry.", node_type="end")

    dg.add_choice("menu", "hotdog", "I’ll take a hot dog.")
    dg.add_choice("menu", "drink", "Give me a drink.")
    dg.add_choice("menu", "peanuts", "Peanuts please.")
    dg.add_choice("menu", "leave", "Nothing for now.")

    dg.add_choice("hotdog", "buy", "Buy it.")
    dg.add_choice("drink", "buy", "Buy it.")
    dg.add_choice("peanuts", "buy", "Buy it.")

    # LOOP back to menu
    dg.add_choice("buy", "menu", "Anything else?")
    dg.add_choice("buy", "leave", "That’s all.")

    dg.set_start("menu")
    return dg


# ---------------------------------------------------------------------------
# NPC 4 — Fan
# ---------------------------------------------------------------------------

def _make_fan():
    dg = DialogGraph("Super Fan")

    dg.add_dialog_node("intro", "LET’S GO!! You ready for this game?!")
    dg.add_dialog_node("team", "Our team’s been on fire lately. No one can stop us!")
    dg.add_dialog_node("opponent", "The other team? Overrated.")
    dg.add_dialog_node("hype", "This is gonna be the best game of the season!")
    dg.add_dialog_node("leave", "I gotta get back to cheering!", node_type="end")

    dg.add_choice("intro", "team", "How’s the team doing?")
    dg.add_choice("intro", "opponent", "What about the other team?")
    dg.add_choice("intro", "hype", "You seem excited.")
    dg.add_choice("intro", "leave", "Enjoy the game.")

    dg.add_choice("team", "intro", "Nice.")
    dg.add_choice("opponent", "intro", "We’ll see.")
    dg.add_choice("hype", "intro", "I hope so.")

    dg.set_start("intro")
    return dg


# ---------------------------------------------------------------------------
# AI handlers for Part 4
# ---------------------------------------------------------------------------

pitcher_ai = AIHandler(
    personality=(
        "You are a confident professional baseball pitcher. "
        "Give short, practical advice about pitching strategy, mindset, and mechanics. "
        "Speak like a focused athlete."
    )
)


# ---------------------------------------------------------------------------
# NPC_DATA — the game spawns every entry in this list
# ---------------------------------------------------------------------------

NPC_DATA = [
    {
        "name":        "Rival Manager",
        "grid_x":      5,
        "grid_y":      5,
        "sprite_name": "manager",
        "dialog":      _make_rival_manager(),
        "ai_handler":  None,
    },
    {
        "name":        "Ace Pitcher",
        "grid_x":      6,
        "grid_y":      5,
        "sprite_name": "pitcher",
        "dialog":      _make_pitcher(),
        "ai_handler":  pitcher_ai,
    },
    {
        "name":        "Concessions Vendor",
        "grid_x":      7,
        "grid_y":      5,
        "sprite_name": "vendor",
        "dialog":      _make_vendor(),
        "ai_handler":  None,
    },
    {
        "name":        "Super Fan",
        "grid_x":      8,
        "grid_y":      5,
        "sprite_name": "fan",
        "dialog":      _make_fan(),
        "ai_handler":  None,
    },
]