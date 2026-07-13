from ollama import Client
import psycopg2
from pgvector.psycopg2 import register_vector

client = Client(base_url="http://ollama:11434")


def get_embedding(job):
    text = f"""
    Company: {job.get('company', '')}
    Title: {job.get('title', '')}
    Location: {job.get('location', '')}
    Region: {job.get('regions', '')}
    Salary: {job.get('salary_min', '')} - {job.get('salary_max', '')}
    """

    res = client.embeddings(
        model="mxbai-embed-large",
        prompt=text
    )

    return res["embedding"]


def ingest_jobs(df):
    conn = psycopg2.connect(
        "postgresql://postgres:postgres@pgvector-db:5432/ragdb"
    )

    register_vector(conn)
    cur = conn.cursor()

    for _, row in df.iterrows():
        job = row.to_dict()

        embedding = get_embedding(job)

        cur.execute(
            """
            INSERT INTO job_embeddings
            (company, title, location, salary_min, salary_max, embedding)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                job["company"],
                job["title"],
                job["location"],
                job["salary_min"],
                job["salary_max"],
                embedding
            )
        )

    conn.commit()
    cur.close()
    conn.close()

    print(f"✅ Ingested {len(df)} jobs into pgvector")