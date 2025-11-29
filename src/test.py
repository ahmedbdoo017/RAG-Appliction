# from qdrant_client import QdrantClient

# db_path = "assets/database/qdrant"
# client = QdrantClient(path=db_path)

# # شوف كل الـ collections الموجودة
# collections = client.get_collections()
# print(collections)


from qdrant_client import QdrantClient, models

db_path = "D:/mini-rag/src/assets/database/qdrant"
client = QdrantClient(path=db_path)

# إنشاء collection_1 لو مش موجودة
client.create_collection(
    collection_name="collection_1",
    vectors_config=models.VectorParams(
        size=768,  # حجم الـ embeddings بتاعك
        distance=models.Distance.COSINE
    )
)

# دلوقتي نجرب نجيب info
info = client.get_collection("collection_1")
print(info)
