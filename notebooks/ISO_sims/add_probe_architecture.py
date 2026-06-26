import yaml
from pathlib import Path

probe_name = ["lensing", "mflike", "multigaussian_mflike_lensing"]
DEFAULTS_DIR = Path("defaults")

def write_yaml(dict, output):
    if Path(output).exists() == False:
        with open(output, "w") as outfile:
            yaml.dump(dict, outfile, default_flow_style=False)

for probe in probe_name:
    write_yaml({"params":{}}, DEFAULTS_DIR / f"parameters/probe_cosmo/cosmo_{probe}.yaml")
    write_yaml({"camb":{}}, DEFAULTS_DIR / f"theory/probe_camb/camb_{probe}.yaml")
    write_yaml({"classy":{}}, DEFAULTS_DIR / f"theory/probe_class/class_{probe}.yaml")

