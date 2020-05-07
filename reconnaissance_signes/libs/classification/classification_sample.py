#!/usr/bin/env python
"""
 Copyright (C) 2018-2019 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
from __future__ import print_function
import sys
import os
from argparse import ArgumentParser, SUPPRESS
import cv2
import numpy as np
import logging as log
from time import time
from openvino.inference_engine import IENetwork, IECore


def processImg(model_path,image):
    model_xml = model_path
    model_bin = os.path.splitext(model_xml)[0] + ".bin"

    # Plugin initialization for specified device and load extensions library if specified
    ie = IECore()
    # Read IR
    net = IENetwork(model=model_xml, weights=model_bin)

    input_blob = next(iter(net.inputs))
    out_blob = next(iter(net.outputs))
    #net.batch_size = len(args.input)

    # Read and pre-process input images
    #n, c, h, w = net.inputs[input_blob].shape
    image = image.transpose((2, 0, 1))  # Change data layout from HWC to CHW

    # Loading model to the plugin
    exec_net = ie.load_network(network=net, device_name='MYRIAD')

    # Start sync inference
    res = exec_net.infer(inputs={input_blob: image})

    # Processing output blob
    res = res[out_blob]
    
    for i, probs in enumerate(res):
        probs = np.squeeze(probs)
        top_ind = np.argsort(probs)[-3:][::-1]
        resultat = []
        for id in top_ind:
            print("{}{}{:.7f}".format(id, ' -> ', probs[id]))
        return(top_ind,probs)
