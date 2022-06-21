# Repositorio para Práctica de Ray Tracing

Este repositorio contiene el desarrollo de los ejercicios de la práctica de Ray Tracing de la asignatura IGM, MUEI 2021-2022. Estudiante Laura Ben Artiles.

Está organizado de la siguiente forma:

Rama <b>feature/moreLight</b>:

Contiene los archivos para dar respuesta a la primera parte de esta tarea: añadir a este motor la posibilidad de trabajar con un número arbitrario de fuentes de luz, cada una de ellas con sus propias características (posición y color).

Para resolver esta tarea se tomó como base la explicación y el código consultado en el siguiente repositorio público https://github.com/arocks/puray/tree/episode04.

Rama <b>feature/triangles</b>:

Contiene los archivos para dar respuesta a la segunda parte de esta tarea: añadir al motor una nueva primitiva gráfica con la que trabajar -> triángulo. Modificar la escena predeterminada para que incluya algún triángulo, además de esferas y planos como en la escena original.

Para resolver esta tarea se tomó como base la explicación y el código consultado en el siguiente blog de Ray Tracing: https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/ray-triangle-intersection-geometric-solution


* Rama <b>main</b>. Contiene un merge desde la rama feature/moreLight.

En cada rama hay una carpeta que contiene capturas con los ejemplos de renders obtenidos para cada caso.

## Ejecución
Se precisa python 2 y las bibliotecas numpy y matplotlib.

```console
    $ python2 raytracing.py
```
