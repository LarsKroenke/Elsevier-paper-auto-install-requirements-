import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math
import pint
import pint_pandas
import latexify
import scienceplots
import pubchempy as pcp
from IPython.display import display
from custom_functions.data_frame_to_latex import df_to_tex
from custom_functions.matplotlib_to_latex import plot_to_latex
from custom_functions.latexify import latexify_expression
from custom_functions.chemfig import chemfig
from custom_functions.variable import write_variables
# from pint import constants as const
from pint import UnitRegistry, set_application_registry
ureg = UnitRegistry()
Q_ = ureg.Quantity
ureg.formatter.default_format = "P~"

set_application_registry(ureg)

# matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

# plt.style.use(['science', 'grid'])