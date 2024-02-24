import streamlit as st
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from io import StringIO

from sklearn.manifold import TSNE

def tsne_demo(data):
    st.sidebar.header("t-SNE Parameters")
    # t-SNE Parameters
    perplexity = st.sidebar.slider("Perplexity", min_value=5, max_value=50, value=30, step=1, key='perplexity')
    n_iter = st.sidebar.slider("Number of iterations", min_value=250, max_value=1000, value=1000, step=250, key='n_iter')
    learning_rate = st.sidebar.slider("Learning rate", min_value=10, max_value=200, value=200, step=10, key='learning_rate')

    if st.sidebar.button("Run t-SNE"):
        st.write("Running t-SNE...")
        tsne = TSNE(n_components=2, perplexity=perplexity, n_iter=n_iter, learning_rate=learning_rate)
        tsne_results = tsne.fit_transform(data)

        # Visualization
        fig, ax = plt.subplots()
        ax.scatter(tsne_results[:, 0], tsne_results[:, 1])
        ax.set_title('t-SNE Visualization')

        # Convert plot to SVG
        svg = StringIO()
        fig.savefig(svg, format="svg", bbox_inches="tight")
        svg.seek(0)
        svg_result = svg.getvalue()

        # Display plot
        st.pyplot(fig)

        # Download button for SVG
        st.download_button(label="Download t-SNE Visualization as SVG",
                           data=svg_result,
                           file_name="tsne_visualization.svg",
                           mime="image/svg+xml")


def pca_demo(data):
    st.sidebar.header("PCA Parameters")
    n_components = 2  # We're focusing on 2D visualization for simplicity

    if st.sidebar.button("Run PCA"):
        st.write("Running PCA...")
        pca = PCA(n_components=n_components)
        pca_results = pca.fit_transform(data)
        
        # Visualization
        fig, ax = plt.subplots()
        ax.scatter(pca_results[:, 0], pca_results[:, 1])
        ax.set_title('PCA Visualization')
        ax.set_xlabel('Principal Component 1')
        ax.set_ylabel('Principal Component 2')


        # Convert plot to SVG
        svg = StringIO()
        fig.savefig(svg, format="svg", bbox_inches="tight")
        svg.seek(0)
        svg_result = svg.getvalue()

        st.pyplot(fig)

        # Explained Variance
        st.write("Explained variance by component:", pca.explained_variance_ratio_)

        # Download button for SVG
        st.download_button(label="Download PCA Visualization as SVG",
                           data=svg_result,
                           file_name="pca_visualization.svg",
                           mime="image/svg+xml")

def load_data(uploaded_file):
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("Displaying the first few lines of the uploaded dataset:")
        st.dataframe(data.head())  # Display the first 5 lines
        return data
    else:
        st.info("Using example dataset.")
        # Generate an example dataset
        data = pd.DataFrame(np.random.randn(100, 5), columns=list('ABCDE'))
        st.write("Displaying the first few lines of the example dataset:")
        st.dataframe(data.head())  # Display the first 5 lines
        return data


def main():
    st.set_page_config(page_title="Data Visualization Tools", page_icon="🔬")

    st.markdown("# Data Visualization Tools")
    st.write(
        """This application allows you to perform dimensionality reduction on your dataset using either PCA or t-SNE and visualize the results."""
    )

    uploaded_file = st.sidebar.file_uploader("Choose a file")
    data = load_data(uploaded_file)

    # Add an option for the user to select the dimensionality reduction technique
    technique = st.sidebar.selectbox("Select technique", ["PCA", "t-SNE"])

    if technique == "PCA":
        pca_demo(data)
    elif technique == "t-SNE":
        # Assume tsne_demo function is defined elsewhere in the script
        tsne_demo(data)

if __name__ == '__main__':
    main()
