# %%
import lightgbm as lgb
import matplotlib.pyplot as plt
from loguru import logger
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from best_practices.utils import load_parquet_index

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题

# %%
# 加载数据
PATH_STEP4_OUTPUT = r'D:\Users\Kan\Documents\GitHub\ddump\data3\step4'
df = load_parquet_index(PATH_STEP4_OUTPUT, '2021*.parquet')

# %%
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

# 特征与标签
X = df.drop(columns=drop_columns)
y = df['label_5'].copy()
y[:] = 0
y[df['label_5'] > 0.7] = 1
# y[df['label_5'] < 0.2] = 0
# %%
# 划分测试集与验证集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, shuffle=False)

# %%
lgb_train = lgb.Dataset(X_train, y_train, categorical_feature=categorical_feature)
lgb_valid = lgb.Dataset(X_test, y_test, categorical_feature=categorical_feature, reference=lgb_train)

# %%
params = {
    'boosting_type': 'gbdt',

    # 二分类，默认binary_logloss，可用auc
    'objective': 'binary',
    'metric': 'binary_logloss',

    'max_depth': 10,
    'num_leaves': 255,
    'min_data_in_leaf': 10,  # [Warning] No further splits with positive gain, best gain: -inf
    'learning_rate': 0.2,  # 学习率。推荐0.05-0.2
    'feature_fraction': 0.9,  # colsample_bytree 推荐范围：[0.8, 0.9, 1.0]
    'bagging_fraction': 0.8,  # subsample 推荐范围：[0.8, 0.9, 1.0]
    'bagging_freq': 5,  # subsample_freq
    'lambda_l1': 0,  # reg_alpha。搜索范围0~1000。值过大，则说明有一些不必要的特征可以剔除，可以先做特征筛选
    'lambda_l2': 0,  # reg_lambda。推荐0~1000。如果有非常强势的特征，可以人为加大一些reg_lambda使得整体特征效果平均一些，一般会比reg_alpha的数值略大一些
    'verbose': -1,
    'device_type': 'cpu',  # 看情况，有可能gpu更慢
}

# %%

logger.info('开始训练...')
results = {}

# gbm = lgb.Booster(model_file='model.txt') # 可用于预测
gbm = None

gbm = lgb.train(params,
                lgb_train,
                num_boost_round=100,
                valid_sets=(lgb_valid, lgb_train),
                valid_names=('valid', 'train'),
                init_model=gbm,  # 持续学习
                categorical_feature=categorical_feature,
                callbacks=[
                    lgb.log_evaluation(10),
                    lgb.early_stopping(stopping_rounds=20),  # 一般设成num_boost_round的10%
                    lgb.record_evaluation(results),
                    lgb.reset_parameter(learning_rate=lambda iter: max(0.3 * (0.99 ** iter), 0.005))
                ],
                )

# print(gbm.best_score)
# 需要在这里记录下参数，直接加载模型时参数丢失
print('=' * 60)
print(gbm.params)
print('=' * 60)

logger.info('保存模型...')
# save model to file
gbm.save_model('model.txt')

# %%

y_pred_train = gbm.predict(X_train, num_iteration=gbm.best_iteration)
y_pred_test = gbm.predict(X_test, num_iteration=gbm.best_iteration)

# 二分类时，通过概率大小得到分类
y_pred_train = y_pred_train > 0.5
y_pred_test = y_pred_test > 0.5

# auc只能用于二分类，所以这里看精确度
logger.info(f'train accuracy:{accuracy_score(y_train, y_pred_train):.5f}')
logger.info(f'valid accuracy:{accuracy_score(y_test, y_pred_test):.5f}')

# %%
lgb.plot_metric(results)
plt.show()

fig, ax = plt.subplots(1, 2, figsize=(14, 14))
lgb.plot_importance(gbm, ax=ax[0], max_num_features=40)
lgb.plot_importance(gbm, ax=ax[1], importance_type='gain', max_num_features=40)
fig.tight_layout()
plt.show()

# %%
