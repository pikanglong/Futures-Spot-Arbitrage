import pandas as pd

list = []
for r in range(1, 21):
    list_row = []
    for c in range(1, 21):
        # 利润
        # list_row.append(r/(2+r/100)*c)
        # 风险
        # list_row.append(r/100+(2+r/100)/c)
    list.append(list_row)
df = pd.DataFrame(list)
df.index = df.index + 1
l = []
for i in range(1, 21):
    l.append(str(i))
df.columns = l
print(df)