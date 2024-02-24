if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install("DESeq2")
BiocManager::install("tidyverse")
library(DESeq2)
library(ggplot2)

counts <- read.csv("./data/All_genes_expression.csv", row.names = 1)
conditions <- read.csv("./data/conditions.csv", row.names = 1)

# Ensure conditions are factors
conditions$condition <- factor(conditions$condition)

# Create a DESeq2 dataset
dds <- DESeqDataSetFromMatrix(countData = counts,
                              colData = conditions,
                              design = ~ condition)

# Run the DESeq2 pipeline
dds <- DESeq(dds)

# Extract results
res <- results(dds)

# Basic result table
res_df <- as.data.frame(res)

# Print the results table
print(head(res_df))

# Optional: Write results to CSV
write.csv(res_df, "DEA_results.csv")

# Visualization with base R (MA Plot as an example)
# Uncomment below if ggplot2 is not available
# plot(log2(res_df$baseMean + 1), res_df$log2FoldChange, 
#      col = ifelse(res_df$padj < 0.05, "red", "black"), 
#      xlab = "log2(Base Mean + 1)", ylab = "log2 Fold Change", 
#      main = "MA Plot")

# Visualization with ggplot2 (if available)
if ("ggplot2" %in% rownames(installed.packages())) {
  library(ggplot2)
  ggplot(res_df, aes(x = log2(baseMean + 1), y = log2FoldChange, color = padj < 0.05)) +
    geom_point() +
    theme_minimal() +
    scale_color_manual(values = c("FALSE" = "black", "TRUE" = "red")) +
    labs(x = "log2(Base Mean + 1)", y = "log2 Fold Change", title = "MA Plot", color = "Significant") +
    theme(legend.position = "bottom")
}

