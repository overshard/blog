# Generated by Django 4.0.5 on 2022-06-11 05:33

from django.db import migrations
import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_blogindexpage_cover_image_blogpostpage_cover_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogindexpage',
            name='body',
            field=wagtail.fields.StreamField([('rich_text', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('code', wagtail.blocks.StructBlock([('language', wagtail.blocks.ChoiceBlock(choices=[('python', 'Python'), ('javascript', 'Javascript'), ('htmlmixed', 'HTML'), ('css', 'CSS'), ('shell', 'Shell')])), ('text', wagtail.blocks.TextBlock())])), ('embed', wagtail.embeds.blocks.EmbedBlock())], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='blogpostpage',
            name='body',
            field=wagtail.fields.StreamField([('rich_text', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('code', wagtail.blocks.StructBlock([('language', wagtail.blocks.ChoiceBlock(choices=[('python', 'Python'), ('javascript', 'Javascript'), ('htmlmixed', 'HTML'), ('css', 'CSS'), ('shell', 'Shell')])), ('text', wagtail.blocks.TextBlock())])), ('embed', wagtail.embeds.blocks.EmbedBlock())], blank=True, use_json_field=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.StreamField([('rich_text', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('code', wagtail.blocks.StructBlock([('language', wagtail.blocks.ChoiceBlock(choices=[('python', 'Python'), ('javascript', 'Javascript'), ('htmlmixed', 'HTML'), ('css', 'CSS'), ('shell', 'Shell')])), ('text', wagtail.blocks.TextBlock())])), ('embed', wagtail.embeds.blocks.EmbedBlock())], blank=True, use_json_field=True),
        ),
    ]
