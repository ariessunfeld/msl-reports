# msl-reports

# Install
`pip install dist/msl_reports-0.0.0-py3-none-any.whl`

# Usage
```
import mslreports
from mslreports import ChemCamSPUL
mslreports.config.username = os.getenv("JPL_USERNAME")
mslreports.config.password = os.getenv("JPL_PASSWORD")
mslreports.connect()

rp = ChemCamSPUL.get_report(sol=3940)
print(rp.contacts)
print(dir(rp)) # see all attributes
```
