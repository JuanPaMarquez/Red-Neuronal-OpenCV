Documentacion de las funciones para mejor entendimiento

### Funciones en `capture_and_save.py`

1. **`capture_and_save(personName, cameraLabel, model, progressBar)`**:
   - Esta función se encarga de capturar imágenes de una persona desde la cámara, recibe como parámetros:
     - `personName`: El nombre de la persona a la que se están capturando las imágenes.
     - `cameraLabel`: El widget `QLabel` donde se muestra la vista previa de la cámara en la interfaz de usuario.
     - `model`: El modelo de red neuronal convolucional utilizado para la detección facial y la extracción de características.
     - `progressBar`: El widget `QProgressBar` que muestra el progreso de la captura de imágenes.
   - Inicia la captura de video desde la cámara y procesa los fotogramas uno por uno.
   - Detecta rostros en cada fotograma utilizando un clasificador de Haar y extrae las características faciales utilizando el modelo `openface`.
   - Guarda las características faciales extraídas en archivos `.npy` en la carpeta correspondiente a la persona.
   - Actualiza la vista previa de la cámara en la interfaz de usuario y la barra de progreso para mostrar el progreso de la captura.
   - Cuando se completa la captura de imágenes, restablece la barra de progreso a cero.

### Funciones en `gui.py`

1. **`capture()`**:
   - Esta función se activa cuando se hace clic en el botón "Capturar y Guardar" en la interfaz de usuario.
   - Muestra un cuadro de diálogo para que el usuario ingrese el nombre de la persona a la que se están capturando las imágenes.
   - Inicia la cámara y la captura de imágenes llamando a la función `capture_and_save`.
   - Configura la variable `is_capturing` para indicar que se está capturando imágenes.

2. **`train()`**:
   - Esta función se activa cuando se hace clic en el botón "Entrenar Modelo" en la interfaz de usuario.
   - Entrena el modelo SVM utilizando las características faciales previamente extraídas y guardadas.
   - Muestra un mensaje de información cuando el entrenamiento se completa con éxito.

3. **`start_recognition()`**:
   - Esta función se activa cuando se hace clic en el botón "Iniciar Reconocimiento" en la interfaz de usuario.
   - Inicia la cámara para el reconocimiento facial en tiempo real llamando a la función `start_camera`.
   - Carga el modelo SVM previamente entrenado y el modelo `openface`.
   - Configura la variable `is_recognizing` para indicar que se está realizando el reconocimiento facial.

4. **`identify_person()`**:
   - Esta función se activa cuando se hace clic en el botón "Identificar Persona" en la interfaz de usuario.
   - Captura una imagen de la cámara y la utiliza para identificar a la persona presente en la imagen.
   - Muestra un mensaje de información con el nombre de la persona identificada o "Desconocido".

5. **`start_camera()`** y **`stop_camera()`**:
   - Estas funciones se encargan de iniciar y detener la captura de la cámara respectivamente.
   - Se utilizan para activar y desactivar el temporizador que actualiza el fotograma de la cámara en la interfaz de usuario.

6. **`update_frame()`**:
   - Esta función se activa periódicamente para actualizar el fotograma de la cámara en la interfaz de usuario.
   - Cuando se está capturando imágenes, llama a la función `capture_and_save` para procesar los fotogramas y actualizar la barra de progreso.
   - Cuando se está realizando el reconocimiento facial, llama a la función `display_recognition` para mostrar el resultado del reconocimiento en tiempo real.

7. **`display_recognition()`**:
   - Esta función muestra el resultado del reconocimiento facial en tiempo real en la vista previa de la cámara.
   - Dibuja un rectángulo alrededor de los rostros detectados y muestra el nombre de la persona identificada o "Desconocido" sobre el rectángulo.

8. **`load_model()`**:
   - Esta función carga el modelo SVM previamente entrenado y el modelo `openface` utilizado para el reconocimiento facial.

Claro, aquí tienes una explicación detallada de las funciones en `train_model.py` y `recognize.py`:

### Funciones en `train_model.py`

1. **`train_model()`**:
   - Esta función se encarga de entrenar un modelo de SVM utilizando las características faciales extraídas previamente.
   - Lee los archivos `.npy` que contienen las características faciales de cada persona desde la carpeta de datos.
   - Asigna etiquetas a cada conjunto de características faciales según el nombre de la carpeta que contiene las imágenes.
   - Entrena un clasificador SVM utilizando el conjunto de características faciales y las etiquetas asociadas.
   - Guarda el modelo entrenado en un archivo `.pkl` para su uso posterior.

### Funciones en `recognize.py`

1. **`recognize()`**:
   - Esta función se encarga de reconocer caras en tiempo real utilizando el modelo SVM previamente entrenado.
   - Lee el modelo SVM desde el archivo `.pkl` y el modelo `openface` para la extracción de características faciales.
   - Inicia la captura de video desde la cámara y procesa los fotogramas uno por uno.
   - Detecta rostros en cada fotograma utilizando un clasificador de Haar.
   - Extrae las características faciales de cada rostro detectado utilizando el modelo `openface`.
   - Utiliza el modelo SVM para predecir la identidad de cada rostro.
   - Si la predicción tiene una probabilidad alta, muestra el nombre de la persona reconocida sobre el rectángulo del rostro en el fotograma de la cámara.
   - Si la probabilidad es baja, muestra "Desconocido" sobre el rectángulo del rostro.
   - La función se ejecuta continuamente hasta que se presiona la tecla "Esc" para salir.