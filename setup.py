from setuptools import setup
from setuptools.command.install import install
import os

class CustomInstallCommand(install):
    """Customized setuptools install command - runs PyInstaller after installation."""
    def run(self):
        install.run(self)
        os.system('pyinstaller --onefile --windowed run_server.py')

setup(
    name='LLM-App',
    version='1.0',
    py_modules=['run_server'],
    install_requires=[
        'Flask',
        'PyInstaller',
    ],
    cmdclass={
        'install': CustomInstallCommand,
    },
)
