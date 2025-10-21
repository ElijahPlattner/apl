from django.db import migrations
import csv
from pathlib import Path

def load_lexicon_data(apps, schema_editor):
    Lexicon = apps.get_model(app_label='api', model_name='Lexicon')
    
    csv_path = Path("/Users/elijahplattner/Downloads/Lexicon/words_219k_m3314.csv")
    if not csv_path.exists():
        print(f"⚠️  CSV file not found at {csv_path}")
        return

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        objs = []
        for row in reader:
            objs.append(Lexicon(
                rank=int(row["rank"]),
                word=row["word"],
                freq=int(row["freq"]) if row["freq"] else None,
                num_texts=int(row["num_texts"]) if row["num_texts"] else None,
                perc_caps=float(row["perc_caps"]) if row["perc_caps"] else None,
                blog=int(row["blog"]) if row["blog"] else None,
                web=int(row["web"]) if row["web"] else None,
                tvm=int(row["tvm"]) if row["tvm"] else None,
                spok=int(row["spok"]) if row["spok"] else None,
                fic=int(row["fic"]) if row["fic"] else None,
                mag=int(row["mag"]) if row["mag"] else None,
                news=int(row["news"]) if row["news"] else None,
                acad=int(row["acad"]) if row["acad"] else None,
                blog_pm=float(row["blog_pm"]) if row["blog_pm"] else None,
                web_pm=float(row["web_pm"]) if row["web_pm"] else None,
                tvm_pm=float(row["tvm_pm"]) if row["tvm_pm"] else None,
                spok_pm=float(row["spok_pm"]) if row["spok_pm"] else None,
                fic_pm=float(row["fic_pm"]) if row["fic_pm"] else None,
                mag_pm=float(row["mag_pm"]) if row["mag_pm"] else None,
                news_pm=float(row["news_pm"]) if row["news_pm"] else None,
                acad_pm=float(row["acad_pm"]) if row["acad_pm"] else None,
                apl_class=row["apl_class"]
            ))

        Lexicon.objects.bulk_create(objs, batch_size=2000)
        print(f"✅ Loaded {len(objs)} lexicon entries.")

def unload_lexicon_data(apps, schema_editor):
    Lexicon = apps.get_model(app_label='api', model_name='Lexicon')
    Lexicon.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.RunPython(load_lexicon_data, reverse_code=unload_lexicon_data),
    ]