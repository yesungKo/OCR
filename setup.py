from setuptools import setup, find_packages

setup(
    name='ocr_project',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python',
        'paddleocr',
        'paddlepaddle-gpu',
        'pandas',
        'Pillow',
        'argparse'
    ],
    entry_points={
        'console_scripts': [
            'ocr_project=ocr_project.run:main',
        ],
    },
)
