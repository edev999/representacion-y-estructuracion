import requests
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata
from understatapi import UnderstatClient
import sys
import re

sys.stdout.reconfigure(encoding="utf-8")
position_map = {
    "Centre-Forward": "ST",
    "Second Striker": "ST",

    "Left Winger": "ST",
    "Right Winger": "ST",

    "Attacking Midfield": "CM",

    "Central Midfield": "CM",
    "Left Midfield": "CM",
    "Right Midfield": "CM",

    "Defensive Midfield": "CM",

    "Left-Back": "CB",
    "Right-Back": "CB",
    "Centre-Back": "CB",

    "Goalkeeper": "GK"
}

def limpiar_nombre(nombre):
    if pd.isna(nombre):
        return ""

    nombre = str(nombre).lower().strip()

    # convertir guiones en espacio
    nombre = nombre.replace("-", " ")

    # quitar tildes
    nombre = "".join(
        c
        for c in unicodedata.normalize("NFD", nombre)
        if unicodedata.category(c) != "Mn"
    )

    # quitar símbolos
    nombre = re.sub(r"[^a-z\s]", "", nombre)

    nombre = " ".join(nombre.split())

    # quedarse con nombre + primer apellido
    partes = nombre.split()
    nombre = " ".join(partes[:2])

    return nombre


def obtener_datos_understat(temporada="2025"):
    """Descarga los datos base ofensivos y de xG desde Understat (Sin La Liga)."""
    # Hemos quitado 'La_Liga' de aquí
    ligas = ["La_Liga", "EPL", "Bundesliga", "Serie_A", "Ligue_1"]
    todos_los_jugadores = []

    print("\n[1/2] Iniciando descarga masiva desde UnderstatAPI...")

    with UnderstatClient() as understat:
        for liga in ligas:
            print(f"  -> Descargando datos de la liga: {liga}...")
            try:
                data = understat.league(league=liga).get_player_data(season=temporada)
                df_liga = pd.DataFrame(data)
                df_liga["League"] = liga
                todos_los_jugadores.append(df_liga)
                print(f"{len(df_liga)} jugadores descargados de {liga}.")
            except Exception as e:
                print(f"Error al descargar datos de {liga}: {e}")

    if todos_los_jugadores:
        df_final = pd.concat(todos_los_jugadores, ignore_index=True)
        cols_numericas = ["goals", "time", "assists"]

        for col in cols_numericas:
            if col in df_final.columns:
                df_final[col] = pd.to_numeric(df_final[col], errors="coerce")

        # Creamos la columna limpia para futuros cruces
        df_final["player_name_limpio"] = df_final["player_name"].apply(limpiar_nombre)

        print(f" Fase 1 completada. {len(df_final)} jugadores en la base de datos.")
        return df_final
    else:
        print("\n No se pudieron descargar datos de Understat.")
        return None


# Limpiar valores €
def clean_value(v):
    v = v.replace("€", "").replace(",", "").lower()
    if "m" in v:
        return float(v.replace("m", "")) * 1_000_000
    if "k" in v:
        return float(v.replace("k", "")) * 1_000
    return None


def main():
    print(" INICIANDO PIPELINE DE SCOUTING (EPL, BUNDESLIGA, SERIE A, LIGUE 1)...")
    headers = {"User-Agent": "Mozilla/5.0"}

    leagues = {
        "LaLiga": "ES1",
        "PremierLeague": "GB1",
        "Bundesliga": "L1",
        "SerieA": "IT1",
        "Ligue1": "FR1",
    }

    players = []
    teams = []
    nationalities = []
    league_names = []
    values = []
    ages = []
    positions = []

    for league, code in leagues.items():
        print("Descargando:", league)
        for page in range(1, 20):
            url = f"https://www.transfermarkt.com/{league.lower()}/marktwerte/wettbewerb/{code}/page/{page}"
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, "lxml")
            rows = soup.select("table.items tbody tr")
            if not rows:
                break
            for row in rows:
                name_tag = row.select_one("td.hauptlink a")
                value_tag = row.select_one("td.rechts.hauptlink")
                td_zentriert = row.select("td.zentriert")
                if name_tag and value_tag:
                    players.append(name_tag.text.strip())
                    values.append(value_tag.text.strip())
                    league_names.append(league)

                    # Nacionalidad
                    nat_img = row.select_one("img.flaggenrahmen")
                    if nat_img and nat_img.get("title"):
                        nationalities.append(nat_img.get("title").strip())
                    else:
                        nationalities.append("Unknown")

                    # Equipo (cuarto td.zentriert, índice 3)
                    if len(td_zentriert) >= 4:
                        club_a = td_zentriert[3].select_one("a")
                        if club_a and club_a.get("title"):
                            teams.append(club_a.get("title").strip())
                        else:
                            teams.append("Unknown")
                    else:
                        teams.append("Unknown")
                    # Edad (tercer td.zentriert)
                    if len(td_zentriert) >= 3:
                        age_text = td_zentriert[2].text.strip()
                        try:
                            ages.append(int(age_text))
                        except:
                            ages.append(None)
                    else:
                        ages.append(None)
                    # Posicion
                    pos_tag = row.select_one("table.inline-table tr:nth-of-type(2) td")
                    if pos_tag:
                        positions.append(pos_tag.text.strip())
                    else:
                        positions.append("Unknown")

    # Crear dataframe
    df = pd.DataFrame(
        {
            "Player": players,
            "Team": teams,
            "Nationality": nationalities,
            "League": league_names,
            "Age": ages,
            "Position": positions,
            "MarketValue": values,
        }
    )
    df["Position"] = df["Position"].map(position_map).fillna(df["Position"])
    league_map = {
        "PremierLeague": "EPL",
        "LaLiga": "La_Liga",
        "Bundesliga": "Bundesliga",
        "SerieA": "Serie_A",
        "Ligue1": "Ligue_1",
    }

    df["League"] = df["League"].map(league_map)
    # 1. Base Understat
    df_stats = obtener_datos_understat(temporada="2025")
    if df_stats is None:
        return

    df["MarketValue"] = df["MarketValue"].apply(clean_value)
    # Prepara columnas limpias para el merge
    df["player_name_limpio"] = df["Player"].apply(limpiar_nombre)
    tm_players = set(df["player_name_limpio"])
    us_players = set(df_stats["player_name_limpio"])

    missing = tm_players - us_players
    print("Jugadores en Transfermarkt pero no en Understat:", list(missing)[:20])

    # Merge (inner, solo jugadores que aparecen en ambos datasets)
    df_merged = pd.merge(
        df,
        df_stats,
        left_on=["player_name_limpio", "League"],
        right_on=["player_name_limpio", "League"],
        how="inner",
        suffixes=("_tm", "_understat"),
    )

    # Opcional: eliminar columnas duplicadas o renombrar para claridad
    df_merged.drop_duplicates(subset=["player_name_limpio", "League"], inplace=True)
    # Columnas numéricas que quieres conservar de Understat
    cols_numericas = ["goals", "time", "assists"]

    # Columnas que quieres mantener de Transfermarkt (puedes ajustar si quieres más)
    cols_transfermarkt = [
        "Player",
        "Team",
        "Nationality",
        "Age",
        "League",
        "Position",
        "MarketValue",
    ]

    # Seleccionar solo esas columnas de cada dataframe en el combinado
    df_merged_reducido = df_merged[
        cols_transfermarkt + [col for col in cols_numericas if col in df_merged.columns]
    ]

    print(
        f"Jugadores combinados con solo columnas numéricas y Transfermarkt: {len(df_merged_reducido)}"
    )
    print(df_merged_reducido.head())

    # Guardar resultado combinado
    df_merged_reducido.to_csv(
        "jugadores_combinados.csv", encoding="utf-8-sig", index=False
    )


# Punto de entrada del script
if __name__ == "__main__":

    main()
