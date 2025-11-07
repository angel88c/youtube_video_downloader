import streamlit as st
import yt_dlp
import os
import json
from pathlib import Path
from datetime import datetime
import re

# Configuración
VIDEOS_DIR = Path("videos_descargados")
PLAYLIST_FILE = Path("playlist.json")

# Crear directorio de videos si no existe
VIDEOS_DIR.mkdir(exist_ok=True)

# Detectar si estamos en Streamlit Cloud
import sys
IS_CLOUD = hasattr(sys, 'ps1') == False and 'streamlit' in sys.modules

# Funciones auxiliares
def cargar_playlist():
    """Carga la playlist desde el archivo JSON"""
    if PLAYLIST_FILE.exists():
        with open(PLAYLIST_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def guardar_playlist(playlist):
    """Guarda la playlist en el archivo JSON"""
    with open(PLAYLIST_FILE, 'w', encoding='utf-8') as f:
        json.dump(playlist, indent=2, ensure_ascii=False, fp=f)

def sanitizar_nombre(nombre):
    """Sanitiza el nombre del archivo removiendo caracteres inválidos"""
    return re.sub(r'[<>:"/\\|?*]', '', nombre)

def descargar_video(url, progreso_callback=None):
    """Descarga un video de YouTube en calidad HD"""
    try:
        def hook(d):
            if d['status'] == 'downloading' and progreso_callback:
                progreso_callback(d)
        
        ydl_opts = {
            'format': 'best[height<=1080]/best',
            'outtmpl': str(VIDEOS_DIR / '%(title)s.%(ext)s'),
            'progress_hooks': [hook],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            titulo = info.get('title', 'Sin título')
            duracion = info.get('duration', 0)
            thumbnail = info.get('thumbnail', '')
            nombre_archivo = sanitizar_nombre(titulo) + '.mp4'
            
            return {
                'titulo': titulo,
                'url': url,
                'archivo': nombre_archivo,
                'duracion': duracion,
                'thumbnail': thumbnail,
                'fecha_descarga': datetime.now().isoformat()
            }
    except Exception as e:
        raise Exception(f"Error al descargar: {str(e)}")

def eliminar_video(video_info):
    """Elimina un video del disco y de la playlist"""
    ruta_video = VIDEOS_DIR / video_info['archivo']
    if ruta_video.exists():
        ruta_video.unlink()
    
    playlist = cargar_playlist()
    playlist = [v for v in playlist if v['archivo'] != video_info['archivo']]
    guardar_playlist(playlist)

def formatear_duracion(segundos):
    """Convierte segundos a formato HH:MM:SS"""
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segs = int(segundos % 60)
    
    if horas > 0:
        return f"{horas:02d}:{minutos:02d}:{segs:02d}"
    return f"{minutos:02d}:{segs:02d}"

# Interfaz de Streamlit
st.set_page_config(
    page_title="Descargador de Videos de YouTube",
    page_icon="🎥",
    layout="wide"
)

# Inicializar session state
if 'video_descargado' not in st.session_state:
    st.session_state.video_descargado = None

st.title("🎥 Descargador de Videos de YouTube HD")

# Advertencia para Streamlit Cloud
if IS_CLOUD:
    st.info("""
    ☁️ **Modo Cloud Activado:**
    Los videos se descargarán directamente a tu computadora usando el botón "Descargar a mi PC".
    La playlist es temporal y se limpiará al reiniciar la aplicación.
    """)

st.markdown("---")

# Sección de descarga
st.header("📥 Descargar Video")

col1, col2 = st.columns([3, 1])

with col1:
    url = st.text_input(
        "URL del video de YouTube:",
        placeholder="https://www.youtube.com/watch?v=..."
    )

with col2:
    st.write("")  # Espaciado
    st.write("")  # Espaciado
    boton_descargar = st.button("⬇️ Descargar", type="primary", use_container_width=True)

if boton_descargar and url:
    if 'youtube.com' in url or 'youtu.be' in url:
        with st.spinner('Descargando video...'):
            progreso_placeholder = st.empty()
            
            def actualizar_progreso(d):
                if 'downloaded_bytes' in d and 'total_bytes' in d:
                    porcentaje = (d['downloaded_bytes'] / d['total_bytes']) * 100
                    progreso_placeholder.progress(porcentaje / 100, f"Descargando: {porcentaje:.1f}%")
            
            try:
                video_info = descargar_video(url, actualizar_progreso)
                
                # Agregar a la playlist
                playlist = cargar_playlist()
                
                # Verificar si ya existe
                if not any(v['url'] == url for v in playlist):
                    playlist.append(video_info)
                    guardar_playlist(playlist)
                
                progreso_placeholder.empty()
                
                # Guardar en session state para descarga automática
                st.session_state.video_descargado = video_info
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.error("❌ Por favor ingresa una URL válida de YouTube")
elif boton_descargar:
    st.warning("⚠️ Por favor ingresa una URL")

# Mostrar botón de descarga si hay un video recién descargado
if st.session_state.video_descargado:
    video = st.session_state.video_descargado
    ruta_video = VIDEOS_DIR / video['archivo']
    
    if ruta_video.exists():
        st.success(f"✅ Video descargado: {video['titulo']}")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.info(f"📊 Duración: {formatear_duracion(video['duracion'])} | Tamaño: {ruta_video.stat().st_size / (1024 * 1024):.2f} MB")
        
        with col2:
            with open(ruta_video, 'rb') as f:
                if st.download_button(
                    label="💾 Descargar a mi PC",
                    data=f,
                    file_name=video['archivo'],
                    mime='video/mp4',
                    type="primary",
                    use_container_width=True
                ):
                    st.balloons()
        
        with col3:
            if st.button("✅ Listo", use_container_width=True):
                st.session_state.video_descargado = None
                st.rerun()

st.markdown("---")

# Sección de playlist
st.header("📋 Mi Playlist Local")

playlist = cargar_playlist()

if playlist:
    st.info(f"📊 Total de videos: {len(playlist)}")
    
    for idx, video in enumerate(playlist):
        with st.expander(f"🎬 {video['titulo']}", expanded=False):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.write(f"**Duración:** {formatear_duracion(video['duracion'])}")
                st.write(f"**Descargado:** {video['fecha_descarga'][:10]}")
                
            with col2:
                ruta_video = VIDEOS_DIR / video['archivo']
                if ruta_video.exists():
                    tamaño_mb = ruta_video.stat().st_size / (1024 * 1024)
                    st.write(f"**Tamaño:** {tamaño_mb:.2f} MB")
                    st.write(f"**Archivo:** {video['archivo']}")
                else:
                    st.warning("⚠️ Archivo no encontrado")
            
            with col3:
                if st.button("🗑️ Eliminar", key=f"del_{idx}", use_container_width=True):
                    eliminar_video(video)
                    st.rerun()
                
                if ruta_video.exists():
                    with open(ruta_video, 'rb') as f:
                        st.download_button(
                            label="💾 Exportar",
                            data=f,
                            file_name=video['archivo'],
                            mime='video/mp4',
                            key=f"down_{idx}",
                            use_container_width=True
                        )
            
            # Mostrar miniatura si está disponible
            if video.get('thumbnail'):
                st.image(video['thumbnail'], width=300)
else:
    st.info("📭 No hay videos en tu playlist. ¡Descarga algunos videos para comenzar!")

# Información adicional
st.markdown("---")
with st.expander("ℹ️ Información y Ayuda"):
    st.markdown("""
    ### Cómo usar esta aplicación:
    
    1. **Descargar videos:**
       - Copia la URL de un video de YouTube
       - Pégala en el campo de texto
       - Haz clic en "Descargar"
    
    2. **Gestionar tu playlist:**
       - Todos los videos descargados aparecerán en la sección "Mi Playlist Local"
       - Puedes eliminar videos individuales
       - También puedes exportar videos a otras ubicaciones
    
    3. **Calidad de descarga:**
       - Los videos se descargan en la mejor calidad HD disponible (hasta 1080p)
       - El formato de salida es MP4
    
    ### Ubicación de archivos:
    - **Videos:** `{}`
    - **Playlist:** `{}`
    """.format(VIDEOS_DIR.absolute(), PLAYLIST_FILE.absolute()))
