import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    df = pd.read_csv('..\\compare_ES_to_special_teams\\percentile_results.csv')

    fig = plt.figure()
    # ax = fig.add_axes([0, 0, 1, 1])
    ax = fig.add_subplot(111)
    plt.ylim(100, 0)
    plt.xlim(100, 0)
    ax.scatter(df['EV_xGF'], df['PP_xGF'], color='b')
    ax.set_xlabel('Even-Strength xGF/60 RAPM')
    ax.set_ylabel('Power Play xGF/60 RAPM')
    ax.set_title('Scatter Plot')
    # for i, row in df.iterrows():
    #     ax.annotate(row['player'], (row['EV_xGF'], row['PP_xGF']))
    plt.show()


