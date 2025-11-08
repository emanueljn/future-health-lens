from django.core.management.base import BaseCommand
from indicators.etl.fetch_who import fetch_indicator
from indicators.etl.transform import clean_and_interpolate
from indicators.models import Indicator, Country, IndicatorValue

INDICATORS = {
    "expectativa_vida": "WHOSIS_000001",
    "mortalidade_infantil": "MDG_0000000001",
    "vacina_sarampo": "WHS9_86",
    "alcoolismo": "SA_0000001462",
    "tabagismo": "SA_0000001400"
}

class Command(BaseCommand):
    help = "Carrega indicadores WHO para o banco"

    def add_arguments(self, parser):
        parser.add_argument('--country', type=str, help='Country ISO code, ex: BRA', default=None)

    def handle(self, *args, **opts):
        country = opts['country']
        for key, code in INDICATORS.items():
            self.stdout.write(f"Buscando {code} ...")
            df = fetch_indicator(code, country_code=country)
            if df.empty:
                self.stdout.write(self.style.WARNING(f"Sem dados para {code}"))
                continue
            df = clean_and_interpolate(df)
            # Persistir
            indicator_obj, _ = Indicator.objects.get_or_create(code=code, defaults={'name': key})
            for _, row in df.iterrows():
                country_name = row.get('country') or country or 'BRA'
                country_obj, _ = Country.objects.get_or_create(code=country or 'BRA', defaults={'name': country_name})
                IndicatorValue.objects.update_or_create(
                    indicator=indicator_obj,
                    country=country_obj,
                    year=int(row['year']),
                    defaults={'value': None if pd.isna(row['value']) else float(row['value'])}
                )
            self.stdout.write(self.style.SUCCESS(f"Persistidos dados para {code}"))