from . import store
from .schemas import LecturaEntrada, ComandoLED

def guardar_lectura(datos: LecturaEntrada) -> dict:
    lectura = datos.model_dump()
    store.lecturas.append(lectura)
    # Conservamos como máximo las últimas 100 lecturas recibidas.
    del store.lecturas[:-100]
    return {"lectura": lectura, "led": store.estado_led["color"]}

def listar_lecturas() -> list[dict]:
    return store.lecturas

def consultar_led() -> dict:
    return store.estado_led

def cambiar_led(comando: ComandoLED) -> dict:
    store.estado_led["color"] = comando.color
    return store.estado_led

def promediar_lecturas(n: int) -> dict | None:
    ultimas = store.lecturas[-n:]
    cantidad = len(ultimas)

    if cantidad == 0:
        return None

    suma_temp = sum(lectura["temperatura"] for lectura in ultimas)
    promedio_temp = round(suma_temp / cantidad, 2)

    suma_humedad = sum(lectura["humedad"] for lectura in ultimas)
    promedio_humedad = round(suma_humedad / cantidad, 2)

    return {
        "cantidad": cantidad,
        "temperatura_promedio": promedio_temp,
        "humedad_promedio": promedio_humedad
    }