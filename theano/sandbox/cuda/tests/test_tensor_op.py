"""
This file test tensor op that should also operate on CudaNdaray.
"""
import sys, time

from theano import shared
from theano.compile.pfunc import pfunc
from theano import tensor

import numpy
import theano
import theano.tensor as T

# Skip test if cuda_ndarray is not available.
from nose.plugins.skip import SkipTest
import theano.sandbox.cuda as cuda_ndarray
if cuda_ndarray.cuda_available == False:
    raise SkipTest('Optional package cuda disabled')

import theano.sandbox.cuda as tcn
import theano.sandbox.cuda as cuda
import theano.compile.mode
from theano.tests import unittest_tools as utt

if theano.config.mode=='FAST_COMPILE':
    mode_with_gpu = theano.compile.mode.get_mode('FAST_RUN').including('gpu')
    mode_without_gpu = theano.compile.mode.get_mode('FAST_RUN').excluding('gpu')
else:
    mode_with_gpu = theano.compile.mode.get_default_mode().including('gpu')
    mode_without_gpu = theano.compile.mode.get_default_mode().excluding('gpu')


def test_shape_i():
    x = cuda.ftensor3()
    v = cuda.CudaNdarray(numpy.zeros((3,4,5),dtype='float32'))
    f = theano.function([x],x.shape[1])
    topo = f.maker.env.toposort()
    assert len(topo)==1
    assert isinstance(topo[0].op,T.opt.Shape_i)
    assert f(v)==4