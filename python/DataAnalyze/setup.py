from setuptools import setup

setup(
    name="DataAnalyzer",
    version='1.4',
    description='python3でデータ解析用の自作パッケージ',
    author='x',
    install_requires=open('requirements.txt').read().splitlines(),
)
