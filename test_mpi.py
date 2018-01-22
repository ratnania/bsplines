# -*- coding: UTF-8 -*-
#! /usr/bin/python

from bsplines import Bspline
from bsplines import CardinalBspline
from bsplines import UniformBspline
import numpy as np
import matplotlib.pyplot as plt


def test_sequential(p, n):

    T = np.linspace(0.,1.,n+1)
    T = [0.] *p  + list(T) + [1.] * p
    T = np.array(T)

    bsp = Bspline(T,p)

    nx = 400
    N = len(T) - p - 1
    x = np.linspace(0.0,1.0,nx)

    y = np.zeros((N,nx), dtype=np.double)
    for i in range(0,N):
        y[i]=bsp(x, i=i)

        label = '$N_{' + '{i}'.format(i=i) + '}$'

        alpha = 1.
        linestyle = '-'

        plt.plot(x, y[i],
                 label=label,
                 alpha=alpha,
                 linestyle=linestyle)

    grid = np.unique(T)
    plt.plot(grid, np.zeros_like(grid), 'ok')
    plt.legend(loc=9, ncol=4)
    plt.ylim([0., 1.1])

    plt.savefig('splines_sequential.png')
    plt.clf()

def test_parallel(p, n, n_procs=2):

    T = np.linspace(0.,1.,n+1)
    T = [0.] *p  + list(T) + [1.] * p
    T = np.array(T)

    bsp = Bspline(T,p)

    nx = 400
    N = len(T) - p - 1
    x = np.linspace(0.0,1.0,nx)
    y = np.zeros((N,nx), dtype=np.double)
    for i in range(0, N):
        y[i]=bsp(x, i=i)

    for i_proc in range(0, n_procs):
        ns = N // n_procs
        i_begin = i_proc * ns
        i_end   = (i_proc+1) * ns - 1
        i_splines = range(i_begin, i_end+1)

        for i in range(0, N):
            label = '$N_{' + '{i}'.format(i=i) + '}$'

            alpha = 1.
            linestyle = '-'

            if i not in i_splines:
                if (i_begin - p <= i) and (i <= i_begin - 1):
                    linestyle = '--'
                elif (i_end + 1 <= i ) and (i <= i_end + p):
                    linestyle = '--'
                else:
                    alpha = 0.6
                    linestyle = ':'

            plt.plot(x, y[i],
                     label=label,
                     alpha=alpha,
                     linestyle=linestyle)

        grid = np.unique(T)
        plt.plot(grid, np.zeros_like(grid), 'ok')
        plt.legend(loc=9, ncol=4)
        plt.ylim([0., 1.1])
        plt.title('Proc $P_{i_proc}$'.format(i_proc=i_proc))

        plt.savefig('splines_parallel_proc_{proc}.png'.format(proc=i_proc))
        plt.clf()

##########################################
if __name__ == "__main__":
    p = 2
    n = 16 - p

#    test_sequential(p, n)
    test_parallel(p, n, n_procs=2)
#    test_parallel(p, n, n_procs=4)
