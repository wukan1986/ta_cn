"""
优先实现WorldQuant BRAIN中Fast Expression的函数
然后再实现通达信的函数
"""

from ..wq.arithmetic import abs_ as ABS
from ..wq.arithmetic import add as ADD
from ..wq.arithmetic import divide as DIV
from ..wq.arithmetic import log as LN  # 自然对数
from ..wq.arithmetic import log10 as LOG  # 10为底的对数
from ..wq.arithmetic import max_ as MAX
from ..wq.arithmetic import mean as MEAN
from ..wq.arithmetic import min_ as MIN
from ..wq.arithmetic import multiply as MUL
from ..wq.arithmetic import round_ as ROUND
from ..wq.arithmetic import sign as SGN
from ..wq.arithmetic import subtract as SUB
from ..wq.logical import if_else as IF
from ..wq.time_series import ts_count as COUNT
from ..wq.time_series import ts_delay as REF
from ..wq.time_series import ts_delta as DIFF
from ..wq.time_series import ts_max as HHV
from ..wq.time_series import ts_mean as MA
from ..wq.time_series import ts_min as LLV
from ..wq.time_series import ts_sum as SUM
from ..wq.cross_sectional import rank as RANK

ABS
MAX
MIN
REF
HHV
MA
LLV
SUM
ADD
SUB
MUL
DIV
ROUND
MEAN
LN
LOG
SGN
DIFF
IF
COUNT
RANK
