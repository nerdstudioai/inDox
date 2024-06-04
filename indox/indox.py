from typing import List, Any, Tuple
import warnings
import logging
from .visualization import visualize_contexts_
from .utils import clear_log_file

warnings.filterwarnings("ignore")

# Set up logging
logging.basicConfig(filename='indox.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')


class IndoxRetrievalAugmentation:
    def __init__(self):
        """
        Initialize the IndoxRetrievalAugmentation class
        """
        self.db = None
        self.qa_history = []
        logging.info("IndoxRetrievalAugmentation initialized")

    def connect_to_vectorstore(self, vectorstore_database):
        """
        Establish a connection to the vector store database using configuration parameters.
        """
        try:
            logging.info("Attempting to connect to the vector store database")
            self.db = vectorstore_database

            if self.db is None:
                raise RuntimeError('Failed to connect to the vector store database.')

            logging.info("Connection to the vector store database established successfully")
            return self.db
        except ValueError as ve:
            logging.error(f"Invalid input: {ve}")
            raise ValueError(f"Invalid input: {ve}")
        except RuntimeError as re:
            logging.error(f"Runtime error: {re}")
            raise RuntimeError(f"Runtime error: {re}")
        except Exception as e:
            logging.error(f"Failed to connect to the database due to an unexpected error: {e}")
            raise RuntimeError(f"Failed to connect to the database due to an unexpected error: {e}")

    def store_in_vectorstore(self, docs: List[str]) -> Any:
        """
        Store text chunks into a vector store database.
        """
        if not docs or not isinstance(docs, list):
            logging.error("The `docs` parameter must be a non-empty list.")
            raise ValueError("The `docs` parameter must be a non-empty list.")

        try:
            logging.info("Storing documents in the vector store")
            if self.db is not None:
                self.db.add_document(docs)
            else:
                raise RuntimeError("The vector store database is not initialized.")

            logging.info("Documents stored successfully")
            return self.db
        except ValueError as ve:
            logging.error(f"Invalid input data: {ve}")
            raise ValueError(f"Invalid input data: {ve}")
        except RuntimeError as re:
            logging.error(f"Runtime error while storing in the vector store: {re}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error while storing in the vector store: {e}")
            return None

    # def answer_question(self, qa_model, query: str, db=None, top_k: int = 5, document_relevancy_filter: bool = False,
    #                     generate_clustered_prompts: bool = False) -> Tuple[str, Tuple[List[str], List[float]]]:
    #     """
    #     Answer a query using the QA model, finding the most relevant document chunks in the database.
    #     """
    #     if not query:
    #         logging.error("Query string cannot be empty.")
    #         raise ValueError("Query string cannot be empty.")
    #
    #     vector_database = db if db is not None else self.db
    #
    #     if vector_database is None:
    #         logging.error("Vector store database is not initialized.")
    #         raise RuntimeError("Vector store database is not initialized.")
    #
    #     try:
    #         logging.info("Retrieving context and scores from the vector database")
    #         context, scores = vector_database.retrieve(query, top_k=top_k)
    #         if generate_clustered_prompts:
    #             from .prompt_augmentation import generate_clustered_prompts
    #             context = generate_clustered_prompts(context, embeddings=vector_database.embeddings)
    #
    #         if not document_relevancy_filter:
    #             logging.info("Generating answer without document relevancy filter")
    #             answer = qa_model.answer_question(context=context, question=query)
    #         else:
    #             logging.info("Generating answer with document relevancy filter")
    #             from .prompt_augmentation import RAGGraph
    #             graph = RAGGraph(qa_model)
    #             graph_out = graph.run({'question': query, 'documents': context, 'scores': scores})
    #             answer = qa_model.answer_question(context=graph_out['documents'], question=graph_out['question'])
    #             context, scores = graph_out['documents'], graph_out['scores']
    #
    #         retrieve_context = (context, scores)
    #         new_entry = {'query': query, 'answer': answer, 'context': context, 'scores': scores}
    #         self.qa_history.append(new_entry)
    #         logging.info("Query answered successfully")
    #         return answer, retrieve_context
    #
    #     except ValueError as ve:
    #         logging.error(f"Invalid input data: {ve}")
    #         raise ValueError(f"Invalid input data: {ve}")
    #     except RuntimeError as re:
    #         logging.error(f"Runtime error while retrieving or answering the query: {re}")
    #         raise RuntimeError(f"Runtime error while retrieving or answering the query: {re}")
    #     except Exception as e:
    #         logging.error(f"Unexpected error while answering the question: {e}")
    #         raise RuntimeError(f"Unexpected error while answering the question: {e}")

    class QuestionAnswer:
        def __init__(self, llm, vector_database, top_k: int = 5, document_relevancy_filter: bool = False,
                     generate_clustered_prompts: bool = False):
            self.qa_model = llm
            self.document_relevancy_filter = document_relevancy_filter
            self.top_k = top_k
            self.generate_clustered_prompts = generate_clustered_prompts
            self.vector_database = vector_database
            self.qa_history = []
            self.context = []
            if self.vector_database is None:
                logging.error("Vector store database is not initialized.")
                raise RuntimeError("Vector store database is not initialized.")

        def invoke(self, query):
            if not query:
                logging.error("Query string cannot be empty.")
                raise ValueError("Query string cannot be empty.")
            try:
                logging.info("Retrieving context and scores from the vector database")
                context, scores = self.vector_database.retrieve(query, top_k=self.top_k)
                if self.generate_clustered_prompts:
                    from .prompt_augmentation import generate_clustered_prompts
                    context = generate_clustered_prompts(context, embeddings=self.vector_database.embeddings)

                if not self.document_relevancy_filter:
                    logging.info("Generating answer without document relevancy filter")
                    answer = self.qa_model.answer_question(context=context, question=query)
                else:
                    logging.info("Generating answer with document relevancy filter")
                    from .prompt_augmentation import RAGGraph
                    graph = RAGGraph(self.qa_model)
                    graph_out = graph.run({'question': query, 'documents': context, 'scores': scores})
                    answer = self.qa_model.answer_question(context=graph_out['documents'],
                                                           question=graph_out['question'])
                    context, scores = graph_out['documents'], graph_out['scores']

                retrieve_context = (context, scores)
                new_entry = {'query': query, 'answer': answer, 'context': context, 'scores': scores}
                self.qa_history.append(new_entry)
                self.context = retrieve_context
                logging.info("Query answered successfully")
                return answer
            except Exception as e:
                logging.error(f"Error while answering query: {e}")
                raise

    class Agent:
        def __init__(self, llm, vector_database, tools: list, top_k: int = 5):
            self.llm = llm
            self.tools = tools
            self.top_k = top_k
            self.vector_database = vector_database
            self.qa_history = []
            self.context = []
            if self.vector_database is None:
                logging.error("Vector store database is not initialized.")
                raise RuntimeError("Vector store database is not initialized.")

        def run(self, query):
            if not query:
                logging.error("Query string cannot be empty.")
                raise ValueError("Query string cannot be empty.")
            context, scores = self.vector_database.retrieve(query, top_k=self.top_k)
            from .prompt_augmentation import RAGGraph
            graph = RAGGraph(self.qa_model)
            graph_out = graph.run({'question': query, 'documents': context, 'scores': scores})
            answer = self.llm.answer_question(context=graph_out['documents'],
                                              question=graph_out['question'])
            context, scores = graph_out['documents'], graph_out['scores']
            if len(context < 1):
                #TODO Add agent functionality here
                # use llm.answer_with_agent
                pass


            
    # TODO add visualization for evaluation
    # def evaluate(self):
    #     """
    #     Evaluate the performance of the system based on the inputs provided from previous queries.
    #
    #     Returns:
    #     - dict: The evaluation metrics generated by `get_metrics` if inputs exist.
    #     - None: If no previous query results are available.
    #
    #     Raises:
    #     - RuntimeError: If no previous query results are available to evaluate.
    #     """
    #     if self.inputs:
    #         return get_metrics(self.inputs)
    #     else:
    #         raise RuntimeError("No inputs available for evaluation. Please make a query first.")

    # def visualize_context(self):
    #     """
    #     Visualize the context of the last query made by the user.
    #     """
    #     if not self.qa_history:
    #         print("No entries to visualize.")
    #         return
    #
    #     last_entry = self.qa_history[-1]
    #     return visualize_contexts_(last_entry['query'], last_entry['context'], last_entry['scores'])

    # def get_tokens_info(self):
    #     """
    #     Print an overview of the number of tokens used for different operations.
    #
    #     Displays the following token counts:
    #     - `input_tokens_all`: Number of input tokens sent to GPT-3.5 Turbo for summarization.
    #     - `output_tokens_all`: Number of output tokens received from GPT-3.5 Turbo.
    #     - `embedding_tokens`: Number of tokens used in the embedding process and sent to the database.
    #
    #     If no output tokens were used, only the embedding token information is displayed.
    #     """
    # if self.output_tokens_all > 0:
    #     print(
    #         f"""
    #         Overview of All Tokens Used:
    #         Input tokens sent to GPT-3.5 Turbo (Model ID: 0125) for summarizing: {self.input_tokens_all}
    #         Output tokens received from GPT-3.5 Turbo (Model ID: 0125): {self.output_tokens_all}
    #         Tokens used in the embedding section that were sent to the database: {self.embedding_tokens}
    #         """
    #     )
    # else:
    #     print(
    #         f"""
    #         Overview of All Tokens Used:
    #         Tokens used in the embedding section that were sent to the database: {self.embedding_tokens}
    #         """
    #     )
