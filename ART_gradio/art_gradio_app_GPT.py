import gradio as gr
import os
import subprocess
import uuid
from openai import OpenAI
import openai
import pandas as pd
import zipfile
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

client = OpenAI(api_key='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')

# Set your OpenAI API key here
quant_completed = False

def generate_file_inputs(num_samples):
    """ Generate file upload inputs based on the number of samples. """
    inputs = [gr.Number(label="Number of Samples", value=4)]  # Use 'value' instead of 'default'
    for i in range(num_samples):
        inputs.append(gr.File(label=f"Sample {i+1} Forward Read (FASTQ)", type="binary"))
        inputs.append(gr.File(label=f"Sample {i+1} Reverse Read (FASTQ)", type="binary"))
    inputs.append(gr.Radio(label="Select Organism", choices=["mouse", "human"]))
    return inputs


def process_files(num_samples, *uploaded_files):
    global quant_completed
    organism = uploaded_files[-1]
    uploaded_files = uploaded_files[:-1]

    for i in range(0, len(uploaded_files), 2):
        forward_read_file = uploaded_files[i]
        reverse_read_file = uploaded_files[i + 1]
        forward_filepath = save_file(forward_read_file)
        reverse_filepath = save_file(reverse_read_file)

        # Calculate sample number
        sample_num = (i // 2) + 1
        run_salmon(forward_filepath, reverse_filepath, organism, sample_num)
    
    quant_completed = True
    return "Quantification completed for all samples."

def save_file(uploaded_file):
    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True)
    unique_id = uuid.uuid4()
    filename = f"uploaded_file_{unique_id}.fastq"
    filepath = os.path.join(uploads_dir, filename)
    with open(filepath, "wb") as f:
        f.write(uploaded_file)
    return filepath

def run_salmon(forward_read_file, reverse_read_file, organism, sample_num):
    base_output_dir = 'salmon_results'
    os.makedirs(base_output_dir, exist_ok=True)

    # Create a unique directory for each sample
    sample_output_dir = os.path.join(base_output_dir, f'sample_{sample_num}')
    os.makedirs(sample_output_dir, exist_ok=True)

    if organism == 'mouse':
        index_path = 'mouse_index'
    elif organism == 'human':
        index_path = 'human_index'

    salmon_command = f"salmon quant -i {index_path} -l A -1 {forward_read_file} -2 {reverse_read_file} -o {sample_output_dir}"
    subprocess.run(salmon_command, shell=True, check=True)

#gather metadata using NLP
def gather_metadata(user_input, history=[]):
    global num_samples  # Make num_samples a global variable if it's used across multiple function calls
    history.append({"role": "user", "content": user_input})

    if len(history) == 1:  # First user input (number of samples)
        num_samples = int(user_input)  # Convert to integer and assign to num_samples
        next_question = f"What is the condition for Sample 1?"
    elif len(history) <= 2 * num_samples:  # Subsequent inputs for each sample
        next_sample_number = len(history) // 2 + 1
        if next_sample_number > num_samples:
            return format_metadata(history, num_samples), []
        next_question = f"What is the condition for Sample {next_sample_number}?"
    else:  # All data collected
        return format_metadata(history, num_samples), []

    history.append({"role": "assistant", "content": next_question})

    return next_question, history


#format metadata into a csv file
def format_metadata(history, num_samples):
    metadata_content = "Sample,Condition\n"
    for i in range(1, num_samples + 1):
        condition = history[2 * i]["content"]
        metadata_content += f"sample{i},{condition}\n"

    # Define the path for the metadata file
    metadata_folder = "metadata"
    os.makedirs(metadata_folder, exist_ok=True)
    metadata_file_path = os.path.join(metadata_folder, "metadata.csv")

    # Save the metadata content to a CSV file
    with open(metadata_file_path, "w") as file:
        file.write(metadata_content)

    # Return a message indicating that the metadata file is ready
    return "Metadata file created and saved as 'metadata.csv'. You can now proceed with DESeq2 analysis.", []

def run_analysis_and_generate_volcano_plot(_=None):
    try:
        # Run DESeq2 analysis
        subprocess.run(["Rscript", "deseq2_analysis.R"], check=True)

        # Assuming the R script outputs a results file suitable for a volcano plot
        results_file = "filtered_deseq2_results.csv"

        # Generate and save the volcano plot
        results_df = pd.read_csv(results_file)
        results_df['-log10(pvalue)'] = -np.log10(results_df['pvalue'])
        significant = (results_df['padj'] < 0.05) & (abs(results_df['log2FoldChange']) > 1)

        # Identifying top 5 significant genes based on lowest adjusted p-values
        top_genes = results_df[significant].nsmallest(10, 'padj')

        plt.figure(figsize=(10, 6))
        plt.scatter(results_df['log2FoldChange'], results_df['-log10(pvalue)'],
                    color='grey', alpha=0.7, label='Non-significant')
        plt.scatter(results_df['log2FoldChange'][significant], 
                    results_df['-log10(pvalue)'][significant], 
                    color='red', alpha=0.7, label='Significant')

        # Annotating top genes
        for idx, row in top_genes.iterrows():
            gene_name = row[0]
            plt.text(row['log2FoldChange'], row['-log10(pvalue)'], gene_name, fontsize=9)

        plt.title('Volcano Plot of RNA-Seq Data')
        plt.xlabel('Log2 Fold Change')
        plt.ylabel('-Log10(p-value)')
        plt.legend()

        plot_file_path = 'volcano_plot.png'
        plt.savefig(plot_file_path)
        plt.close()

        chat_response, _ = chatbot_response('metadata/metadata.csv', [])

        return plot_file_path, chat_response

    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}"

# converts metadata csv file to string
def csv_to_string(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    # Convert DataFrame to a string
    csv_string = df.to_string(index=False)
    return csv_string

#gives suggestions based on the metadata
def chatbot_response(file_path, history):
    # Convert CSV to string
    metadata = csv_to_string(file_path)

    # Add system and user messages to history
    history.append({"role": "system", "content": "You are a helpful assistant analyzing RNA sequencing metadata."})
    history.append({"role": "user", "content": f"Here is some RNA sequencing metadata: {metadata}. Please analyze it and provide any warnings about the validity of the data and suggestions for further visualization."})

    # Get response from OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=history
    )

    # Extract assistant message
    assistant_message = response.choices[0].message.content
    history.append({"role": "assistant", "content": assistant_message})

    return assistant_message, history

    
#file processing interface
iface1 = gr.Interface(
    fn=process_files,
    inputs=generate_file_inputs(4),  # Default to 2 samples
    outputs="text",
    title="ART - Automated RNA-sequencing Tool",
    description="Specify the number of samples and upload your paired-end FASTQ files.",
    article="""<p>Welcome to ART, an automated tool for RNA sequencing analysis. Start by specifying the number of samples. The default is set to 4, but you can adjust this number as needed.</p>
               <p>Next, upload the corresponding paired-end FASTQ files for each sample. There's a separate upload field for the forward and reverse reads of each sample.</p>
               <p>Finally, select the organism for your analysis - either mouse or human. After uploading all files and making your selection, click 'Submit' to start the RNA quantification process using Salmon.</p>""",
    api_name="process_files_api"
)

# Metadata creation interface
metadata_interface = gr.Interface(
    fn=gather_metadata,
    inputs=gr.Textbox(label="Enter Metadata"),  # Custom label for the input
    outputs=[
        gr.Textbox(label="Next Instruction"),  # Custom label for the output (instruction)
        gr.Textbox(label="Metadata History", visible=False)  # Custom label for the history (optional)
    ],
    title="Metadata Creation",
    description="Input the metadata for your samples.",
    article="""<p>Enter the metadata for each of your samples here. Start by inputting the total number of samples. Subsequently, you'll be prompted to enter specific conditions for each sample, such as 'treated' or 'untreated'. This information is crucial for accurately formatting your metadata for downstream analysis.</p>""",
    api_name="metadata_creation_api"
)



# Analysis creation interface
analysis_interface = gr.Interface(
    fn=run_analysis_and_generate_volcano_plot,
    inputs=gr.Button(),
    outputs=[gr.Image(type="filepath", label="Volcano Plot"),
             gr.Textbox(label="AI Insights")],  # Adding chatbot response as second output
    title="RNA-Seq Analysis and Visualization",
    description="Generate a volcano plot and get AI-driven insights from metadata.",
    article="""<p>This interface initiates the RNA-seq data analysis. By clicking the 'Run Analysis' button, you will start the statistical processing using DESeq2, a method for differential expression analysis.</p>
               <p>Once the analysis is complete, a volcano plot will be generated. This plot visualizes significant genes and their expression changes. Genes of particular interest, based on statistical criteria, will be highlighted.</p>"""
)

#AI suggestions interface
chat_interface = gr.ChatInterface(
    fn=chatbot_response,
    title="RNA Sequencing Analysis Assistant",
    description="Enter your RNA sequencing metadata, and get AI-driven insights, warnings, and visualization suggestions."
)

#integrate the interfaces
tabbed_interface = gr.TabbedInterface(
    [iface1, metadata_interface, analysis_interface, chat_interface],
    ["File Processing", "Metadata Creation", "Analysis"]
)

if __name__ == "__main__":
    tabbed_interface.launch(server_name="127.0.0.1")


