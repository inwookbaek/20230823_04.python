def app():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    # 한글처리
    from matplotlib import rc, font_manager

    font_name = font_manager\
                    .FontProperties(\
                        fname='D:/lec/04.python/D2Coding-Ver1.3.2-20180524.ttf')\
                    .get_name()
    rc('font', family=font_name)
    rc('axes', unicode_minus=False) # minus처리
    
    df = pd.DataFrame(np.random.rand(10,4), columns=['A','B','C','D'])
    df.plot.area(stacked=True)
    plt.show()    

if __name__ == '__main__':
    app()
