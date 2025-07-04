A smart and user-friendly   Movie Recommendation System   that suggests   Telugu and English movies   based on user input using   TMDb API   and   machine learning similarity models  . This app provides real-time poster images and recommendations using an interactive   Streamlit   interface.
 🔥 Features

  🔍   Movie-based Recommendations   – Enter any movie name (Telugu or English) and get similar movie suggestions.
  🎞️   Real-time Poster Fetching   – Uses TMDb API to display movie posters dynamically.
  🧠   ML-based Similarity Engine   – Utilizes a precomputed similarity matrix to improve accuracy.
  🔁   Fallback Mechanism   – Smart fallback to genre-based discovery if similar results are unavailable.
  🌐   Streamlit Web App   – Clean and minimalistic UI for ease of use.
  
   🛠️ Tech Stack

    Frontend  : [Streamlit](https://streamlit.io/)
    Backend  : Python
    Machine Learning  : Cosine similarity on vectorized movie metadata
    API  : [TMDb API](https://developer.themoviedb.org/)
    Others  : Requests, Pickle, Pandas

   📂 Project Structure

```bash
.
├── app.py                Main Streamlit application
├── ml.ipynb              Notebook used for similarity matrix generation
├── movies.pkl            Pickled DataFrame of movies
├── similarity.pkl        Pickled similarity matrix
├── requirements.txt      List of required Python libraries
└── README.md             Project documentation
```

   ⚙️ Installation & Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/movie-recommendation-system.git
   cd movie-recommendation-system
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Get your TMDb API key from [TMDb](https://www.themoviedb.org/) and replace it in `app.py`:

   ```python
   API_KEY = "your_api_key_here"
   ```

4. Run the app:

   ```bash
   streamlit run app.py
   ```

   💡 How it Works

    Step 1:   User inputs a movie name.
    Step 2:   The system checks for similar movies using the similarity matrix.
    Step 3:   TMDb API is used to fetch the poster and metadata of recommended movies.
    Step 4:   If no similar Telugu movies are found, fallback to genre-based recommendations.

   🤝 Contribution

Feel free to fork the project, make changes, and create pull requests. Contributions are welcome!

   📄 License

This project is open-sourced under the MIT License.
