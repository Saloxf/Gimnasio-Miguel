from datetime import datetime, timezone

import gpxpy


def analizar_gpx(archivo):
    archivo.seek(0)
    gpx = gpxpy.parse(archivo)
    puntos = [
        punto
        for track in gpx.tracks
        for segmento in track.segments
        for punto in segmento.points
    ]
    if len(puntos) < 2:
        raise ValueError("El GPX debe contener al menos dos puntos de recorrido.")
    puntos.sort(key=lambda punto: punto.time or gpx.time or datetime.min.replace(tzinfo=timezone.utc))
    distancia_total = float(gpx.length_2d() or 0)
    tiempo_total = int(gpx.get_duration() or 0)
    ruta = []
    elevacion = []
    segmentos = {}
    ganada = perdida = 0.0
    anterior = None
    distancia_acumulada = 0.0
    for punto in puntos:
        if anterior is not None:
            distancia_acumulada += float(anterior.distance_2d(punto) or 0)
        distancia_punto = distancia_acumulada
        ruta.append({
            "lat": round(punto.latitude, 6),
            "lon": round(punto.longitude, 6),
            "elevacion": round(punto.elevation or 0, 2),
            "tiempo": punto.time.isoformat() if punto.time else None,
        })
        elevacion.append({
            "distancia": round(distancia_punto, 2),
            "valor": round(punto.elevation or 0, 2),
        })
        numero = int(distancia_punto // 1000) + 1
        segmentos.setdefault(numero, []).append(punto)
        if anterior and punto.elevation is not None and anterior.elevation is not None:
            cambio = punto.elevation - anterior.elevation
            if cambio > 0:
                ganada += cambio
            else:
                perdida += abs(cambio)
        anterior = punto
    datos_segmentos = []
    for numero, puntos_segmento in sorted(segmentos.items()):
        distancia_inicio = (numero - 1) * 1000
        distancia_fin = min(numero * 1000, distancia_total)
        tiempos = [p.time for p in puntos_segmento if p.time]
        duracion = int((tiempos[-1] - tiempos[0]).total_seconds()) if len(tiempos) > 1 else 0
        distancia_segmento = max(0, distancia_fin - distancia_inicio)
        datos_segmentos.append({
            "numero": numero,
            "distancia_metros": round(distancia_segmento, 2),
            "duracion_segundos": max(0, duracion),
            "ritmo_segundos_km": round(duracion * 1000 / distancia_segmento) if distancia_segmento and duracion else None,
        })
    return {
        "ruta": ruta,
        "elevacion": elevacion,
        "distancia_metros": round(distancia_total, 2),
        "duracion_segundos": tiempo_total,
        "elevacion_ganada": round(ganada, 2),
        "elevacion_perdida": round(perdida, 2),
        "segmentos": datos_segmentos,
    }
