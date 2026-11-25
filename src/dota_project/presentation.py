def tidy_outputs(notebook, log_path):
    markers = ['Pandas4Warning', 'UserWarning: Bins whose width', 'TqdmWarning', 'Best trial:', 'ExperimentalWarning', '0/25 [']
    records = []
    for index, cell in enumerate(notebook.cells):
        if cell.cell_type != 'code':
            continue
        kept = []
        for output in cell.outputs:
            if output.output_type == 'stream' and output.name == 'stderr':
                if any(marker in output.text for marker in markers):
                    records.append(f'ячейка {index + 1}\n{output.text}')
                    continue
                if not output.text.strip():
                    continue
            kept.append(output)
        cell.outputs = kept
    if records:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text('\n\n'.join(records))
