


from app.services.extract import extract_and_save_executives
from app.pipelines.job_rag_pipeline import ingest_jobs


def main():
    df = extract_and_save_executives()
    ingest_jobs(df)


if __name__ == "__main__":
    main()