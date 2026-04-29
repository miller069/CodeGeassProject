"""
dialog_data.py - NPC dialog tree definitions

Author: Ibrahim Chatila
Date:   2026-04-26
Lab:    Lab 7 - NPC Dialog with Graphs

NPC_DATA format
---------------
Each entry is a dict with these keys:

    "name"       : str  — displayed in the dialog box header
    "grid_x"     : int  — tile column on the map
    "grid_y"     : int  — tile row on the map
    "sprite_name": str  — subfolder name under graphics/npcs/
    "dialog"     : DialogGraph instance (built by a helper function below)
    "ai_handler" : AIHandler | None  — set to an AIHandler for AI nodes
"""

from dialog_graph import DialogGraph

try:
    from ai_npc import AIHandler
    _AI_AVAILABLE = True
except Exception:
    _AI_AVAILABLE = False


# ---------------------------------------------------------------------------
# NPC 1 — Town Elder
# Demonstrates: branching tree, loop back, end node.
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

    # Branching from greet
    dg.add_choice("greet",   "quest",    "Tell me about the quest.")
    dg.add_choice("greet",   "lore",     "What can you tell me about this place?")
    dg.add_choice("greet",   "farewell", "Nothing, thanks. Goodbye.")
    # Quest branch
    dg.add_choice("quest",   "accept",   "I'll look into it.")
    dg.add_choice("quest",   "decline",  "That sounds too dangerous for now.")
    # Lore loops back to greet (loop example)
    dg.add_choice("lore",    "greet",    "Interesting. What else can you tell me?")
    dg.add_choice("lore",    "farewell", "Thank you, elder.")
    # End branches
    dg.add_choice("accept",  "farewell", "Farewell.")
    dg.add_choice("decline", "farewell", "Farewell.")

    dg.set_start("greet")
    return dg


# ---------------------------------------------------------------------------
# NPC 2 — Merchant
# Demonstrates: shop loop, multi-branch item menu, end node.
# ---------------------------------------------------------------------------

def _make_merchant():
    dg = DialogGraph("Merchant")

    dg.add_dialog_node(
        "menu",
        "Welcome, traveller! I have wares for every need. What can I get you?"
    )
    dg.add_dialog_node(
        "potions",
        "I've got Healing Potions for 50 gold and Antidotes for 30 gold. "
        "Stock up before heading into the wilds!"
    )
    dg.add_dialog_node(
        "weapons",
        "Finest steel in the region! Iron Sword — 120 gold. "
        "Short Bow — 90 gold. Dagger — 45 gold."
    )
    dg.add_dialog_node(
        "haggle",
        "Ha! You drive a hard bargain. Fine — I'll knock off ten gold "
        "on your next purchase. Don't tell the guild."
    )
    dg.add_dialog_node(
        "no_gold",
        "Come back when your purse is heavier, friend. "
        "Good things cost good coin."
    )
    dg.add_dialog_node(
        "farewell",
        "May fortune smile on you! Come again.",
        node_type="end"
    )

    # Main menu branches (branching requirement)
    dg.add_choice("menu",     "potions",  "Show me your potions.")
    dg.add_choice("menu",     "weapons",  "What weapons do you have?")
    dg.add_choice("menu",     "farewell", "Nothing today, thanks.")

    # From potions: loop back to menu or haggle
    dg.add_choice("potions",  "haggle",   "Those prices seem steep...")
    dg.add_choice("potions",  "menu",     "Let me look at something else.")   # loop
    dg.add_choice("potions",  "farewell", "I'll pass for now.")

    # From weapons: loop back to menu or leave
    dg.add_choice("weapons",  "no_gold",  "I can't afford any of that.")
    dg.add_choice("weapons",  "menu",     "Let me see what else you have.")   # loop
    dg.add_choice("weapons",  "farewell", "Thanks, I'll think about it.")

    # After haggle: back to menu (loop)
    dg.add_choice("haggle",   "menu",     "Alright, let me pick something.")
    dg.add_choice("haggle",   "farewell", "I'll remember that. Farewell.")

    # After no-gold: back to menu or leave
    dg.add_choice("no_gold",  "menu",     "Actually, let me check again.")
    dg.add_choice("no_gold",  "farewell", "Fair enough. Goodbye.")

    dg.set_start("menu")
    return dg


# ---------------------------------------------------------------------------
# NPC 3 — Elara the Sage
# Demonstrates: AI node for open-ended wisdom questions.
# ---------------------------------------------------------------------------

def _make_sage():
    dg = DialogGraph("Elara the Sage")

    dg.add_dialog_node(
        "intro",
        "Ah, a seeker of knowledge! I am Elara. I have studied these lands "
        "for fifty years. What would you know?"
    )
    dg.add_dialog_node(
        "lore_monsters",
        "The creatures to the north are known as Shadewalkers — beings born "
        "from corrupted ley lines. Light weakens them; fire banishes them."
    )
    dg.add_dialog_node(
        "lore_magic",
        "Magic flows through three streams: the Arcane, drawn from the mind; "
        "the Divine, granted by faith; and the Primal, taken from nature itself."
    )
    dg.add_dialog_node(
        "wisdom",
        "(Elara considers your question carefully...)",
        node_type="ai"
    )
    dg.add_dialog_node(
        "thanks",
        "Knowledge freely shared grows stronger for the sharing. Return "
        "any time your curiosity stirs.",
        node_type="end"
    )

    # Branching from intro
    dg.add_choice("intro",          "lore_monsters", "Tell me about the creatures out there.")
    dg.add_choice("intro",          "lore_magic",    "How does magic work in this world?")
    dg.add_choice("intro",          "wisdom",        "I have a question for you...")
    dg.add_choice("intro",          "thanks",        "I think I know enough. Farewell.")

    # From monster lore: loop back or go to AI
    dg.add_choice("lore_monsters",  "wisdom",        "I have another question...")
    dg.add_choice("lore_monsters",  "intro",         "Tell me something else.")          # loop
    dg.add_choice("lore_monsters",  "thanks",        "That's all I needed. Thank you.")

    # From magic lore: loop back or go to AI
    dg.add_choice("lore_magic",     "wisdom",        "I have another question...")
    dg.add_choice("lore_magic",     "intro",         "What else can you teach me?")      # loop
    dg.add_choice("lore_magic",     "thanks",        "Fascinating. Thank you, Elara.")

    # After AI wisdom response
    dg.add_choice("wisdom",         "intro",         "That's helpful — what else do you know?")  # loop
    dg.add_choice("wisdom",         "thanks",        "Thank you, that's all I needed.")

    dg.set_start("intro")
    return dg


# ---------------------------------------------------------------------------
# AI handlers for Part 4
# ---------------------------------------------------------------------------
# Elara's personality: in-character for a centuries-old fantasy scholar.
sage_ai = AIHandler(
    personality=(
        "You are Elara, an ancient sage in a fantasy RPG world. "
        "You have spent fifty years studying the arcane arts, monster lore, "
        "and the history of this land. You speak with calm, poetic authority — "
        "never rushed, never flustered. Weave in references to the Arcane, "
        "Divine, and Primal streams of magic when relevant. "
        "Keep your answer to 2-3 sentences and stay fully in character."
    )
) if _AI_AVAILABLE else None


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
        "name":        "Merchant",
        "grid_x":      20,
        "grid_y":       8,
        "sprite_name": "merchant",
        "dialog":      _make_merchant(),
        "ai_handler":  None,
    },
    {
        "name":        "Elara the Sage",
        "grid_x":      15,
        "grid_y":      14,
        "sprite_name": "sage",
        "dialog":      _make_sage(),
        "ai_handler":  sage_ai,
    },
]
