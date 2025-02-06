import faiss
import numpy as np
import pandas as pd
import logging
from datetime import datetime
from tqdm import tqdm
import torch
from sentence_transformers import SentenceTransformer
import time
# 로거 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('embedding_log.log'),
        logging.StreamHandler()
    ]
)

class LocalEmbeddingGenerator:
    def __init__(self, model_name="BAAI/bge-m3", device='cuda', batch_size=32):
        self.model = SentenceTransformer(model_name, device=device)
        self.batch_size = batch_size
        self.device = device
        self.total_processed = 0
        
        if not torch.cuda.is_available():
            logging.warning("CUDA is not available. Using CPU instead.")
            self.device = 'cpu'

    def generate_embeddings(self, texts):
        try:
            embeddings = self.model.encode(texts, 
                                         batch_size=self.batch_size,
                                         convert_to_numpy=True,
                                         normalize_embeddings=True)
            self.total_processed += len(texts)
            return embeddings
        except Exception as e:
            logging.error(f"Error generating embeddings: {str(e)}")
            raise

if __name__ == '__main__':
    start_total = time.time()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Loading dataset...")
        data = pd.read_csv("book_info3차.csv")
        final_answers = data["Final Answer"].tolist()
        total_records = len(final_answers)
        
        embedder = LocalEmbeddingGenerator(device='cuda')
        
        embeddings = []
        progress_bar = tqdm(total=total_records, desc="Generating Embeddings", unit="rec")
        
        for i in range(0, total_records, embedder.batch_size):
            batch_texts = final_answers[i:i+embedder.batch_size]
            
            try:
                batch_embeddings = embedder.generate_embeddings(batch_texts)
                embeddings.extend(batch_embeddings)
                
                progress_bar.update(len(batch_texts))
                progress_bar.set_postfix({
                    "Device": embedder.device.upper(),
                    "Batch Size": embedder.batch_size,
                    "Processed": embedder.total_processed
                })
                
            except Exception as e:
                logger.error(f"Error processing batch {i//embedder.batch_size}: {str(e)}")
                continue

        logger.info("Creating FAISS index...")
        dimension = embeddings[0].shape[0]
        embeddings_array = np.array(embeddings, dtype='float32')
        
        index = faiss.IndexFlatIP(dimension)
        index.add(embeddings_array)
        faiss.write_index(index, "vector_store_100003차.index")

        total_time = time.time() - start_total
        logger.info(f"""
        ===== Processing Complete =====
        Total Records: {total_records}
        Successful Embeddings: {len(embeddings)}
        Total Time: {total_time:.2f} seconds
        Embedding Speed: {total_records/total_time:.2f} rec/sec
        Device Used: {embedder.device.upper()}
        """)

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        raise
