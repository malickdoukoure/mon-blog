from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_merge_0002_article_image_article_likes_0002_article_slug_category_slug_alter_article_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="article",
            name="likes",
        ),
    ]
