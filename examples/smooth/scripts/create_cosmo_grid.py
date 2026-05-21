# sample grid parameter file

from cobaya import InputDict
from cobaya.grid_tools.batchjob import DataSet
from cobaya.yaml import yaml_load_file

yaml_folder = "../yamls/"

#######################################################################
# Default dictionary

default: InputDict = {
    "sampler": yaml_load_file(yaml_folder+"mcmc_params.yaml"),
    "params": yaml_load_file(yaml_folder+"params_cosmo_smooth.yaml"),
    "theory": yaml_load_file(yaml_folder+"theory_camb.yaml")
}

defaults = [default]

importance_defaults = []
minimize_defaults = []
getdist_options = {"ignore_rows": 0.3}

#######################################################################
# Likelihoods

MFLike: InputDict = {
        "likelihood": yaml_load_file(yaml_folder+"like_mflike.yaml"),
        "params": yaml_load_file(yaml_folder+"params_mflikefg_smooth.yaml")
        | yaml_load_file(yaml_folder+"params_mflikesyst_smooth.yaml"),
        "theory": yaml_load_file(yaml_folder+"theory_BandpowerForeground.yaml")
    }

LensingLike: InputDict = {
    "likelihood": yaml_load_file(yaml_folder+"like_LensingLikelihood.yaml"),
    "theory": yaml_load_file(yaml_folder+"theory_ccl.yaml")
}

LensingLike_ede = InputDict = {
    "likelihood": yaml_load_file(yaml_folder+"like_LensingLikelihood_camb.yaml")
}

ShearKappaLike: InputDict = {
    "likelihood": yaml_load_file(yaml_folder+"like_shearkappa.yaml"),
    "params": yaml_load_file(yaml_folder+"params_shearkappanuisance_smooth.yaml"),
    "theory": yaml_load_file(yaml_folder+"theory_ccl.yaml")
}

joint1 = DataSet(["MFLike", "LensingLike"], [MFLike, LensingLike])
joint2 = DataSet(["MFLike", "ShearKappaLike"], [MFLike, ShearKappaLike])
joint3 = DataSet(["LensingLike", "ShearKappaLike"], [LensingLike, ShearKappaLike])
joint4 = DataSet(
    ["MFLike", "LensingLike", "ShearKappaLike"], [MFLike, LensingLike, ShearKappaLike]
)
joint1_ede = DataSet(["MFLike", "LensingLike"], [MFLike, LensingLike_ede])

datasets_main = [("MFLike", MFLike),
                 ("LensingLike", LensingLike),
                 ("ShearKappaLike", ShearKappaLike),
                 joint1,
                 joint2,
                 joint3,
                 joint4]

datasets_ede = [("MFLike", MFLike),
                 ("LensingLike", LensingLike_ede),
                 joint1]

#######################################################################
# Models

model_names = ["lcdm", "mnu", "neff", "mnu_neff", "ede"]
models = {}
param_extra_opts = {}
for m in model_names:
    elts = m.split("_")
    models[m] = {"params":{}, "theory":{}, "mcmc":{}}
    for e in elts:
        yaml_model = yaml_load_file(yaml_folder+f"{e}.yaml")
        if "params" in yaml_model:
            models[m]["params"] = {**models[m]["params"], **yaml_model["params"]}
        if "theory" in yaml_model:
            models[m]["theory"] = {**models[m]["theory"], **yaml_model["theory"]}    
        if "mcmc" in yaml_model:
            models[m]["mcmc"] = {**models[m]["mcmc"], **yaml_model["mcmc"]}    
    if "mnu" not in elts:
        mnu = yaml_load_file(yaml_folder+"mnu_fixed.yaml")
        models[m]["params"] = {**models[m]["params"], **mnu["params"]}

#######################################################################
# Groups

groups = {
    "main": {
        "models": ["lcdm", "mnu", "neff", "mnu_neff"],
        "datasets": datasets_main
    },
    "ede": {
        "models": ["ede"],
        "datasets": datasets_ede
    }
}

#######################################################################
# Pre-computed covariances

cov_dir = "output_camb_grid/"
