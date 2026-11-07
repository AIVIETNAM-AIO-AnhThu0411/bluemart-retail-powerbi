from pathlib import Path
from core import load_and_prepare, summarize

info=summarize(load_and_prepare(Path(__file__).parent / "data"))
for key,value in info.items():print(f"{key:<16} {value}")
assert info['sales_rows']==641126
assert info['skus']==200
assert info['stores']==50
assert info['date_min']=='2021-01-01'
assert info['date_max']=='2025-10-31'
assert info['campaign_days']==800
assert info['regular_days']==965
assert abs(info['revenue']-73149339.22)<0.1
assert abs(info['gross_profit']-21078696.7)<0.1
print('OK: Blue Mart KPI khop nguon.')
