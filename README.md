# 🎥 Descargador de Videos de YouTube HD

Una aplicación simple y elegante desarrollada con Streamlit que te permite descargar videos de YouTube en calidad HD y gestionar una playlist local.

## ✨ Características

- **Descarga en HD**: Descarga videos en la mejor calidad disponible (hasta 1080p)
- **Descarga Directa al Navegador**: Descarga automática a tu carpeta de Descargas
- **Playlist Local**: Gestiona todos tus videos descargados en una lista de reproducción
- **Interfaz Intuitiva**: UI moderna y fácil de usar construida con Streamlit
- **Gestión de Videos**: Elimina o exporta videos fácilmente
- **Información Detallada**: Visualiza duración, tamaño, fecha de descarga y miniaturas
- **Barra de Progreso**: Seguimiento en tiempo real de las descargas
- **Compatible con Cloud**: Funciona perfectamente en Streamlit Cloud

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🚀 Instalación

1. **Clona o descarga este repositorio**

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta la aplicación:**
   ```bash
   streamlit run app.py
   ```

4. **Abre tu navegador** en la URL que aparece en la terminal (generalmente `http://localhost:8501`)

## 📖 Cómo Usar

### Descargar un Video

1. Copia la URL de cualquier video de YouTube
2. Pégala en el campo de texto
3. Haz clic en el botón "⬇️ Descargar"
4. Espera a que se complete la descarga
5. Haz clic en "💾 Descargar a mi PC" para guardar el video en tu computadora
6. El video se guardará automáticamente en tu carpeta de Descargas

### Gestionar tu Playlist

- **Ver detalles**: Expande cualquier video en la lista para ver información completa
- **Eliminar videos**: Usa el botón "🗑️ Eliminar" para quitar videos
- **Exportar videos**: Usa el botón "💾 Exportar" para descargar videos a otras ubicaciones

## 📁 Estructura de Archivos

```
download_youtube_videos/
├── app.py                  # Aplicación principal
├── requirements.txt        # Dependencias
├── README.md              # Este archivo
├── videos_descargados/    # Carpeta con videos (se crea automáticamente)
└── playlist.json          # Archivo de playlist (se crea automáticamente)
```

## 🛠️ Tecnologías Utilizadas

- **Streamlit**: Framework para la interfaz web
- **yt-dlp**: Biblioteca para descargar videos de YouTube
- **Python**: Lenguaje de programación

## ⚙️ Configuración

Por defecto, los videos se descargan en la carpeta `videos_descargados` y la información de la playlist se guarda en `playlist.json`. Puedes modificar estas rutas editando las constantes en `app.py`:

```python
VIDEOS_DIR = Path("videos_descargados")
PLAYLIST_FILE = Path("playlist.json")
```

## 📝 Notas

- Los videos se descargan en formato MP4
- La calidad máxima es 1080p (Full HD)
- Se requiere conexión a internet para descargar videos
- El tamaño de los archivos varía según la duración y calidad del video
- En despliegue cloud, los videos se descargan directamente al navegador

## ☁️ Uso en Streamlit Cloud

La aplicación está optimizada para funcionar en Streamlit Community Cloud:
- Los videos se procesan temporalmente en el servidor
- Después de descargar, usa el botón "Descargar a mi PC" para guardar el video
- La playlist se limpia automáticamente al reiniciar la app
- No requiere almacenamiento persistente en el servidor

## ⚠️ Advertencias

- Asegúrate de tener suficiente espacio en disco
- Respeta los derechos de autor de los videos que descargues
- Esta herramienta es solo para uso personal y educativo

## 🐛 Solución de Problemas

### Error al descargar videos

- Verifica que la URL sea válida
- Asegúrate de tener conexión a internet
- Algunos videos pueden tener restricciones de descarga

### Error de dependencias

- Actualiza pip: `pip install --upgrade pip`
- Reinstala las dependencias: `pip install -r requirements.txt --force-reinstall`

## 📜 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Siéntete libre de abrir issues o pull requests.

---

Hecho con ❤️ usando Python y Streamlit
