import lightgbm as lgb
import matplotlib.pyplot as plt
import optuna
from optuna.integration import LightGBMPruningCallback
from optuna.pruners import MedianPruner
from optuna.visualization.matplotlib import plot_optimization_history, plot_intermediate_values
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from best_practices.utils import load_parquet_index

# 加载数据
PATH_STEP4_OUTPUT = r'D:\Users\Kan\Documents\GitHub\ddump\data3\step4'
df = load_parquet_index(PATH_STEP4_OUTPUT, '2020*.parquet')

# X中要排除的特征。
# 1. 标注需要排除
# 2. 未来函数需要排除
drop_columns = ['high_limit', 'low_limit', 'pre_close', 'paused', 'factor', 'pct',
                'returns_1', 'returns_5', 'returns_10', ]

# 分类特征
categorical_feature = ['涨停', '曾涨停', '跌停', '曾跌停', '一字板', 'T字板',
                       'industry', 'MA金叉', ]

# 特征与标签
X = df.drop(columns=drop_columns)
y = df['returns_5'] > 0


def objective(trial, X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, shuffle=False)

    lgb_train = lgb.Dataset(X_train, y_train, categorical_feature=categorical_feature)
    lgb_valid = lgb.Dataset(X_test, y_test, categorical_feature=categorical_feature, reference=lgb_train)

    params = {
        'boosting_type': 'gbdt',
        'objective': 'binary',
        'max_depth': 8,
        "metric": "auc",
        'num_leaves': trial.suggest_int("num_leaves", 2, 256, step=5),
        'learning_rate': trial.suggest_float("learning_rate", 0.05, 0.3, step=0.05),  # 学习率。推荐0.05-0.2
        'feature_fraction': 0.9,  # colsample_bytree 推荐范围：[0.8, 0.9, 1.0]
        'bagging_fraction': 0.8,  # subsample 推荐范围：[0.8, 0.9, 1.0]
        'bagging_freq': 5,  # subsample_freq
        'lambda_l1': 0,  # reg_alpha。搜索范围0~1000。值过大，则说明有一些不必要的特征可以剔除，可以先做特征筛选
        'lambda_l2': 0,  # reg_lambda。搜索范围0~1000。如果有非常强势的特征，可以人为加大一些reg_lambda使得整体特征效果平均一些，一般会比reg_alpha的数值略大一些
        'verbose': -1,  # 不显示
        'device_type': 'cpu',
    }

    # 剪枝
    pruning_callback = LightGBMPruningCallback(trial, "auc", "valid")

    gbm = lgb.train(params,
                    lgb_train,
                    num_boost_round=20,
                    valid_sets=(lgb_valid, lgb_train),
                    valid_names=('valid', 'train'),
                    categorical_feature=categorical_feature,
                    callbacks=[pruning_callback],
                    )

    y_pred_test = gbm.predict(X_test, num_iteration=gbm.best_iteration)

    accuracy = accuracy_score(y_test, y_pred_test > 0.5)
    return accuracy


study = optuna.create_study(
    pruner=MedianPruner(n_warmup_steps=5),
    direction='maximize',  # 这需要根据目标函数进行修改为最大auc还是最小binary_logloss
    # 这可实现调优中断后恢复
    study_name="lgb_example", storage="sqlite:///lgb_tune.db", load_if_exists=True,
)

# 可以在这里手动指定一些超参数
# https://optuna.readthedocs.io/zh_CN/latest/tutorial/20_recipes/008_specify_params.html

study.optimize(lambda trial: objective(trial, X, y), n_trials=10)

print('=' * 60)
print("Number of finished trials: {}".format(len(study.trials)))

print("Best trial:")
trial = study.best_trial

print("  Value: {}".format(trial.value))

print("  Params: ")
for key, value in trial.params.items():
    print("    {}: {}".format(key, value))

# 可视化
# https://optuna.readthedocs.io/zh_CN/latest/tutorial/10_key_features/005_visualization.html

plot_optimization_history(study)
plt.show()

plot_intermediate_values(study)
plt.show()
