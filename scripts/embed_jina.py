"""in this script, we load arxiv metadata and compute vector embeddings
using jina embedding

"""
#%%
import argparse
import gzip
import json
import h5py
from datetime import datetime
from dateutil import parser as date_parser
from transformers import AutoModel

# fields to store
FIELDS = [
    'id',
    'authors',
    'title',
    'abstract',
    'categories',
    'versions_dates'
]

# utility functions
def parse_datetime_str(date_str):
    """parse date string from arxiv into rfc3339 format"""
    date = date_parser.parse(date_str)
    rfc3339_date = date.isoformat("T") + "Z"
    return rfc3339_date

def parse_json(json_obj):
    """parse json object from arxiv"""
    json_parsed = {}
    for f in FIELDS:
        if f == 'versions_dates':
            v = [parse_datetime_str(v_) for v_ in json_obj[f]]
        else:
            v = json_obj[f]
        json_parsed[f] = v
    return json_parsed

def text_repr(json_obj):
    """text representation of json object, used for embedding"""
    return f"title: {json_obj['title']}\nabstract: {json_obj['abstract'].strip()}"

def data_loader(fname, batch_size=1000, skip=None):
    """load data from gzip file"""
    with gzip.open(fname, 'rt') as f:
        batch = []
        l_counter = 0
        for line in f:
            l_counter += 1
            if (skip is None) or (l_counter > skip):
                json_object = parse_json(json.loads(line))
                batch += [json_object]
                if len(batch) == batch_size:
                    yield batch
                    batch = []
            else:
                if l_counter % 10000 == 0:
                    print(f"skipped {l_counter} lines")
    yield batch

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", help="Path to the data file")
    parser.add_argument("--ofile", help="Path to the output file")
    parser.add_argument("--skip", type=int, default=None)

    args = parser.parse_args()

    # create an output h5 file for storing the embedding
    h5f = h5py.File(args.ofile, 'a')

    # load embedding model
    model = AutoModel.from_pretrained(
        'jinaai/jina-embeddings-v2-base-en', 
        trust_remote_code=True,
        device_map='cuda'
    )
    n_records = 0
    for batch in data_loader(args.data, skip=args.skip):
        reprs = [text_repr(json_obj) for json_obj in batch]
        embeddings = model.encode(reprs)
        for json_obj, embedding in zip(batch, embeddings):
            if json_obj['id'] not in h5f:
                dset = h5f.create_dataset(json_obj['id'], data = embedding)
                dset.attrs['metadata'] = json.dumps(json_obj)
        n_records += len(reprs)
        if n_records % 10000 == 0:
            print(f"{datetime.now()} - {n_records} records processed")