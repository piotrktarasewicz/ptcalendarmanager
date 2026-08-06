# Plan testów PT Calendar Manager 0.16.3

1. Zainstaluj 0.16.3 na czystym koncie Windows bez katalogu `%APPDATA%\PT Calendar Manager` i bez dodatku NVDA Google Calendar Manager.
2. Uruchom program, naciśnij `Ctrl+L` i potwierdź, że otwiera się logowanie Google bez pytania o `client_secret.json`.
3. Anuluj albo dokończ logowanie i sprawdź, że nie pojawia się komunikat o braku konfiguracji OAuth.
4. Powtórz test dla wersji przenośnej rozpakowanej do nowego katalogu.
5. Zaktualizuj działającą wersję 0.16.2 do 0.16.3 i sprawdź zachowanie tokenu, ustawień, wybranych kalendarzy i języka.
6. Otwórz pomoc przez F1 oraz ze skrótu instalatora i sprawdź nagłówki w NVDA.
7. Sprawdź dodawanie, edycję i usuwanie zwykłego oraz cyklicznego wydarzenia.
8. Potwierdź, że archiwum źródłowe nie zawiera `client_secret.json`, `token.dat` ani `token.json`.
