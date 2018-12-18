import os.path
import setuptools

# Get long description from README.
with open('README.rst', 'r') as fh:
    long_description = fh.read()

# Get package metadata from '__about__.py' file.
about = {}
base_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(base_dir, 'resolwe_bio', '__about__.py'), 'r') as fh:
    exec(fh.read(), about)

setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__summary__'],
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author=about['__author__'],
    author_email=about['__email__'],
    url=about['__url__'],
    license=about['__license__'],
    # Exclude tests from built/installed package.
    packages=setuptools.find_packages(
        exclude=['tests', 'tests.*', '*.tests', '*.tests.*']
    ),
    package_data={
        'resolwe_bio': [
            'descriptors/*.yml',
            'fixtures/*.yaml',
            'processes/**/*.yml',
            'processes/**/*.py',
            'tools/*.py',
            'tools/*.R',
            'tools/*.sh',
        ]
    },
    python_requires='>=3.6, <3.7',
    install_requires=(
        'Django~=1.11.0',
        # XXX: Remove django-autoslug after all migrations that import it are
        # deleted.
        'django-autoslug==1.9.3',
        'djangorestframework~=3.9.0',
        'elasticsearch-dsl~=5.4.0',
        # XXX: Required due to issue https://github.com/pypa/pip/issues/4905.
        'resolwe >=16.0a1, ==16.*',
        'wrapt>=1.10.8',
        'django-filter~=2.0.0',
    ),
    extras_require={
        'docs': [
            # XXX: Temporarily pin Sphinx to version 1.5.x since 1.6 doesn't
            # work with our custom page template.
            'Sphinx~=1.5.6',
            'sphinx_rtd_theme',
        ],
        'package': ['twine', 'wheel'],
        'test': [
            # pycodestyle 2.3.0 raises false-positive for variables
            # starting with 'def'
            # https://github.com/PyCQA/pycodestyle/issues/617
            'pycodestyle~=2.2.0',
            'pydocstyle>=1.0.0',
            'pylint~=1.8.0',
            'tblib>=1.3.0',
            'check-manifest',
            'twine',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='bioinformatics resolwe bio pipelines dataflow django',
)
