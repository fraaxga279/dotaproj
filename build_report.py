from pathlib import Path
import base64
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import nbformat

root = Path(__file__).resolve().parent
registry = pd.read_csv(root / 'artifacts' / 'advanced' / 'experiment_registry.csv')
config = json.loads((root / 'artifacts' / 'advanced' / 'advanced_config.json').read_text())
rows = []
for label, groups in [('baseline', []), ('baseline + чат', ['text']), ('baseline + тренды + чат', ['trend', 'text']), ('итоговая модель', config['groups'])]:
    matching = registry.loc[registry['groups'].map(lambda value: sorted(json.loads(value)) == sorted(groups))]
    if groups:
        matching = matching.loc[matching['C'].eq(0.1)]
    else:
        matching = matching.loc[matching['name'].eq('baseline')]
    rows.append({'модель': label, 'gini': matching.iloc[-1]['gini_valid']})
summary = pd.DataFrame(rows)
reports = root / 'reports'
figures = reports / 'figures'
figures.mkdir(parents=True, exist_ok=True)
summary.to_csv(reports / 'results.csv', index=False)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12, 'axes.spines.top': False, 'axes.spines.right': False})
fig, ax = plt.subplots(figsize=(10, 4.6), facecolor='#f7f8fa')
ax.set_facecolor('#f7f8fa')
colors = ['#a1acbd', '#879dc4', '#5e80b5', '#245da6']
bars = ax.barh(summary['модель'], summary['gini'], color=colors, height=0.62)
ax.invert_yaxis()
ax.set_xlim(0, 0.48)
ax.set_xlabel('gini на ноябрьской валидации')
ax.set_title('чат и динамика матча добавляют сигнал', loc='left', pad=18)
ax.grid(axis='x', alpha=0.16)
ax.set_axisbelow(True)
for bar, value in zip(bars, summary['gini']):
    ax.text(value + 0.006, bar.get_y() + bar.get_height() / 2, f'{value:.5f}', va='center')
fig.text(0.02, 0.01, 'обучение: январь–октябрь 2024 · валидация использовалась для отбора признаков', fontsize=9, color='#566176')
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig(figures / 'model_comparison.png', dpi=180)
plt.close(fig)
score = config['validation_gini']
delta = score - config['baseline_gini']
text = f'''# прогноз победителя dota 2

## задача

оценить вероятность победы radiant по составам команд и первым 15 минутам матча. в train 641 090 матчей, в test 59 748.

## подход

сначала используются регионы, циклические признаки даты, mmr и герои. затем добавляются tf-idf чата, статистики преимущества по золоту и опыту, тренды и временные окна. основная модель — логистическая регрессия.

## результат локального запуска

итоговый gini — {score:.5f}, прирост к baseline — {delta:.5f}. выбраны {', '.join(config['groups'])}. сравнение всех экспериментов лежит в журнале `artifacts/advanced/experiment_registry.csv`.

![сравнение моделей](figures/model_comparison.png)

## что было важно

проверять модель на будущем месяце, не использовать duration и закрытую статистику test, обучать преобразования только на train. отдельная обработка повреждённых составов позволяет сохранить все строки test. сохранение и загрузка pipeline проверены по совпадению прогнозов.

## ограничения и следующий шаг

ноябрь использовался и для отбора, и для оценки. качество на скрытом test неизвестно. дальше стоит проверить несколько временных разбиений и выделить отдельный финальный период. готовый pipeline рассчитан на имеющиеся match_id и требует обновления источников для новых матчей.
'''
(reports / 'summary.md').write_text(text)
for path in (root / 'notebooks').glob('*.ipynb'):
    notebook = nbformat.read(path, as_version=4)
    number = 0
    for cell in notebook.cells:
        for output in cell.get('outputs', []):
            png = output.get('data', {}).get('image/png')
            if png:
                number += 1
                (figures / f'{path.stem}_{number:02}.png').write_bytes(base64.b64decode(png))
print('отчёт и графики сохранены')
