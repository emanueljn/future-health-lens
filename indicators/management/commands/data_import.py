# from django.core.management.base import BaseCommand
# from indicators.models import Indicator, IndicatorValue
# from indicators.utils import download_data, INDICATORS
#
# class Command(BaseCommand):
#     help = "Importa dados da WHO para o banco"
#
#     def handle(self, *args, **kwargs):
#         df = download_data()
#         if df.empty:
#             self.stdout.write("Nenhum dado encontrado.")
#             return
#
#         for name, code in INDICATORS.items():
#             indicator, _ = Indicator.objects.get_or_create(nome=name, codigo=code)
#
#         for _, row in df.iterrows():
#             ind = Indicator.objects.get(nome=row["indicator"])
#             IndicatorValue.objects.update_or_create(
#                 indicador=ind,
#                 ano=row["year"],
#                 pais=row["contry"],
#                 defaults={"value": row["value"]}
#             )
#
#         self.stdout.write("Dados importados com sucesso.")