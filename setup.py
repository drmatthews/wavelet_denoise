from setuptools import setup

setup(name='wavelet_denoise',
      version='0.1',
      description='Python translation of Thunderstorm wavelet denoising',
      url='http://github.com/drmatthews/wavelet_denoise',
      author='Dan Matthews',
      author_email='daniel.r.matthews@kcl.ac.uk',
      license='MIT',
      packages=['wavelet_denoise'],
      install_requires=[
          'numpy',
          'scipy',
      ],      
      zip_safe=False)