"""
dialog_data.py - NPC dialog tree definitions

Author: Ryan Miller
Date:   [Date]
Lab:    Lab 7 - NPC Dialog with Graphs
"""

from dialog_graph import DialogGraph
from ai_npc import AIHandler


# ---------------------------------------------------------------------------
# Example NPC 1 — Town Elder
# ---------------------------------------------------------------------------

def _make_town_elder():
    dg = DialogGraph("Town Elder")

    dg.add_dialog_node(
        "greet",
        "Ah, a new face! Welcome to the village. What brings you to my door?"
    )
    dg.add_dialog_node(
        "quest",
        "Dark creatures have been sighted near the old forest to the north. "
        "We need a brave soul to investigate before anyone else goes missing."
    )
    dg.add_dialog_node(
        "lore",
        "This village was founded three centuries ago by a wandering band of "
        "scholars. The great library at the centre holds many forgotten secrets."
    )
    dg.add_dialog_node(
        "accept",
        "Brave and noble! Return to me when you have news. "
        "May the old gods watch over you."
    )
    dg.add_dialog_node(
        "decline",
        "I understand — the path is perilous. Should you change your mind, "
        "the offer stands."
    )
    dg.add_dialog_node("farewell", "Safe travels, adventurer.", node_type="end")

    dg.add_choice("greet",   "quest",    "Tell me about the quest.")
    dg.add_choice("greet",   "lore",     "What can you tell me about this place?")
    dg.add_choice("greet",   "farewell", "Nothing, thanks. Goodbye.")

    dg.add_choice("quest",   "accept",   "I'll look into it.")
    dg.add_choice("quest",   "decline",  "That sounds too dangerous for now.")

    dg.add_choice("lore",    "greet",    "Interesting. What else can you tell me?")
    dg.add_choice("lore",    "farewell", "Thank you, elder.")

    dg.add_choice("accept",  "farewell", "Farewell.")
    dg.add_choice("decline", "farewell", "Farewell.")

    dg.set_start("greet")
    return dg


# ---------------------------------------------------------------------------
# NPC 2 — Angelina (Vendor)
# ---------------------------------------------------------------------------

def _make_angelina():
    dg = DialogGraph("Angelina")

    dg.add_dialog_node("menu", "Welcome salvager! Looking for equipment?")
    dg.add_dialog_node("weapons", "I have laser rifles and plasma blades available.")
    dg.add_dialog_node("armor", "Take a look at these EVA suits.")
    dg.add_dialog_node("bye", "Come back if you find more salvage.", node_type="end")

    dg.add_choice("menu", "weapons", "Show me weapons.")
    dg.add_choice("menu", "armor", "Show me armor.")
    dg.add_choice("menu", "bye", "Nothing right now.")

    dg.add_choice("weapons", "menu", "Let me look at something else.")
    dg.add_choice("armor", "menu", "Let me look at something else.")

    dg.set_start("menu")
    return dg


# ---------------------------------------------------------------------------
# NPC 3 — A-76 (Historian AI)
# ---------------------------------------------------------------------------

def _make_a76():
    dg = DialogGraph("A-76")

    dg.add_dialog_node("intro", "Historical unit A-76 online. Data fragments detected.")
    dg.add_dialog_node("history", "...", node_type="ai")
    dg.add_dialog_node("drives", "Encrypted data drives reveal hidden war records.")
    dg.add_dialog_node("bye", "Archive connection closed.", node_type="end")

    dg.add_choice("intro", "history", "Tell me about the war.")
    dg.add_choice("intro", "drives", "What are encrypted data drives?")
    dg.add_choice("intro", "bye", "Goodbye.")

    dg.add_choice("history", "intro", "Ask something else.")
    dg.add_choice("drives", "intro", "I have another question.")

    dg.set_start("intro")
    return dg


# ---------------------------------------------------------------------------
# AI handlers for Part 4
# ---------------------------------------------------------------------------

a76_ai = AIHandler(
    personality=(
        "You are A-76, a calm robotic historian in a sci-fi RPG. "
        "Explain forgotten events from Galaxy War II. "
        "Keep responses under three sentences."
    )
)


# ---------------------------------------------------------------------------
# NPC_DATA — the game spawns every entry in this list
# ---------------------------------------------------------------------------

NPC_DATA = [
    {
        "name":        "Town Elder",
        "grid_x":      10,
        "grid_y":       5,
        "sprite_name": "town_elder",
        "dialog":      _make_town_elder(),
        "ai_handler":  None,
    },
    {
        "name":        "Angelina",
        "grid_x":      20,
        "grid_y":       8,
        "sprite_name": "angelina",
        "dialog":      _make_angelina(),
        "ai_handler":  None,
    },
    {
        "name":        "A-76",
        "grid_x":      25,
        "grid_y":      14,
        "sprite_name": "a76",
        "dialog":      _make_a76(),
        "ai_handler":  a76_ai,
    },
]