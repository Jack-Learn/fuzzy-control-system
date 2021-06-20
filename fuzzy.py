import numpy as np
import matplotlib.pyplot as plt
import math
import skfuzzy as fuzzy
from skfuzzy import control as ctrl

# 定義變數範圍
x_age = np.arange(65, 100, 1)
x_times = np.arange(5, 30, 1)
y_score = np.arange(60, 100, 1)

# 定義模糊控制變量
age = ctrl.Antecedent(x_age, 'age')
times = ctrl.Antecedent(x_times, 'times')
score = ctrl.Consequent(y_score, 'score')

# 定義歸屬函數
age['S'] = fuzzy.trimf(x_age, [65, 65, 80])     # 定義三角歸屬函數
age['M'] = fuzzy.trimf(x_age, [65, 80, 100])
age['L'] = fuzzy.trimf(x_age, [80, 100, 100])
times['S'] = fuzzy.trimf(x_times, [5, 5, 15])
times['M'] = fuzzy.trimf(x_times, [5, 15, 30])
times['L'] = fuzzy.trimf(x_times, [15, 30, 30])
score['L'] = fuzzy.trimf(y_score, [60, 60, 80])
score['M'] = fuzzy.trimf(y_score, [60, 80, 100])
score['H'] = fuzzy.trimf(y_score, [80, 100, 100])

# 可視化歸屬函數
# age.automf(names=['Small', 'Medium', 'Large'])
# times.automf(names=['Small', 'Medium', 'Large'])
# score.automf(names=['Low', 'Medium', 'High'])
# age.view()
# times.view()
# score.view()
# plt.show()

# 定義解模糊方法
score.defuzzify_method = 'centroid' # 質心法

# 定義規則
rule1=ctrl.Rule(antecedent=((age['S'] & times['S']) | (age['S'] & times['M'])| (age['M'] & times['S']) | (age['L'] & times['S'])), consequent=score['L'], label='Low')
rule2=ctrl.Rule(antecedent=((age['S'] & times['L']) | (age['M'] & times['M']) | (age['L'] & times['M'])), consequent=score['M'], label='Medium')
rule3=ctrl.Rule(antecedent=((age['M'] & times['L']) | (age['L'] & times['L'])), consequent=score['M'], label='Medium')

# 不知道是什麼
# rule1.view() # install decorator-5.0.5 (Error: random_state_index is incorrect)
# plt.show()


# 測試
score_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
scoring =  ctrl.ControlSystemSimulation(score_ctrl)

scoring.input['age'] = 65
scoring.input['times'] = 20
scoring.compute()
print(scoring.output['score'])
score.view(sim=scoring)
plt.show()
