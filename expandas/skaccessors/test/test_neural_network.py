#!/usr/bin/env python

import numpy as np
import pandas as pd
import pandas.compat as compat

import sklearn.datasets as datasets
import sklearn.neural_network as nn

import expandas as expd
import expandas.util.testing as tm


class TestNeuralNtwork(tm.TestCase):

    def test_objectmapper(self):
        df = expd.ModelFrame([])
        self.assertIs(df.neural_network.BernoulliRBM, nn.BernoulliRBM)

    def test_RBM(self):
        digits = datasets.load_digits()
        df = expd.ModelFrame(digits)

        models = ['BernoulliRBM']
        for model in models:
            mod1 = getattr(df.neural_network, model)(random_state=self.random_state)
            mod2 = getattr(nn, model)(random_state=self.random_state)

            df.fit(mod1)
            mod2.fit(digits.data, digits.target)

            result = df.transform(mod1)
            expected = mod2.transform(digits.data)
            self.assertTrue(isinstance(result, expd.ModelFrame))
            self.assert_numpy_array_almost_equal(result.data.values, expected)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
