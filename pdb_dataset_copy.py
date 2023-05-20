import os
import sys

import torch
from torch.utils.data import Dataset
import json
import numpy as np
from torch.utils.data.dataloader import default_collate

import time

class ESMDataset(Dataset):
    def __init__(self, pdb_root, ann_paths, chain="C"):
        """
        protein (string): Root directory of protein (e.g. coco/images/)
        ann_root (string): directory to store the annotation file
        """
        self.pdb_root = pdb_root
        self.annotation = json.load(open(ann_paths, "r"))
        self.pdb_ids = {}
        self.chain = chain
        # self.protein_encoder = protein_encoder

    def __len__(self):
        return len(self.annotation)

    def __getitem__(self, index):

        ann = self.annotation[index]

        protein_embedding = '{}.pt'.format(ann["pdb_id"])

        protein_embedding_path = os.path.join(self.pdb_root, protein_embedding)
        protein_embedding = torch.load(protein_embedding_path, map_location=torch.device('cpu'))
        protein_embedding.requires_grad = False
        caption = ann["caption"]

        return {
            "text_input": caption,
            "encoder_out": protein_embedding,
            "chain": self.chain,
            "pdb_id": ann["pdb_id"]
        }

    def collater(self, samples):
        max_len_protein_dim0 = -1
        # updated_samples = []
        for pdb_json in samples:
            pdb_embeddings = pdb_json["encoder_out"]
            shape_dim0 = pdb_embeddings.shape[0]
            max_len_protein_dim0 = max(max_len_protein_dim0, shape_dim0)
        for pdb_json in samples:
            # new_pdb = {}
            pdb_embeddings = pdb_json["encoder_out"]
            shape_dim0 = pdb_embeddings.shape[0]
            pad1 = ((0, max_len_protein_dim0 - shape_dim0), (0, 0), (0, 0))
            arr1_padded = np.pad(pdb_embeddings, pad1, mode='constant', )
            # new_pdb["text_input"] = pdb_json["text_input"]
            # new_pdb["chain"] = pdb_json["chain"]
            # new_pdb["pdb_id"] = pdb_json["pdb_id"]
            # new_pdb["encoder_out"] = pdb_json["text_input"]
            pdb_json["encoder_out"] = arr1_padded

        # print(samples)
        # print(samples[0]["encoder_out"].shape)
        # print(samples[1]["encoder_out"].shape)
        return default_collate(samples)

