from setuptools import setup

setup(
    name='slideshow_plus',
    version='0.1',
    description='RPI, projector, mobile phone as controller.',
    url='',
    author='Kristjan Voje',
    author_email='kristjan.voje@gmail.com',
    license='MIT',
    packages=['slideshow_plus'],
    install_requires=['Flask', 'python-magic'],
    zip_safe=False
)
