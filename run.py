from pathlib import Path
import argparse
import os
import sys

os.environ.setdefault('MPLBACKEND', 'Agg')
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('MPLCONFIGDIR', '/tmp/dota-matplotlib')

import nbformat
from nbclient import NotebookClient


def main():
    parser = argparse.ArgumentParser(description='запуск исследования dota 2')
    parser.add_argument('notebook', choices=['baseline', 'features', 'all'])
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    names = {'baseline': '01_baseline.ipynb', 'features': '02_features.ipynb'}
    selected = list(names) if args.notebook == 'all' else [args.notebook]
    for name in selected:
        path = root / 'notebooks' / names[name]
        notebook = nbformat.read(path, as_version=4)
        print('запускаю', path.name, flush=True)
        client = NotebookClient(notebook, timeout=7200, resources={'metadata': {'path': str(root)}}, kernel_name='python3')
        client.on_cell_executed = lambda cell, cell_index, execute_reply: print('ячейка', cell_index + 1, 'готова', flush=True)
        client.execute()
        sys.path.insert(0, str(root / 'src'))
        from dota_project.presentation import tidy_outputs
        tidy_outputs(notebook, root / 'reports' / (path.stem + '_execution.log'))
        nbformat.validate(notebook)
        nbformat.write(notebook, path)
        print('готово', path.name, flush=True)


if __name__ == '__main__':
    main()
