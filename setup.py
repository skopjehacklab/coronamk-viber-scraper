from setuptools import setup, find_packages

setup(
    name = "coronamk-viber-scraper",
    version = "0.1",
    url = "https://github.com/skopjehacklab/coronamk-viber-scraper",
    install_requires = ["requests"],
    description = "",
    long_description = "",
    package_data = {},
    entry_points = {
        'console_scripts': ['coronamk-viber-scraper=coronamk_viber_scraper.__main__:main']
    },
    packages = find_packages(),
)
