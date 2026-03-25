from vector_db.parent_store_manager import ParentStoreManager
import asyncio

class DeterministicRetriever:

    def __init__(self, collection):
        self.collection = collection
        self.parent_store_manager = ParentStoreManager()

    async def deterministic_search_child_chunks(
        self,
        query: str,
        limit: int = 5,
        score_threshold: float = 0.7,
    ) -> list[dict]:
        """
        Deterministically search top-K child chunks.
        Returns structured data, not formatted strings.
        """
        try:
            # similarity_search is sync → offload to thread
            results = await asyncio.to_thread(
                self.collection.similarity_search_with_score,
                query,
                k=limit,
            )

            filtered_results = []
            for item in results:
                if isinstance(item, tuple) and len(item) == 2:
                    doc, score = item
                    if score >= score_threshold:
                        filtered_results.append(doc)
                else:
                    filtered_results.append(item)

            if not filtered_results:
                return []

            return [
                {
                    "parent_id": doc.metadata.get("parent_id", ""),
                    "file_name": doc.metadata.get("source", ""),
                    "content": doc.page_content.strip(),
                }
                for doc in filtered_results
            ]

        except Exception as e:
            raise RuntimeError(f"Child retrieval failed: {e}")
        
    async def deterministic_retrieve_parent_chunks(
        self,
        parent_id: str,
    ) -> dict | None:
        """
        Deterministically retrieve a parent chunk from disk.
        """
        try:
            parent = await self.parent_store_manager.load_content(parent_id)
            if not parent:
                return "NO_PARENT_DOCUMENT"

            return {
                "parent_id": parent_id,
                "file_name": parent.get("metadata", {}).get("source", "unknown"),
                "content": parent.get("page_content", "").strip(),
            }          

        except Exception as e:
            return f"PARENT_RETRIEVAL_ERROR: {str(e)}"

    async def deterministic_retrieval_workflow(
        self,
        query: str,
        limit: int = 5,
    ) -> dict:
        """
        Runs child + parent retrieval in parallel.
        """
        child_chunks = await self.deterministic_search_child_chunks(query, limit)
        if not child_chunks:
            return {
                "child_chunks": [],
                "parent_chunks": [],
            }

        parent_ids = {
            chunk["parent_id"]
            for chunk in child_chunks
            if chunk["parent_id"]
        }
        parent_tasks = [
            self.deterministic_retrieve_parent_chunks(pid)
            for pid in parent_ids
        ]
        parent_chunks = [
            p for p in await asyncio.gather(*parent_tasks)
            if p is not None
        ]

        return {
            "child_chunks": child_chunks,
            "parent_chunks": parent_chunks,
        }


    def format_retrieval_context(self, result: dict) -> str:
        sections = []

        if result["child_chunks"]:
            sections.append("### Child Chunks")
            for c in result["child_chunks"]:
                sections.append(
                    f"Parent ID: {c['parent_id']}\n"
                    f"File Name: {c['file_name']}\n"
                    f"Content: {c['content']}"
                )

        if result["parent_chunks"]:
            sections.append("\n### Parent Documents")
            for p in result["parent_chunks"]:
                sections.append(
                    f"Parent ID: {p['parent_id']}\n"
                    f"File Name: {p['file_name']}\n"
                    f"Content: {p['content']}"
                )

        return "\n\n".join(sections)