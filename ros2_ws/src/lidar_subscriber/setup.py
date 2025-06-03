from setuptools import find_packages, setup

package_name = 'lidar_subscriber'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='k',
    maintainer_email='k@todo.todo',
    description='Este paquete recibe la información del LiDAR del argo J8',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'lidar_subscriber = lidar_subscriber.lidar_subscriber:main'
        ],
    },
)
