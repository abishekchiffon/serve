# pylint: disable=W0223
# Details : https://github.com/PyCQA/pylint/issues/3098
"""
Base module for all vision handlers
"""
from abc import ABC
import io
import torch
from PIL import Image
from .base_handler import BaseHandler
from captum.attr import IntegratedGradients


class VisionHandler(BaseHandler, ABC):
    """
    Base class for all vision handlers
    """

    def initialize(self, context):
        super(VisionHandler, self).initialize(context)
        self.ig = IntegratedGradients(self.model)
        self.initialized = True

    def preprocess(self, data):
        images = []
        
        for row in data:
            # Compat layer: normally the envelope should just return the data
            # directly, but older versions of Torchserve didn't have envelope.
            if isinstance(row, dict):
                image = row.get("data") or row.get("body") or row
            else:
                image = row
            image = Image.open(io.BytesIO(image))
            image = self.image_processing(image)
            images.append(image)

        return torch.stack(images)

    def get_insights(self, tensor_data, raw_data, target=0):
        print("input shape", tensor_data.shape)
        return self.ig.attribute(tensor_data, target=target, n_steps=15).tolist()
        