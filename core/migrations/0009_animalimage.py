from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_animal_adotante'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnimalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to='animal_images/', verbose_name='imagem')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('animal', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='imagens', to='core.animal')),
            ],
            options={
                'verbose_name': 'Imagem do Animal',
                'verbose_name_plural': 'Imagens do Animal',
            },
        ),
    ]
