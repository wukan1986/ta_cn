import lightgbm as lgb
import matplotlib.pyplot as plt
import numpy as np
from loguru import logger
from sklearn.metrics import r2_score

from best_practices.utils import load_parquet_index

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题

# 加载数据
PATH_STEP4_OUTPUT = r'D:\Users\Kan\Documents\GitHub\ddump\data3\step4'
# 换了个年份
df = load_parquet_index(PATH_STEP4_OUTPUT, '2022*.parquet')

# X中要排除的特征。
# 1. 标注需要排除
# 2. 未来函数需要排除
drop_columns = ['high_limit', 'low_limit', 'pre_close', 'paused', 'factor', 'pct',
                'returns_1', 'returns_5', 'returns_10',
                'label_1', 'label_5', 'label_10',
                ]

# 分类特征
categorical_feature = ['涨停', '曾涨停', '跌停', '曾跌停', '一字板', 'T字板',
                       'industry', 'MA金叉', ]


# 根据时间排序
df = df.sort_index(level=[1])

# 特征与标签，需要按情况进行调整
X = df.drop(columns=drop_columns)
y = df['label_5'].copy()
y[:] = 0
y[df['label_5'] > 0.7] = 1
# y[df['label_5'] < 0.2] = 0

# 划分测试集与验证集，换到新的年份，全做为测试集
X_test, y_test = X, y

lgb_valid = lgb.Dataset(X_test, y_test, categorical_feature=categorical_feature)

gbm = lgb.Booster(model_file='model.txt')  # 可用于预测

y_pred_test = gbm.predict(X_test, num_iteration=gbm.best_iteration)

# 这里需要按情况进行选择
if False:
    # 多分类时，通过argmax得到最大可能性的分类位置
    y_pred_test = np.argmax(y_pred_test, axis=1)

    # # 二分类时，通过概率大小得到分类
    # y_pred_test = y_pred_test > 0.5

    # auc只能用于二分类，所以这里看精确度
    logger.info(f'valid accuracy:{accuracy_score(y_test, y_pred_test):.5f}')
else:
    # 回归时，评价
    logger.info(f'valid r2:{r2_score(y_test, y_pred_test):.5f}')

    # 应当看每天的IC才对，而不是全体IC
    logger.info(f'valid ic:{np.corrcoef(np.vstack((y_test, y_pred_test)))[0, 1]:.5f}')

# %%


fig, ax = plt.subplots(1, 2, figsize=(14, 14))
lgb.plot_importance(gbm, ax=ax[0], max_num_features=40)
lgb.plot_importance(gbm, ax=ax[1], importance_type='gain', max_num_features=40)
fig.tight_layout()
plt.show()

# %%
