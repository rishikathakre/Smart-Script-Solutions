from pathlib import Path
import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from transformers import pipeline
from fetch_transcript import zip_transcript  # Assuming you have defined these functions
from preprocessing import stride_sentences  # Assuming you have defined these functions

class Engine:
    def __init__(self, transcript:list) -> None:
        self.base_path = Path('./models')

        self.qa_model_name = 'deepset/roberta-base-squad2'
        self.qa_model = pipeline('question-answering',model=self.qa_model_name)

        self.sim_model_name = 'Similarity_Model'  # Example sentence transformer model
        self.sim_model_path = str(self.base_path / self.sim_model_name)
        self.sim_model = SentenceTransformer(self.sim_model_path)

        self.timestamps, self.texts = zip_transcript(transcript).values()

        self.stride = 10
        self.text_groups = stride_sentences(self.texts, self.stride)

        self.embeddings = self._encode_transcript()

        self.summarization_model_name = "t5-base"           #text to text transfer transformer
        self.summarizer = pipeline("summarization", model=self.summarization_model_name)

    def summarize_video(self):
        try:
            video_text = ' '.join(self.texts).strip()
            summary = self.summarizer(video_text, max_length=1000, min_length=100, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            return f"Error summarizing video: {e}"

    def _encode_transcript(self):
        return self.sim_model.encode(self.text_groups)

    def ask(self, question_text:str):
        result = self.qa_model(
            question=question_text,
            context=' '.join(self.text_groups).strip(),
            doc_stride=256,
            max_answer_len=512,
            max_question_len=128,
        )
        return result['answer']

    def find_similar(self, txt:str, top_k=1):
        txt_embedding = self.sim_model.encode(txt)
        similarities = cos_sim(txt_embedding, self.embeddings)
        similarities = similarities.reshape(-1)
        indices = list(torch.argsort(similarities, descending=True))
        indices = [idx.item() for idx in indices][:top_k]
        groups = [self.text_groups[i] for i in indices]
        timestamps = [self.timestamps[self.stride * i] for i in indices]
        return groups, timestamps

if __name__ == '__main__':
    # Example usage
    transcript_data = [
        "This is the first sentence.",
        "This is the second sentence.",
        "This is the third sentence.",
        # Add more sentences as needed
    ]

    model = Engine(transcript_data)
    print(model.ask("What is the first sentence?"))
    print(model.find_similar("Find sentences similar to this.", top_k=2))
