import numpy as np
import math
from .bspline import BSpline
from .convolution_filter import pad, ConvolutionFilter

def crop(arr, margin, width, height):
    row_start = margin
    row_stop = margin + height
    col_start = margin
    col_stop = margin + width
    return arr[row_start:row_stop,col_start:col_stop]

class CompoundWaveletFilter:
    def __init__(self, spline_order, spline_scale):
        self.order = float(spline_order)
        self.scale = float(spline_scale)
        self.nsamples = int(2.0 * math.ceil(self.order * self.scale / 2.0) - 1.0)
        self.w1 = WaveletFilter(1, self.order, self.scale, self.nsamples, 'zeros')
        self.w2 = WaveletFilter(2, self.order, self.scale, self.nsamples, 'zeros')
        self.margin = int(float(self.w2.get_kernelX()) / 2.0)

    def filter_image(self, image):
        padded = pad(image, self.margin, 'duplicate')
        v1 = self.w1.filter_image(padded)
        v2 = self.w2.filter_image(v1)

        self.result_f1 = np.subtract(image, crop(v1, self.margin, image.shape[1], image.shape[0]))
        self.result_f2 = np.subtract(image, crop(v2, self.margin, image.shape[1], image.shape[0]))
        self.result = crop(np.subtract(v1, v2), self.margin, image.shape[1], image.shape[0])
        
        return self.result

class WaveletFilter:
    def __init__(self, plane, spline_order, spline_scale, nsamples, padding):
        self.plane = plane
        self.order = spline_order
        self.scale = spline_scale
        self.nsamples = nsamples
        self.kernel = self.get_kernel()
        self.mfilter = ConvolutionFilter(self.kernel, padding=padding)
        self.mfilter.create_separable_kernel()

    def get_kernel(self):
        nsamples = self.nsamples
        samples = np.array(range(nsamples))
        for i in range(nsamples):
            samples[i] = i - nsamples / 2

        plane = self.plane
        spline_order = self.order
        spline_scale = self.scale
        bspline = BSpline(spline_order, spline_scale, samples)
        spline = bspline.bspline_blender()
        if plane == 1:
            return spline
        else:
            step = 2**(plane-1)
            n = (step * (nsamples - 1)) + 1
            kernel = np.zeros(n)
            for i in range(spline.shape[0]):
                kernel[i*step] = spline[i]
            return kernel

    def get_kernelX(self):
        return self.kernel.shape[0]

    def filter_image(self, image):
        return self.mfilter.filter_image(image) 
