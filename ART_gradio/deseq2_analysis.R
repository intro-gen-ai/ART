library(DESeq2)
library(tximport)
library(stringr)

run_deseq2 <- function(salmon_dir, metadata_path) {
  # List all quant.sf files
  files <- list.files(salmon_dir, pattern="quant.sf", full.names=TRUE, recursive=TRUE)
  names(files) <- paste0("sample", seq_along(files))
  
  # Import data using tximport
  txi <- tximport(files, type="salmon", txOut=TRUE)
  
  # Read metadata
  sampleTable <- read.csv(metadata_path, row.names=1)
  
  # Create DESeqDataSet
  dds <- DESeqDataSetFromTximport(txi, colData=sampleTable, design=~ Condition)
  
  # Run DESeq
  dds <- DESeq(dds)
  
  # Extract results
  results <- results(dds)
  
  # Split row names to extract gene symbol and gene type
  rn <- strsplit(rownames(results), "\\|")
  gene_symbol <- sapply(rn, function(x) x[length(x) - 3])
  gene_type <- sapply(rn, function(x) x[length(x)])
  
  # Identify valid rows for "protein_coding"
  valid <- grepl("protein_coding", gene_type)
  
  # Filter results and gene symbols based on valid rows
  results <- results[valid, ]
  gene_symbol <- gene_symbol[valid]
  
  # Assign filtered gene symbols as row names
  rownames(results) <- gene_symbol
  
  return(results)
}

# Call the function and write to CSV
results <- run_deseq2('salmon_results', 'metadata/metadata.csv')
write.csv(results, file = "filtered_deseq2_results.csv")

