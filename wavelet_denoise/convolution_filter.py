import numpy as np
#from scipy.signal import convolve
from scipy.ndimage.filters import convolve

def pad(image, margin, method):
    if 'duplicate' in method:
        return np.pad(image,((margin,margin),(margin,margin)),
            mode='wrap')
    if 'zeros' in method:
        return np.pad(image,((margin,margin),(margin,margin)),
            mode='constant',constant_values=0.0)

class ConvolutionFilter:
    def __init__(self, kernel, padding='duplicate'):
        self.kernel = kernel
        self.padding = padding

    def create_separable_kernel(self):
        kernel = self.kernel
        self.kernelX = np.reshape(kernel,(1,kernel.shape[0]))
        self.kernelY = np.reshape(kernel,(kernel.shape[0],1))

    def convolve2D(self, arr, kernel, padding):
        i = convolve(arr, kernel, mode='wrap')
        return i
        # img = arr
        # margin = int(float(kernel.shape[0]) / 2.0)
        # istart = margin
        # istop = arr.shape[0] - margin
        # jstart = margin
        # jstop = arr.shape[1] - margin
        # for i in range(istart,istop):
        #     for j in range(jstart,jstop):
        #         total = 0.0
        #         for k in range(0,kernel.shape[0]):
        #             total = np.sum(arr[i,j] * kernel[k])
        #         img[i,j] = total

        # return img
    # def convolve2D(self, arr, k, padding):
    #     pad_size = ceil(java.lang.Math.max(kw, kh) / 2.0).toInt()
    #     padded = pad(arr, pad_size, padding)
    #     i1 = convolve(padded,kX)
    #     i2 = convolve(i1,kY)
    #     return i2

    def filter_image(self, image):
        kernelX = self.kernelX
        kernelY = self.kernelY
        return self.convolve2D(
            self.convolve2D(image, kernelX, self.padding),
                            kernelY, self.padding)