from setuptools import setup, find_packages

setup(
    name = "piriti",
    description = "Bridge between HTTP POST messages and WebSockets",
    version = "0.1.0",
    author = 'Lajos Santa',
    author_email = 'santa.lajos@coldline.hu',
    url = 'https://github.com/voidpp/piriti',
    install_requires = [
        "Flask-uWSGI-WebSocket~=0.5",
        "voidpp-tools~=1.8",
        "gevent~=1.1",
        "PyYAML~=3.12"
    ],
    scripts = [        
    ],
    packages = find_packages(),
)
