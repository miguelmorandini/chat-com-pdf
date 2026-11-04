import unittest
import hashlib
from src.ingest_pipeline import criar_chunks

class TestIncrementalPipeline(unittest.TestCase):
    def test_chunking_and_metadata(self):
        doc = {
            "titulo": "Lakehouse Medallion",
            "url": "https://docs.databricks.com/aws/en/lakehouse/medallion",
            "conteudo": "A arquitetura medalhao divide os dados em bronze, silver e gold. " * 15,
            "hash": "test_hash"
        }
        chunks = criar_chunks(doc, tamanho=200, overlap=50)
        self.assertGreater(len(chunks), 1)
        self.assertEqual(chunks[0]["titulo"], "Lakehouse Medallion")
        self.assertEqual(chunks[0]["url"], "https://docs.databricks.com/aws/en/lakehouse/medallion")

    def test_hash_calculation(self):
        txt1 = "Delta Lake ACID transactions"
        txt2 = "Delta Lake ACID transactions"
        txt3 = "Delta Lake ACID transactions modified"

        h1 = hashlib.sha256(txt1.encode("utf-8")).hexdigest()
        h2 = hashlib.sha256(txt2.encode("utf-8")).hexdigest()
        h3 = hashlib.sha256(txt3.encode("utf-8")).hexdigest()

        self.assertEqual(h1, h2)
        self.assertNotEqual(h1, h3)

if __name__ == "__main__":
    unittest.main()
