from setuptools import setup, find_packages

setup(
    name = "coronamk_viber_scrapper",
    version = "0.1",
    url = "https://github.com/skopjehacklab/coronamk_viber_scrapper",
    install_requires = ["requests"],
    description = "",
    long_description = "",
    package_data = {},
    entry_points = {
        'console_scripts': ['coronamk-viber-scrapper=coronamk_viber_scrapper.__main__:main']
    },
    packages = find_packages(),
)
