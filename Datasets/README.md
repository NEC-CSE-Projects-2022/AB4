# Performance-Driven Text Classification on MovieLens-100K

This repository contains the implementation and experiments for the research work **“Performance-Driven Text Classification on MovieLens-100K Using FLAN-T5 and BART”**. The project explores how modern transformer-based language models can be leveraged for movie genre prediction and recommendation using sparse textual information.

---

## 📌 Project Overview

Traditional recommender systems often rely heavily on user interaction history and structured metadata, which leads to issues such as sparsity, cold-start problems, and limited interpretability. This project proposes a **dual-model NLP framework** that:

- Generates enriched movie summaries using **FLAN-T5**
- Performs **zero-shot, multi-label genre classification** using **BART (MNLI)**
- Provides **explainability** of predictions using **LIME**

The framework is evaluated on the **MovieLens-100K** dataset and demonstrates competitive performance even without extensive fine-tuning or dense metadata.

---

## 🔗 Project Files & Resources

All relevant code, notebooks, outputs, datasets, and supplementary materials are available here:

👉 https://drive.google.com/drive/folders/1vGJoUxHApiE-aCwh35a0j1HggRPDcyzZ?usp=sharing

---

## 🧠 Key Contributions

- Utilization of **FLAN-T5** for prompt-based movie summary generation  
- Application of **BART** for zero-shot genre classification  
- Support for **multi-label genre prediction**  
- Integration of **LIME** for interpretable predictions  
- Reduced dependency on user interaction history  
- Effective performance on sparse text inputs

---

## 📂 Dataset

- **Dataset**: MovieLens-100K  
- **Size**: 100,000 ratings, 1,682 movies, 943 users  
- **Genres**: 19 possible labels (e.g., Action, Comedy, Drama, Thriller)

Since the dataset lacks detailed descriptions, structured text prompts were constructed using movie titles, genres, and tags to simulate real-world sparse-text scenarios.

---

## 🏗️ System Architecture

The framework follows a **dual-path pipeline**:

1. **FLAN-T5 Path**
   - Generates concise movie summaries using prompt-based text generation
   - Acts as a text-to-text classifier

2. **BART Path**
   - Performs zero-shot genre classification using generated summaries
   - Evaluates input against predefined genre labels without fine-tuning

Predictions from both models are evaluated against ground truth labels using standard classification metrics.

---

## ⚙️ Methodology

### 1. Data Ingestion
- Extract movie titles, genres, and available tags from MovieLens-100K

### 2. Preprocessing
- Text normalization (lowercasing, punctuation removal)
- Concatenation of fields into natural-language-like prompts

### 3. Tokenization
- Model-specific tokenizers for FLAN-T5 and BART

### 4. Model Application
- **FLAN-T5**: Prompt-based generative classification
- **BART**: Zero-shot discriminative classification

### 5. Evaluation
- Accuracy  
- Precision  
- Recall  
- F1-Score

---

## 📊 Experimental Results

| Model     | Precision | Recall | F1-Score |
|----------|-----------|--------|----------|
| FLAN-T5  | 0.89      | 0.87   | 0.85     |
| BART     | 0.84      | 0.81   | 0.82     |

**FLAN-T5 consistently outperformed BART**, especially in balancing precision and recall.

---

## 🧪 Sample Outputs

### Generated Movie Summaries (FLAN-T5)

- *Toy Story (1995)* – A group of toys comes to life and navigates friendship and adventure.  
- *GoldenEye (1995)* – A secret agent races to stop a satellite-based global threat.

### Predicted Genres (BART)

- *Toy Story (1995)* → Animation, Adventure, Comedy  
- *GoldenEye (1995)* → Action, Thriller, Adventure

---

## 🔍 Explainability with LIME

To improve transparency, **LIME** was used to highlight influential words contributing to genre predictions.

### Strengths
- Identifies meaningful genre cues such as *“crime”*, *“romantic”*, and *“detective”*  
- Builds trust by explaining why a movie was classified a certain way

### Limitations
- Analysis limited to a small number of examples  
- No quantitative comparison with expert annotations

---

## 💻 Technology Stack

- **Python**  
- **Hugging Face Transformers**  
- **FLAN-T5**  
- **BART (facebook/bart-large-mnli)**  
- **LIME**  
- **scikit-learn**, **pandas**, **numpy**

The experiments were conducted on a CPU-based system, but the code is compatible with GPU environments such as Google Colab.

---

## 🚀 Future Work

- Extend experiments to larger and more balanced datasets  
- Incorporate multi-modal features (audio, video)  
- Compare with additional explainability techniques (e.g., SHAP)  
- Integrate with real-world recommender system pipelines

---

## 📖 Citation

If you use this work, please cite:

> Performance-Driven Text Classification on MovieLens-100K Using FLAN-T5 and BART

---

## 🙌 Acknowledgements

- GroupLens Research for the MovieLens dataset  
- Hugging Face for open-source transformer models

---

## 📬 Contact

For questions or collaborations, feel free to reach out via GitHub issues or email.

Happy experimenting! 🎬✨
