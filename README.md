# Vehículo con Dirección Ackermann para Implementación de SLAM
## Descripción

Este proyecto presenta el desarrollo e implementación de un vehículo con dirección **Ackermann** utilizando **ROS 2 Jazzy**. El objetivo principal es desarrollar una plataforma de robótica móvil capaz de implementar algoritmos de **Simultaneous Localization and Mapping (SLAM)** y realizar navegación autónoma en un entorno controlado.

La arquitectura del sistema se divide en tres componentes principales: **control**, **percepción** y **navegación**.

### Control del vehículo

El control del movimiento está a cargo de un **LEGO EV3**, el cual se comunica con una **Raspberry Pi 5** mediante una conexión **socket TCP/IP**. La Raspberry Pi ejecuta ROS 2 y actúa como puente entre el hardware y el ecosistema ROS.

Para integrar el vehículo con ROS 2 se implementó un sistema basado en **ros2_control**, utilizando el controlador **bicycle_steering_controller**, adecuado para plataformas con dirección Ackermann. Esta integración requirió el desarrollo de:

- Un servidor que se ejecuta en el LEGO EV3.
- Un driver encargado de la comunicación entre el EV3 y la Raspberry Pi.
- Una **Hardware Interface** personalizada para conectar el hardware físico con `ros2_control`.

Gracias a esta arquitectura es posible controlar el robot desde ROS 2 de forma transparente y publicar la información de odometría necesaria para el resto del sistema.

### Percepción y estimación del estado

La percepción del entorno se realiza mediante un **LiDAR**, utilizado para la adquisición de información del entorno y la generación de mapas.

Uno de los principales desafíos en plataformas móviles es la presencia de ruido en los sensores y errores mecánicos, como el deslizamiento de las ruedas, los cuales afectan significativamente la estimación de la posición del robot. Para reducir estos errores se implementó un filtro de Kalman utilizando el paquete **robot_localization**.

El filtro fusiona información proveniente de tres fuentes:

- Odometría de las ruedas.
- Unidad de Medición Inercial (IMU).
- Odometría obtenida mediante LiDAR.

La fusión de estos sensores permite obtener una estimación de la pose considerablemente más precisa y robusta que utilizando cada sensor de forma independiente.

### Mapeo, localización y navegación

Una vez obtenida una estimación confiable de la odometría, se implementó el proceso de mapeo utilizando **slam_toolbox**, permitiendo construir un mapa del entorno de manera simultánea mientras el robot estima su posición.

Posteriormente, se empleó el algoritmo **Adaptive Monte Carlo Localization (AMCL)** para realizar la localización del robot sobre el mapa previamente generado.

Finalmente, se integró el sistema con la pila de navegación de ROS 2 (**Nav2**), realizando el ajuste y optimización de los diferentes parámetros de planificación, control y recuperación hasta obtener un comportamiento estable durante la navegación autónoma dentro del entorno de pruebas.

---

## Objetivos

- Implementar un modelo cinemático Ackermann en ROS 2.
- Integrar el robot con `ros2_control`.
- Adquirir datos de sensores para tareas de percepción.
- Implementar algoritmos de SLAM.
- Visualizar el robot y el mapa generado mediante RViz.
- Servir como plataforma para futuros desarrollos en navegación autónoma.

---

## Características

- 🚗 Modelo cinemático Ackermann.
- 🤖 Descripción del robot mediante URDF/Xacro.
- ⚙️ Integración con `ros2_control`.
- 📡 Compatibilidad con sensores LiDAR.
- 🗺️ Implementación de SLAM.
- 📍 Publicación de odometría y transformaciones (`tf`).
- 🖥️ Visualización en RViz.
- 📦 Organización modular mediante paquetes ROS 2.

---

## Estructura del Proyecto

```
workspace/
├── src/
│   ├── mi_ackermann_description/
│   │   ├── urdf/
│   │   ├── meshes/
│   │   ├── config/
│   │   └── launch/
│   │
│   ├── mi_ackermann_hardware/
│   │   ├── src/
│   │   ├── include/
│   │   └── config/
│   │
│   ├── mi_ackermann_bringup/
│   │   ├── launch/
│   │   ├── config/
│   │   └── rviz/
│   │
│   └── ...
│
└── README.md
```

---

## Requisitos

- Ubuntu 24.04 LTS
- ROS 2 Jazzy
- colcon
- rosdep

Paquetes principales:

- robot_state_publisher
- joint_state_publisher
- xacro
- ros2_control
- ros2_controllers
- controller_manager
- rviz2
- tf2_ros
- slam_toolbox (o cualquier implementación de SLAM compatible)

## Ejecución

Lanzar el sistema:

```bash
ros2 launch mi_ackermann_bringup carlike.launch.xml
```

Visualizar en RViz:

```bash
rviz2
```

---

## Diagrama General

```
                    +-------------------+
                    |      LiDAR        |
                    +---------+---------+
                              |
                              v
+-------------+       +--------------------+
| ros2_control| ----> | Robot Ackermann    |
+-------------+       +--------------------+
                              |
                              v
                      Publicación de TF
                              |
                              v
                        Odometría (/odom)
                              |
                              v
                      Algoritmo de SLAM
                              |
                              v
                        Mapa (/map)
                              |
                              v
                            RViz
```

---

## Tecnologías Utilizadas


- LegoEV3
- ROS 2 Jazzy
- C++
- Python        
- URDF/Xacro
- ros2_control
- RViz2
- TF2
- LiDAR
- SLAM Toolbox

---

## Estado del Proyecto

Actualmente el proyecto incluye:

- [x] Descripción del robot.
- [x] Modelo Ackermann.
- [x] Integración con ros2_control.
- [x] Publicación de estados articulares.
- [x] Publicación de odometría.
- [ ] Integración completa de sensores.
- [ ] Implementación de navegación autónoma.
- [ ] Optimización del sistema de localización.

## Autor

**Jeison Nicolás Díaz Arciniegas**

Universidad Nacional de Colombia

Ingeniería Mecatrónica
