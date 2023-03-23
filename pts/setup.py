from setuptools import setup, find_packages

setup(
    name='pts',
    version='0.1',
    description="PyTorch Probabilistic Time Series Modeling framework",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",

    url='https://github.com/kurvaraviteja355/Intermittent-time-series-forecasting-using-RolledDeepAR',
    license='MIT',
    packages=find_packages(include=["pts"]),
    include_package_data=True,
    zip_safe=True,
    python_requires=">=3.6",
    install_requires=[
        "torch>=1.8.0",
        'pydantic==1.4.0',
        'python-rapidjson',
        'pytorch-warmup',
        'tqdm',
        "gluonts",],

    test_suite='tests',
    tests_require = [
        'flake8',
        'pytest'
    ],
)