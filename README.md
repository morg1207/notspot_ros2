## Configurar espacio de trabajo

```bash
    mkdir -p ~/notspot_ws/src
    cd  ~/notspot_ws/src
    git clone https://github.com/morg1207/notspot_ros2.git
```

## Descargar dependencias y compilar

```bash
    cd  ~/notspot_ws
    rosdep init
    sudo apt update
    rosdep update --rosdistro $ROS_DISTRO
    rosdep install -i --from-path src --rosdistro $ROS_DISTRO -y
    colcon build --symlink-install

    sudo apt install pip -y
    pip install pynput 
```

## Ejecutar simulación

Terminal 1
```bash
    cd  ~/notspot_ws/
    source install/setup.bash
    ros2 launch notspot_gazebo notspot_gazebo.launch.py
```
Terminal 2
```bash
    cd  ~/notspot_ws/
    source install/setup.bash
    ros2 run notspot_joystick keyboard_sim_joy
```