# For step by step instructions, view the README.md file in the root directory

import pandas as pd
import numpy as np

y1 = pd.read_csv(r'supporting.files\Bdistachyon_314_v3.1.annotation_info.txt', sep="\t", header=0)
pd.set_option('display.max_columns', None)
len(y1.index)

