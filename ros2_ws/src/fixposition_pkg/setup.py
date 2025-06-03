from setuptools import find_packages, setup

package_name = 'fixposition_pkg'

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
    description='FixPOsition IMU and GPS subscriber package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'imu_subscriber = fixposition_pkg.imu_subscriber:main',
            'gps_subscriber = fixposition_pkg.gps_subscriber:main',
            'odometry_subscriber = fixposition_pkg.odometry_subscriber:main'
        ],
    },
)
