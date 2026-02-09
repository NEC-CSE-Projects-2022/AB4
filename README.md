22471A0502 — Atmakuri Jagadeesh
Work Done: Dataset analysis, preprocessing, EDA, data construction

22471A0552 — Shaik Mohammad Farooq
Work Done: FLAN-T5 implementation, summary generation, prompt engineering

22471A0551 — Shaik Madeena Noushik
Work Done: BART zero-shot classification, genre prediction, evaluation

22471A0542 — Nalabolu Balakrishna Reddy
Work Done: Explainability using LIME, results analysis, documentation

📄 Abstract
Movie recommendation systems often suffer from data sparsity, cold-start problems, and lack of interpretability. This project proposes a transformer-based text classification framework using FLAN-T5 and BART on the MovieLens-100K dataset. FLAN-T5 is used to generate concise movie summaries from sparse metadata, while BART performs zero-shot multi-label genre classification. The system achieves competitive performance with an F1-score of 0.85 and integrates LIME to provide explainable genre predictions, improving transparency and trust in recommendation systems.

📚 Paper Reference (Inspiration)
👉 [Performance-Driven Text Classification on MovieLens-100K Using FLAN-T5 and BART –
Dr. Rizwana Syed et al.]
Original IEEE conference paper used as inspiration for the project.

🚀 Our Improvement Over Existing Paper
Simplified the workflow for easy reproducibility

Improved prompt construction for better summary quality

Added clearer evaluation metrics explanation

Integrated a user-friendly genre-based recommendation interface

Focused on CPU-based execution for accessibility

🧠 About the Project
What the project does
Generates movie summaries using FLAN-T5

Predicts movie genres using BART in a zero-shot setting

Recommends movies based on genre preferences

Explains predictions using LIME

Why it is useful
Works well with limited or sparse text data

Reduces dependency on user history

Improves transparency in recommendations

Suitable for cold-start scenarios

Project Workflow
Input (Movie title & metadata)
→ Text preprocessing
→ FLAN-T5 summary generation
→ BART zero-shot genre classification
→ Evaluation & LIME explainability
→ Genre-based recommendations

📊 Dataset Used
👉 MovieLens-100K Dataset

Dataset Details
100,000 ratings

1,682 movies

943 users

19 genre labels

Multi-label classification problem

🧰 Dependencies Used
Python

Transformers (Hugging Face)

PyTorch

Scikit-learn

Pandas

NumPy

LIME

🔍 EDA & Preprocessing
Analyzed genre distribution

Constructed synthetic text using movie titles and tags

Lowercasing and punctuation removal

Normalized and tokenized text

Train-test split (80% / 20%) with genre balance

⚙️ Model Training Info
FLAN-T5: Prompt-based text-to-text classification

BART: Zero-shot classification using bart-large-mnli

No fine-tuning required

Implemented using Hugging Face pipelines

🧪 Model Testing / Evaluation
Evaluation metrics used:

Accuracy

Precision

Recall

F1-Score

Performance Summary
Model	Precision	Recall	F1-Score
FLAN-T5	0.89	0.87	0.85
BART	0.84	0.81	0.82
📈 Results
FLAN-T5 produced high-quality movie summaries

Accurate multi-label genre prediction

Strong performance despite sparse data

Explainable predictions using LIME

Effective genre-based recommendations

⚠️ Limitations & Future Work
Dataset imbalance affects rare genres

No multimodal inputs (audio/video)

Future work includes:

Larger datasets

Multimodal learning

SHAP-based explainability

Real-time deployment

🌐 Deployment Info
Prototype UI for genre-based recommendations

Can be deployed using:

Streamlit / Flask

Google Colab / Local system

Runs efficiently on CPU (no GPU required)
