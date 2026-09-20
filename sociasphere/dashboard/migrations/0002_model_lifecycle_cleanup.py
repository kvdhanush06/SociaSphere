from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="user",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name="posts",
                to="auth.user",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="date_modified",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
