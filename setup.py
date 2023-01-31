from setuptools import setup, find_namespace_packages

with open('README.md','r', encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name = 'Top Helper Bot',
    version = '1.0.0',
    description = 'Project "Personal Assistant" with a command line interface',
    url = 'https://github.com/Demonytro/Top-Helper-Bot.git',
    author = 'QUATTRO Team',
    long_description = 'Project "Personal Assistant" with a command line interface',
    classifiers = [
        'Programming Language :: Python :: 3',
        'Operating System :: Windows',
        'License :: MIT License'
    ],
    packages = find_namespace_packages(),
    install_requires = ["requests"],
    entry_points = {'console_scripts': ['topbot = top_helper_bot.menu:main_menu']}
)