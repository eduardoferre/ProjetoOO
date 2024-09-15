from maindudu.models import Automovel

ids = Automovel.objects.values_list('_id', flat=True)

print("Todos os IDs dos Automovels:")
for id in ids:
    print(id)
