Zomathon: Contextual & Sequential Add-on Optimization (CSAO)

This repository contains a Smart Cart Recommendation System designed to enhance the food ordering experience by predicting high-intent add-ons based on contextual and sequential patterns.

Key Features:-

-Sequential Task Framing: Successfully solves the "Incomplete Meal Pattern" by recognizing that certain items (like Biryani) require specific sides (like Salan) for a complete experience.

-Contextual Capture: Dynamically adjusts recommendations based on Meal Time (e.g., Lunch vs. Breakfast) and User Segments.

-Hybrid Recommendation Engine: Combines Association Rules (Market Basket Analysis) with heuristic overrides for high-priority meal sequences.

-Business Impact Focused: Built-in tracking for Average Order Value (AOV) and real-time cart metrics.

Performance Metrics:- 
https://docs.google.com/spreadsheets/d/1erfFmdVdMexSAvWOKALJYvSe9UPxZSVO3lPY0NZ2lhc/edit?gid=958405087#gid=958405087

Repository Structure:

-app.py: The core Streamlit application containing the hybrid recommendation logic.

-01_data_generation.ipynb: Synthetic data pipeline for creating context-aware order histories.

-02_model_training.ipynb: ML pipeline for extracting high-lift association rules.

-rules.csv & menu_items.csv: Production data assets for the inference engine.

How to Run:

Clone the Repository: git clone https://github.com/ompandey06/ZOMATHON_CSAO.git

Install Dependencies: pip install streamlit pandas numpy

Run the Application: streamlit run app.py

Screenshot of output:

<img width="1919" height="918" alt="Screenshot 2026-03-01 164329" src="https://github.com/user-attachments/assets/8e0a125d-8733-493b-9433-a4b684fe0ca6" />


Here is the app link :
https://zomathoncsao-im5vxjrq6n7gzpng5btx65.streamlit.app/
