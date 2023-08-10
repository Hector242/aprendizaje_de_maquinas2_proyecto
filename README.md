# aprendizaje_de_maquinas2_proyecto

Para inicializar el proyecto:

```python
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

Si tienes que quieres correr las versiones especificas que corrí en mi ambiente local puedes hacer lo siguiente:

```python
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements_specific_versions.txt
```
## Ejecucion
Para ejecutar el pipeline completo:

```python
$ source venv/bin/activate
$ cd src/
$ python3 processing_pipeline.py
```
Al iniciar el processing_pipeline.py el script preguntará si se desea o no evaluar el modelo con el test dataset por defecto o usar el example.json. Esa pregunta se responde con 'yes' o 'no'.

Por otro lado, si es la primera corrida es necesario que se tome la opcion 'yes' para que el modelo se entrene. Luego, se puede volver a correr el script python3 processing_pipeline.py y escoger la opcion 'no' para probar con el example.json.

## Logs
El logging de cada script se estara guardando en el directorio /logs.

## Datos transformados
Los datos transformados se guardan en el directorio /features. Aquí se tendrán los datasets de train y test para entrenar y evaluar el modelo. Por otro lado, si se toma la opcion de usar el example.json para evaluar el modelo se creará un nuevo archivo que comenzara con el nombre "custom_data"

## Data original
La data raw se encuentra /data.

## Notebook
En el directorio Notebook se encuentran todas las notebooks. tanto las proporcionadas por el cientifico de datos como la que optimiza los hiperparamentros. Por otro lado, hay una tercera notebook que se llama Prueba y esa notebook se testeo que el pipeline de procesamiento no afectara los resultados que el cientifico de datos haya optinido en la notebook.

## Model
El modelo luego de que se entrena es guardado en un plk y se va a encontrar en el directorio /model_trained.

## Predictions
Las predicciones siempre se guardan en un .csv en el directorio /predictions.
