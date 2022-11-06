from itertools import product

import matplotlib.pyplot as plt
import pandas as pd
import parmap
from loguru import logger

from best_practices.calc import calc_ts, calc_cs, calc_col, calc_cs2, func_prepare
from best_practices.utils import load_parquet_index, func_load_calc_save, dataframe_calc, dataframe_save, \
    func_load_index_column, func_load_index, describe_win, timer

# 行范围，字符串，只用在文件名上
# 分钟数据太大，可改为按月划分
RANGE_I = pd.date_range('2020-01-01', '2022-12-31', freq='Y')
RANGE_I = [f'{i:%Y}' for i in RANGE_I]

# 列范围，字符串，只用在文件名上
# 横向10组在数据量大时也比较慢，可改为20组，50组等
RANGE_J = [f'{i:02d}' for i in range(10)]

# 数据源路径
PATH_STEP1_INPUT1 = r'data\jqresearch\get_price_stock_daily'
PATH_STEP1_INPUT2 = r'data\jqresearch\get_price_stock_factor'
# 中间过程路径。可以考虑这部分保存到共享内存或内存盘中，加快速度
PATH_STEP1_OUTPUT = r'data\step1'
PATH_STEP2_OUTPUT_TS = r'data\step2_ts'
PATH_STEP2_OUTPUT_CS = r'data\step2_cs'
PATH_STEP3_OUTPUT_CS = r'data\step3_cs'
# 演示将分离出的数据再合并
PATH_STEP4_OUTPUT = r'data\step4'

# 数据源路径
PATH_STEP1_INPUT1 = r'D:\Users\Kan\Documents\GitHub\ddump\data\jqresearch\get_price_stock_daily'
PATH_STEP1_INPUT2 = r'D:\Users\Kan\Documents\GitHub\ddump\data\jqresearch\get_price_stock_factor'
# 中间过程路径。可以考虑这部分保存到共享内存或内存盘中，加快速度
PATH_STEP1_OUTPUT = r'D:\Users\Kan\Documents\GitHub\ddump\data3\step1'
PATH_STEP2_OUTPUT_TS = r'D:\Users\Kan\Documents\GitHub\ddump\data3\step2_ts'
PATH_STEP2_OUTPUT_CS = r'D:\Users\Kan\Documents\GitHub\ddump\data3\step2_cs'
PATH_STEP3_OUTPUT_CS = r'D:\Users\Kan\Documents\GitHub\ddump\data3\step3_cs'
# 演示将分离出的数据再合并
PATH_STEP4_OUTPUT = r'D:\Users\Kan\Documents\GitHub\ddump\data3\step4'


@timer
def step1():
    """计算技术指标，并提取用来算横截面的字段"""

    ii = RANGE_I
    jj = ['*']
    parmap.map(func_load_calc_save,
               product(ii, jj),
               load_func=func_load_index_column, load_kwargs=
               {
                   'left_path': PATH_STEP1_INPUT1,
                   'right_path': PATH_STEP1_INPUT2,
                   'left_pattern': '{0}*',
                   'right_pattern': '{0}*',
                   # 源数据来自聚宽，股票代码和时间如下
                   'left_on': ['code', 'time'],
                   'right_on': ['code', 'time'],
               },
               calc_func=func_prepare, calc_args=[],
               save_func=dataframe_save, save_args=
               [
                   {'split_axis': 1, 'path': PATH_STEP1_OUTPUT, 'exclude': []},  # 上流输入`三`型，输出转`田`型
               ],
               pm_processes=len(ii),
               pm_parallel=True)


@timer
def step2():
    """计算技术指标，并提取用来算横截面的字段"""

    ii = ['*']
    jj = RANGE_J  # [0:1]
    parmap.map(func_load_calc_save,
               product(ii, jj),
               load_func=func_load_index, load_kwargs={'path': PATH_STEP1_OUTPUT, },
               calc_func=dataframe_calc, calc_args=
               [
                   {'groupby': None, 'func': calc_col},  # 整列计算
                   {'groupby': 'asset', 'func': calc_ts},  # 时序计算
               ],
               save_func=dataframe_save, save_args=
               [
                   {'split_axis': 0, 'path': PATH_STEP2_OUTPUT_TS, 'exclude': ['close', 'amount']},
                   {'split_axis': 0, 'path': PATH_STEP2_OUTPUT_CS, 'include': ['close', 'amount']},
               ],
               pm_processes=len(jj) // 3,  # IO瓶颈，内存不足
               pm_parallel=True)


@timer
def step3():
    """计算截面指标"""

    # 10进程处理
    ii = RANGE_I
    jj = ['*']
    parmap.map(func_load_calc_save,
               product(ii, jj),
               load_func=func_load_index, load_kwargs=
               {
                   'path': PATH_STEP2_OUTPUT_CS,
                   'columns': None,  # 指定这一阶段要加载的数据，减少内存
               },
               calc_func=dataframe_calc, calc_args=
               [
                   {'groupby': 'date', 'func': calc_cs},  # 横截面
                   {'groupby': ['date', 'industry'], 'func': calc_cs2},  # 行业分组横截面
               ],
               save_func=dataframe_save, save_args=
               [
                   {'split_axis': 1, 'path': PATH_STEP3_OUTPUT_CS, 'exclude': []},  # 输入`三`型，输出转`田`型
               ],
               pm_processes=len(ii),
               pm_parallel=True)


@timer
def step4():
    """试着将TS与CS数据合并，可以不合，看需求，这里只是为了做演示

    没计算只合并就花了15秒
    """
    # 10进程处理
    ii = ['*']
    jj = RANGE_J
    parmap.map(func_load_calc_save,
               product(ii, jj),
               load_func=func_load_index_column, load_kwargs=
               {
                   'left_path': PATH_STEP2_OUTPUT_TS,
                   'right_path': PATH_STEP3_OUTPUT_CS,
                   'left_pattern': '{0}__{1}.*',
                   'right_pattern': '{0}__{1}.*',
                   # 内部已经统一了股票代码和时间日期
                   'left_index': True,
                   'right_index': True,
               },
               calc_func=None, calc_args=[],
               save_func=dataframe_save, save_args=
               [
                   {'split_axis': 0, 'path': PATH_STEP4_OUTPUT, 'exclude': []},  # 输入`三`型，输出转`田`型
               ],
               pm_processes=len(jj) // 3,  # 内存不够，少启动几个进程
               pm_parallel=True)


# @timer
def step5():
    """统计部分指标"""
    df = load_parquet_index(PATH_STEP2_OUTPUT_TS,
                            '*__00.*',  # 先只加载第0组，看看结果如何，之后需要全看
                            columns=None)
    label = ['returns_1', 'returns_5', 'returns_10']
    y = describe_win(df[df['MA金叉']][label])
    print(y)

    # 可以在多进程部分处理，但那里是比较固定的模式，因为生成东西多
    # 这里测试临时想法，稳定后移动到那
    df['rank_20'] = df['收盘价20日排序'] * 10 // 2

    # 结论：高位金叉还要再涨
    y = df[df['MA金叉']].groupby(by='rank_20').apply(lambda x: describe_win(x[label]))
    print(y)


def step6():
    """查看结果

    前一步的操作导致生成的数据为`三`型，
        1. 为了展示某支股票全部数据，不得不所有文件同时加载
        2. 如果是为了交易，只需要最后一天的数据即可

    """
    df = load_parquet_index(PATH_STEP4_OUTPUT, '*__03.*')
    d = df.loc[('002093.SZ', slice(None)), :]
    d = d.droplevel(level=0)
    ax = plt.subplot(311)
    d[['close_adj', 'sma_5', 'sma_10', 'sma_20', 'sma_60']].plot(ax=ax)
    ax = plt.subplot(312)
    d[['macd', 'macdsignal', 'macdhist']].plot(ax=ax)
    ax = plt.subplot(313)
    d[['atr_14']].plot(ax=ax)
    plt.show()

    # d.to_excel('1.xlsx')


if __name__ == '__main__':
    # # 原始数据合并
    step1()
    # 计算技术指标
    step2()
    # 计算截面
    step3()
    step4()
    # 查看结果
    step5()
    #
    # step6()

    logger.info('done')
