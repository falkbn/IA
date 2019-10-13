============================================================================================
ORGANIZACIÓN DE FICHEROS DEL PROYECTO:
============================================================================================
CARPETA py:

Contiene el código desarrollado en el proyecto.

1) Dentro de "acciones.py" se encuentran las acciones posibles que pueden usar los estados.

2) Dentro de "acciones_main.py" se encuentra el código necesario para ejecutar las búsquedas.
   La búsqueda se encuentra en la linea 62 del fichero.

3) Dentro de "file_reader.py" se encuentra un metodo para leer del fichero indicado las
   matrices que representan el tablero Hitori y escribe en el fichero destino los tiempos
   que ha tardado en resolver cada una. Dado que, aunque resuelve la mayoría de 9x9, pero no
   todas no es buena idea ejecutarlo usando el fichero de retos.

4) El fichero "búsqueda_espacio_estados.py" ha sido proporcionado para el proyecto.

5) Aunque el fichero "problema_espacio_estados.py" ha sido proporcionado para el proyecto,
   este ha sido modificado para que no solicite el estado final como parámetro, ya que es

--------------------------------------------------------------------------------------------
CARPETA txt:

Contiene los ficheros de texto proporcionados con las matrices de prueba y reto, además de
los respectivos ficheros de escritura con los tiempos de resolución por A* de las mismas.

--------------------------------------------------------------------------------------------
CARPETA ipybn:

Contiene los ficheros de las prácticas de la asignatura relevantes al proyecto y su 
desarrollo.

--------------------------------------------------------------------------------------------
CARPETA py/ideas:

Contiene antiguas implementaciones e ideas descartadas del proyecto
============================================================================================


============================================================================================
FORMA DE USO 1:
============================================================================================

1) Copiar la matriz deseada del fichero correspondiente.

2) Pegar la matriz en la linea 8 del fichero "acciones_main.py"

3) Cambiar el algoritmo de búsqueda en la línea 61 de desearlo. Por defecto esta A*.

4) Ejecutar el fichero y observar el resultado por consola.
============================================================================================


============================================================================================
FORMA DE USO 2:
============================================================================================

1) Ejecutar el fichero "file_reader.py"

2) Observar los tiempos de cada matriz en el fichero: "ejemplos_reto_prueba_estrella.txt".
============================================================================================


============================================================================================
NOTAS
============================================================================================

Se ha usado "pycharm" como entorno de desarrollo. Para acceder al código abrir la carpeta
con un entorno de desarrollo compatible.
============================================================================================