import faiss
import numpy as np

index_files = [
    "vector_store_100002차.index", 
    "vector_store_100003차.index"
]

def merge_index_files(file_list, output_file):
    merged_index = faiss.read_index(file_list[0])
    
    for file in file_list[1:]:
        current_index = faiss.read_index(file)
        merged_index.add(current_index.reconstruct_n(0, current_index.ntotal))
    
    faiss.write_index(merged_index, output_file)
    print(f"Total vectors: {merged_index.ntotal}")

merge_index_files(index_files, "vector_store_total.index")
