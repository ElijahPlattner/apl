from django.db import connection
from pathlib import Path
from typing import Optional
import json

# Global hash maps (O(1) lookups)
caps_map = {}
common_map = {}
uncommon_map = {}
looked_up_map = {}
skip_map = {}


def load_all_word_lists():
    """Load all five word lists into memory for instant lookups."""
    global caps_map, common_map, uncommon_map, looked_up_map, skip_map

    print("🔹 Loading word lists into memory...")

    try:
        # Import models here to avoid circular imports
        from .models import Lexicon, LookedUpWords, SkipWords

        # === Lexicon-based lists ===
        caps_qs = Lexicon.objects.filter(perc_caps__gte=0.8)
        common_qs = Lexicon.objects.filter(rank__lte=25000, perc_caps__lt=0.8)
        uncommon_qs = Lexicon.objects.filter(rank__gt=25000, perc_caps__lt=0.8)

        caps_map = {w.word.lower(): True for w in caps_qs}
        common_map = {w.word.lower(): True for w in common_qs}
        uncommon_map = {w.word.lower(): True for w in uncommon_qs}

        # === Other tables ===
        looked_up_map = {w.word.lower(): True for w in LookedUpWords.objects.all()}
        skip_map = {w.word.lower(): True for w in SkipWords.objects.all()}

        print(
            f"✅ Loaded {len(caps_map)} caps, {len(common_map)} common, "
            f"{len(uncommon_map)} uncommon, {len(looked_up_map)} looked_up, {len(skip_map)} skip words."
        )

    except Exception as e:
        print(f"⚠️  Error loading word lists: {e}", flush=True)
