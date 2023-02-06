import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.pyplot import show
import seaborn as sns

show(block=False)


def plot_train(df):
    plt.figure(figsize=(14, 8))
    ax1 = df.plot(kind='scatter', x='x', y='y1', color='r', s=1)
    ax2 = df.plot(kind='scatter', x='x', y='y2', color='g', ax=ax1, s=1)
    ax3 = df.plot(kind='scatter', x='x', y='y3', color='b', ax=ax1, s=1)
    ax4 = df.plot(kind='scatter', x='x', y='y4', color='b', ax=ax1, s=1)


def plot_ideal(df):
    df.plot(x='x', y=df.columns.drop('x').values)
    plt.ylim(top=120)
    plt.ylim(bottom=-25)

def plot_test(df):
    df.plot(kind='scatter', x='x', y=df.columns.drop('x').values)

def plot_cleaned_test(df):
    sns.scatterplot(x='x', y='y', data = df, hue='idealfunk')
    #df.plot(kind='scatter', x='x', y='y', c='nummerFunk')

