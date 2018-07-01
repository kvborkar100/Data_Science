import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
df = pd.read_csv('phishing2.csv')
def correlation_matrix(df):
    from matplotlib import pyplot as plt
    from matplotlib import cm as cm

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    cmap = cm.get_cmap('jet', 130)
    cax = ax1.imshow(df.corr(), interpolation="nearest", cmap=cmap)
    ax1.grid(True)
    plt.title('URL Features Correlation')
    labels=df.columns
    ax1.set_xticklabels(labels,fontsize=10)
    ax1.set_yticklabels(labels,fontsize=10)
    fig.colorbar(cax, ticks = [.75,.8,.85,.90,.95,1])
    plt.text()
    plt.show()

def url_behavior_per():
    left = [1, 2]
    prediction = [37.5, 96.25]
    height = [prediction[1], prediction[0]]

    tick_label = ['good', 'bad']

    plt.bar(left, height, tick_label=tick_label,
            width=0.8, color=['green', 'red'])

    plt.xlabel('x - axis')

    plt.ylabel('y - axis')
    plt.axhline(y = 90,color = 'orange',ls = '--')
    plt.axhline(y = 80,color = 'red', ls = '--')
    plt.text(2.5,80,'Bad URL')
    plt.text(2.5,90,'Good URL')

    plt.title('URL Behavior Graph(Prediction %')
    plt.show()

def url_behavior_value():
    left = [1, 2, 3]
    values = [1, 1, 1, -1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    height = [values.count(1), values.count(0), values.count(-1)]
    tick_label = ['1', '0', '-1']
    plt.bar(left, height, tick_label=tick_label,
            width=0.8, color=['green', 'orange', 'red'])
    plt.xlabel('Behavior Value')
    plt.ylabel('Count')
    plt.title('URL Behavior Graph (Values)')
    plt.show()

#correlation_matrix(df)
url_behavior_value()
url_behavior_per()


