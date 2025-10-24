from api.models import Lexicon

caps_list = set()
common_list = set()
uncommon_list = set()

def load_wordlists():
    """
    Load word lists from the database into memory.
    Called once at Django startup.
    """
    global caps_list, common_list, uncommon_list

    # Example queries – adjust filters as needed
    caps_list = set(Lexicon.objects.filter(category="caps").values_list("word", flat=True))
    common_list = set(Lexicon.objects.filter(category="common").values_list("word", flat=True))
    uncommon_list = set(Lexicon.objects.filter(category="uncommon").values_list("word", flat=True))

    print(f"✅ Loaded {len(caps_list)} caps words, {len(common_list)} common, {len(uncommon_list)} uncommon.")