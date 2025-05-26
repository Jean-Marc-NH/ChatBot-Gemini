import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import (
    SPOTIPY_CLIENT_ID,
    SPOTIPY_CLIENT_SECRET,
    SPOTIPY_REDIRECT_URI
)

class SpotifyController:
    def __init__(self, usuario_id: str = None):
        self.usuario_id = usuario_id or "default"
        self.scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI,
            scope=self.scope,
            cache_path=f"Usuarios/{self.usuario_id}/.cache"
        ))

    def _obtener_device_id(self):
        devices = self.sp.devices()
        for d in devices["devices"]:
            print(d)
            if d["is_active"] and d["type"] == "Computer":
                return d["id"]
        return None


    def reproducir_playlist(self, nombre_playlist: str):
        device_id = self._obtener_device_id()
        resultados = self.sp.search(q=nombre_playlist, type='playlist', limit=1)
        if resultados["playlists"]["items"]:
            playlist_uri = resultados["playlists"]["items"][0]["uri"]
            self.sp.start_playback(device_id=device_id, context_uri=playlist_uri)
            return f"Reproduciendo la playlist: {nombre_playlist}"
        return "No encontré esa playlist."

    def reproducir_artista(self, nombre_artista: str):
        device_id = self._obtener_device_id()
        resultados = self.sp.search(q=nombre_artista, type='artist', limit=1)
        if resultados["artists"]["items"]:
            artista_uri = resultados["artists"]["items"][0]["uri"]
            self.sp.start_playback(device_id=device_id, context_uri=artista_uri)
            return f"Reproduciendo música de {nombre_artista}"
        return "No encontré ese artista."

    def pausar(self):
        self.sp.pause_playback()
        return "Música en pausa."

    def continuar(self):
        self.sp.start_playback()
        return "Continuando la reproducción."

    def siguiente(self):
        self.sp.next_track()
        return "Pasando a la siguiente canción."

    def que_suena(self):
        actual = self.sp.current_playback()
        if actual and actual["is_playing"]:
            nombre = actual["item"]["name"]
            artista = actual["item"]["artists"][0]["name"]
            return f"Está sonando '{nombre}' de {artista}"
        return "No hay música sonando ahora."
    
    def reproducir(self, tipo: str, valor: str) -> str:
        device_id = self._obtener_device_id()

        if tipo == "artista":
            resultados = self.sp.search(q=f"artist:{valor}", type="artist", limit=1)
            if resultados["artists"]["items"]:
                uri = resultados["artists"]["items"][0]["uri"]
                self.sp.start_playback(device_id=device_id, context_uri=uri)

                return f"Reproduciendo artista: {valor}"
            else:
                return f"No encontré al artista {valor}."
    
        elif tipo == "cancion":
            resultados = self.sp.search(q=f"track:{valor}", type="track", limit=1)
            if resultados["tracks"]["items"]:
                uri = resultados["tracks"]["items"][0]["uri"]
                self.sp.start_playback(device_id=device_id, context_uri=uri)
                return f"Reproduciendo canción: {valor}"
            else:
                return f"No encontré la canción {valor}."
    
        elif tipo == "playlist":
            resultados = self.sp.search(q=valor, type="playlist", limit=1)
            if resultados["playlists"]["items"]:
                uri = resultados["playlists"]["items"][0]["uri"]
                self.sp.start_playback(device_id=device_id, context_uri=uri)
                return f"Reproduciendo playlist: {valor}"
            else:
                return f"No encontré una playlist llamada {valor}."
    
        elif tipo == "genero":
            resultados = self.sp.search(q=valor, type="playlist", limit=1)
            if resultados["playlists"]["items"]:
                uri = resultados["playlists"]["items"][0]["uri"]
                self.sp.start_playback(device_id=device_id, context_uri=uri)
                return f"Reproduciendo música de género: {valor}"
            else:
                return f"No encontré contenido para el género {valor}."
    
        else:
            return "No entendí qué querés que reproduzca."

