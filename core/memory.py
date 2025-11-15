"""Memory Management System with ChromaDB"""
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain.embeddings import GoogleGenerativeAIEmbeddings

from config.settings import settings

logger = logging.getLogger(__name__)


class AgentMemory:
    """Memory management using ChromaDB for intelligent retrieval"""
    
    def __init__(self):
        """Initialize ChromaDB client and embeddings"""
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_PATH
        )
        
        # Initialize embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=settings.GOOGLE_API_KEY
        )
        
        # Initialize collections
        self.knowledge_collection = self.client.get_or_create_collection(
            name="agent_knowledge_base",
            metadata={"hnsw:space": "cosine"}
        )
        
        self.task_collection = self.client.get_or_create_collection(
            name="agent_tasks",
            metadata={"hnsw:space": "cosine"}
        )
        
        self.results_collection = self.client.get_or_create_collection(
            name="task_results",
            metadata={"hnsw:space": "cosine"}
        )
        
        logger.info("✅ AgentMemory initialized")
    
    def store_knowledge(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Store knowledge in memory
        
        Args:
            content: Content to store
            metadata: Optional metadata
            
        Returns:
            Document ID
        """
        try:
            doc_id = f"knowledge_{datetime.now().timestamp()}"
            embedding = self.embeddings.embed_query(content)
            
            meta = metadata or {}
            meta["timestamp"] = datetime.now().isoformat()
            meta["type"] = "knowledge"
            
            self.knowledge_collection.add(
                documents=[content],
                embeddings=[embedding],
                metadatas=[meta],
                ids=[doc_id]
            )
            
            logger.info(f"✅ Knowledge stored: {doc_id}")
            return doc_id
        except Exception as e:
            logger.error(f"❌ Failed to store knowledge: {str(e)}")
            raise
    
    def retrieve_knowledge(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant knowledge
        
        Args:
            query: Query to search
            top_k: Number of results to return
            
        Returns:
            List of relevant documents
        """
        try:
            embedding = self.embeddings.embed_query(query)
            
            results = self.knowledge_collection.query(
                query_embeddings=[embedding],
                n_results=top_k
            )
            
            documents = []
            if results and results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    documents.append({
                        "content": doc,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "distance": results["distances"][0][i] if results["distances"] else 0
                    })
            
            return documents
        except Exception as e:
            logger.error(f"❌ Failed to retrieve knowledge: {str(e)}")
            return []
    
    def store_task_history(self, task_name: str, task_data: Dict[str, Any]) -> str:
        """Store task history
        
        Args:
            task_name: Name of the task
            task_data: Task data
            
        Returns:
            Task ID
        """
        try:
            task_id = f"task_{task_name}_{datetime.now().timestamp()}"
            content = json.dumps(task_data)
            embedding = self.embeddings.embed_query(content)
            
            metadata = {
                "task_name": task_name,
                "timestamp": datetime.now().isoformat(),
                "type": "task"
            }
            
            self.task_collection.add(
                documents=[content],
                embeddings=[embedding],
                metadatas=[metadata],
                ids=[task_id]
            )
            
            return task_id
        except Exception as e:
            logger.error(f"❌ Failed to store task: {str(e)}")
            raise
    
    def retrieve_similar_tasks(self, task_description: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve similar past tasks
        
        Args:
            task_description: Description of the task
            top_k: Number of similar tasks
            
        Returns:
            List of similar tasks
        """
        try:
            embedding = self.embeddings.embed_query(task_description)
            
            results = self.task_collection.query(
                query_embeddings=[embedding],
                n_results=top_k
            )
            
            tasks = []
            if results and results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    tasks.append({
                        "task_data": json.loads(doc),
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "similarity": 1 - results["distances"][0][i] if results["distances"] else 0
                    })
            
            return tasks
        except Exception as e:
            logger.error(f"❌ Failed to retrieve similar tasks: {str(e)}")
            return []
    
    def store_result(self, task_id: str, result: Dict[str, Any]) -> str:
        """Store task result
        
        Args:
            task_id: ID of the task
            result: Result data
            
        Returns:
            Result ID
        """
        try:
            result_id = f"result_{task_id}_{datetime.now().timestamp()}"
            content = json.dumps(result)
            embedding = self.embeddings.embed_query(content)
            
            metadata = {
                "task_id": task_id,
                "timestamp": datetime.now().isoformat(),
                "type": "result"
            }
            
            self.results_collection.add(
                documents=[content],
                embeddings=[embedding],
                metadatas=[metadata],
                ids=[result_id]
            )
            
            return result_id
        except Exception as e:
            logger.error(f"❌ Failed to store result: {str(e)}")
            raise
    
    def clear_memory(self):
        """Clear all memories"""
        try:
            self.client.delete_collection(name="agent_knowledge_base")
            self.client.delete_collection(name="agent_tasks")
            self.client.delete_collection(name="task_results")
            logger.info("✅ Memory cleared")
        except Exception as e:
            logger.error(f"❌ Failed to clear memory: {str(e)}")


# Global memory instance
_memory: Optional[AgentMemory] = None


def get_memory() -> AgentMemory:
    """Get or create the global memory instance"""
    global _memory
    if _memory is None:
        _memory = AgentMemory()
    return _memory
