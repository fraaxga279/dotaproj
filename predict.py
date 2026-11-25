from pathlib import Path
import argparse
import cloudpickle
import numpy as np
import pandas as pd


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description='прогноз по сохранённой модели')
    parser.add_argument('--input', type=Path, default=root / 'data' / 'raw' / 'matches_df_test.csv')
    parser.add_argument('--model', type=Path, default=root / 'artifacts' / 'advanced' / 'dota_advanced_pipeline.pkl')
    parser.add_argument('--output', type=Path, default=root / 'artifacts' / 'advanced' / 'predictions.csv')
    args = parser.parse_args()
    frame = pd.read_csv(args.input)
    required = {'match_id', 'date', 'region', 'avg_mmr'}
    if not required.issubset(frame.columns):
        raise ValueError('не хватает колонок: ' + ', '.join(sorted(required - set(frame.columns))))
    if frame['match_id'].isna().any() or not frame['match_id'].is_unique:
        raise ValueError('match_id должен быть уникальным и без пропусков')
    with args.model.open('rb') as file:
        model = cloudpickle.load(file)
    sources = [table.index for table in model.tables_.values()]
    if 'text' in model.groups:
        sources.append(model.chat_.index)
    if any(not frame['match_id'].isin(index).all() for index in sources):
        raise ValueError('для части матчей нет дополнительных данных, сначала обнови источники модели')
    values = model.predict_proba(frame)[:, 1]
    if not (np.isfinite(values).all() and ((values >= 0) & (values <= 1)).all()):
        raise ValueError('получились некорректные вероятности')
    result = pd.DataFrame({'ID': frame['match_id'], 'Value': values})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    print('сохранено строк:', len(result))


if __name__ == '__main__':
    main()
