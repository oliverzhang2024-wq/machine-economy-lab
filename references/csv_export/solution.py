import csv
import io

def export_rows(rows, columns):
    if not columns or len(set(columns)) != len(columns):
        raise ValueError('columns must be nonempty and unique')
    out = io.StringIO(newline='')
    writer = csv.writer(out, lineterminator='\n')
    writer.writerow(columns)
    for row in rows:
        writer.writerow(['' if row.get(k) is None else str(row.get(k)) for k in columns])
    return out.getvalue()
