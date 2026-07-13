from app.worker.celery_app import celery_app
import trafilatura
import ollama

from langchain_text_splitters import RecursiveCharacterTextSplitter


@celery_app.task
def process_news_task(title, url):

    print(f"Processing: {title}")

    try:

        # STEP 1 — Download webpage
        downloaded = trafilatura.fetch_url(url)

        if not downloaded:
            raise Exception("Failed to download article")

        # STEP 2 — Extract clean article text
        content = trafilatura.extract(downloaded)

        if not content:
            raise Exception("Failed to extract content")

        print("\n====================")
        print("ARTICLE EXTRACTED")
        print("====================\n")

        # STEP 3 — Chunking
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=100
        )

        chunks = splitter.split_text(content)

        print(f"TOTAL CHUNKS: {len(chunks)}")

        # STEP 4 — Print chunks
        for i, chunk in enumerate(chunks[:3]):

            print("\n======================")
            print(f"CHUNK {i+1}")
            print("======================")
            print(chunk[:500])

        # STEP 5 — Generate embeddings
        embeddings_list = []

        for i, chunk in enumerate(chunks):
            

            response = ollama.embeddings(
                model="mxbai-embed-large",
                prompt=chunk
            )

            vector = response["embedding"]

            embeddings_list.append({
                "text": chunk,
                "embedding": vector
            })

            print("\n======================")
            print(f"EMBEDDING {i+1}")
            print("======================")
            print(f"Vector Dimensions: {len(vector)}")
            print(vector[:5])

        print(f"\nGenerated embeddings: {len(embeddings_list)}")

        return {
            "status": "success",
            "title": title,
            "chunks": len(chunks),
            "embeddings": len(embeddings_list)
        }

    except Exception as e:

        print(f"ERROR: {e}")

        return {
            "status": "failed",
            "error": str(e)
        }