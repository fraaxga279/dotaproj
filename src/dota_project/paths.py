from pathlib import Path
import os


def data_path(root):
    folder = Path(os.environ.get('DOTA_DATA_DIR', root / 'data' / 'raw')).expanduser().resolve()
    required = ['matches_df_train.csv', 'matches_df_test.csv', 'player_df.csv', 'Constants.Heroes.csv', 'game_chat.csv', 'dota_adv.csv']
    missing = [name for name in required if not (folder / name).is_file()]
    if missing:
        raise FileNotFoundError('не хватает файлов: ' + ', '.join(missing))
    return folder


def output_path(root, name):
    folder = root / 'artifacts' / name
    folder.mkdir(parents=True, exist_ok=True)
    return folder
