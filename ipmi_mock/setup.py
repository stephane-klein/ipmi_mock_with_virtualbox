import setuptools

setuptools.setup(
    name="ipmi_mock",
    version="0.1.0",
    author="Stéphane Klein",
    author_email="contact@stephane-klein.info",
    packages=setuptools.find_packages(),
    install_requires=[
        "grpcio==1.10.0",
        "protobuf==3.5.1",
        "six==1.11.0"
    ],
    entry_points="""
    [console_scripts]
    ipmitool = ipmi_mock.client:main
    ipmimock-server = ipmi_mock.server:main
    """

)
