#   Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""parameters init function implementations"""


from __future__ import print_function

import os
import six

import numpy as np
import paddle.fluid as fluid


def init_checkpoint(exe, init_checkpoint_path, main_program):
    """
    init checkpoint params with lr and step info
    """
    assert os.path.exists(
        init_checkpoint_path), "[%s] cann't be found." % init_checkpoint_path
    def existed_persitables(var):
        """
        Check if persitables
        """
        if not fluid.io.is_persistable(var):
            return False
        return os.path.exists(os.path.join(init_checkpoint_path, var.name))

    fluid.io.load_vars(
        exe,
        init_checkpoint_path,
        main_program=main_program,
        predicate=existed_persitables)
    print("Load model from {}".format(init_checkpoint_path))


def init_pretraining_params(exe, pretraining_params_path, main_program):
    """
    init pretraining params without lr and step info
    """
    assert os.path.exists(pretraining_params_path
                          ), "[%s] cann't be found." % pretraining_params_path

    def existed_params(var):
        """
        Check existed params
        """
        if not isinstance(var, fluid.framework.Parameter):
            return False
        return os.path.exists(os.path.join(pretraining_params_path, var.name))

    fluid.io.load_vars(
        exe,
        pretraining_params_path,
        main_program=main_program,
        predicate=existed_params)
    print("Load pretraining parameters from {}.".format(
        pretraining_params_path))

