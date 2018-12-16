from setuptools import setup

setup(
    name='slideshowplus',
    version='0.1',
    description='RPI, projector, mobile phone as controller.',
    url='',
    author='Kristjan Voje',
    author_email='kristjan.voje@gmail.com',
    license='MIT',
    packages=['slideshowplus'],
    install_requires=['Flask', 'python-magic', 'flask-cors'],
    zip_safe=False
)
