# ART - Automated RNA-sequencing Tool
ART is a biostatistics tool that automates the RNA-sequencing pipeline, allowing a researcher with minimal experience in data science, coding, and biostatistics to analyze and visualize bulk RNA-sequencing data. 

## Usage of AI Assistant

### Link to video explanation:

### Instructions for running ART
#### *Setting Up and Running the ART_gradio Application Locally*

##### Prerequisites

Before you begin, ensure the following are installed on your machine:

- Python
- R

##### Step 1: Install the ART_gradio Folder

1. Download the `ART_gradio` folder onto your device.

##### Step 2: Download Required Index Files

1. In the `ART_gradio` folder, find the file named `index_files`.
2. This file contains links to `mouse_index` and `human_index` folders.
3. Download these folders and add them to the `ART_gradio` directory.

##### Step 3: Install R and Required Packages

1. Install R on your machine, if not already installed.
2. Install the necessary R packages with the following commands in R:

    ```r
    install.packages("BiocManager")
    BiocManager::install("DESeq2")
    BiocManager::install("tximport")
    install.packages("stringr")
    ```

##### Step 4: Install and Set Up Salmon for Quantification

1. Install Bioconda on your device.
2. For new MacBooks with Apple Silicon:

    - Activate the 'rosetta' environment using:

        ```bash
        conda activate rosetta
        ```

    - Then, install Salmon with the command:

        ```bash
        conda install salmon
        ```

    - For other systems, install Salmon directly without the 'rosetta' activation.

##### Step 5: Access Sample Data

1. Visit the ART GitHub repository.
2. Download the `sampleData` file for sample runs.

###### Step 6: Run the Python Script and Launch the Web Application

1. Navigate to the `ART_gradio` folder in your command line interface.
2. Run the Python script to start the application (e.g., `python run_app.py`).
3. The web application will be accessible once the script is running successfully.

###### Additional Notes

- Ensure you are in the correct environment before running the Python script, especially on Apple Silicon MacBooks.
- If you encounter any issues, refer to the application's documentation or troubleshooting guide for assistance.

## Project PI/Project Team 
Gian Luca Lupica-Tondo, gian.luca.lupica-tondo@vanderbilt.edu, lupicag, PI

## Project Proposal 

### Description of Problem/Opportunity
RNA sequencing is a sequencing technique used ubiquitously in biomedical research today. It allows researchers to determine the number of RNA, protein-coding transcripts that exist inside a cell. This provides researchers with an intracellular view of how perturbations in biological systems can affect cellular function and behavior. 

While the bench-side technique is relatively simple, the analysis of the data is tedious and often requires outsourcing the raw sequencing (.FASTQ) files to a biostatistician. This creates a disconnect between the researcher and data scientist: neither is able to fully articulate their needs to the other and information is lost in the process. The biologist is often at the whim of whatever the biostatistician produces, leaving many questions unanswered. 

### Proposed Solution/Approach
The Automated RNA-sequencing Tool (ART) is designed to bridge the gap between biologists and data scientists, enabling those with minimal experience in data science and biostatistics to efficiently process, analyze, and visualize bulk RNA-sequencing data. The key components of the solution include:

**User-Friendly Interface:** A graphical interface that allows users to upload raw sequencing (.FASTQ) files and choose the desired analyses without having to write any code.

**Automated Data Processing:** ART will be equipped with pre-configured pipelines to process raw data, perform quality control, and map reads to a reference genome.

**Integrated Analysis Modules:** Users can select from a range of analyses, including differential expression, pathway analysis, and gene ontology, among others.

**Visualization Suite:** ART will offer a suite of visualization tools that enable users to generate plots and graphs from their data, aiding in easier interpretation and presentation.

**Collaboration and Reporting:** Users can generate comprehensive reports of their analyses and share them with collaborators or publish them in journals.

### Project Outline and Timeline

**Interface Design and Development (Oct 27 - Nov 6):** Develop the initial version of the graphical interface for ART.

**Integration of Data Processing Pipelines (Nov 7 - Nov 14):** Integrate the RNA-seq processing tools and pipelines.

**Incorporation of Analysis Modules (Nov 15 - Nov 22):** Add the various analysis modules to ART.

**Development of Visualization Suite (Nov 23 - Nov 30):** Create visualization tools and integrate them into ART.

**Testing and Feedback (Dec 1 - Dec 4):** Test the software with a group of users and gather feedback.

**Refinement and Finalization (Dec 5 - Dec 8):** Address feedback, fix bugs, and finalize the software for launch.

## Goals of project 

### Goal 1 
Enable researchers to analyze RNA-sequencing data without needing specialized knowledge in biostatistics or programming, thereby reducing the reliance on external biostatisticians.
### Goal 2
Facilitate a comprehensive analysis of RNA-sequencing data, from raw data processing to in-depth analysis and visualization, all within a single integrated platform.
### Goal 3
Promote better communication and understanding between biologists and data scientists by offering transparent and understandable analytical methods and results.
### Goal 4
Reduce the time and costs associated with RNA-seq data analysis by providing an automated and efficient solution.

## Project Metrics 

### Metric 1
Time Efficiency: Measure the time it takes for ART to process and visualize a standard RNA-sequencing dataset and compare it to the average time taken by a biostatistician. The tool should reduce the analysis time by at least 50%.   
  A: Reduces analysis time by 60% or more compared to a biostatistician.  
  B: Reduces analysis time by 50-59% compared to a biostatistician.  
  C: Reduces analysis time by 40-49% compared to a biostatistician.  
  D: Reduces analysis time by 30-39% compared to a biostatistician.  
  F: Reduces analysis time by less than 30% or does not reduce time at all.  

### Metric 2
Accuracy: Compare the results generated by ART with those produced by a validated test dataset. The results should have a concordance rate of at least 90%.   
  A: Concordance rate of 90% or higher   
  B: Concordance rate of 80-89%   
  C: Concordance rate of 70-79%    
  D: Concordance rate of 60-69%   
  F: Concordance rate of less than 60%   
  
## Self-Evaluation

### Discussion of Goals 
The first goal of this project was to create a tool that would allow researchers to perform RNA sequencing analysis without knowing how to run the analysis themselves, from a technical standpoint. I firmly believe that ART has met this goal. I show that ART can take raw FASTQ/A RNA sequencing files and can output a common visualization utilized in RNA-seq workflow without the need for any technical knowledge from the user. 

The second goal was also met. The entirety of the analysis is performed on a website hosted by Gradio; the user does not need to use any other platform. The tabbed interface on my website takes the user through the steps of the analysis without having to manually run a terminal or R script.

The third goal was met in part by the integration of OpenAI's GPT-3.5 LLM into my Gradio website. After visualization is performed, the metadata file is uploaded to GPT-3.5, and the LLM outputs suggestions and warnings about the sample size and dataset. This proof-of-concept paves the way for the integration of a "Biostatistican AI Assistant" that would help facilitate future interactions with researchers and those knowledgeable in data analysis. 

In its current state, ART can automate and produce visualization for four samples in roughly ten minutes. This is mostly due to it running on my local machine. However, if we assume that the average RNA sequencing analysis may take weeks to complete after soliciting the help of a biostatistician, I believe that this goal was met. Regardless of time, having an early visualization of the data allows researchers to better guide a biostatistician's analysis, reducing the number of times that the analysis needs to be performed. 

### Discussion of Metrics
The first metric was certainly achieved. An RNA-sequencing analysis with ART takes about 10 minutes for every four samples. Assuming a standard sample size of 20 for an RNA-sequencing experiment, this would take about 50-60 minutes. Furthermore, if this were hosted on a computing cluster the processing time would significantly decrease. From my experience, handing off the raw data to a biostatistician results in the project being placed in a queue that roughly takes one week to complete. For this reason, I award ART with an **A** in the first metric.

The second metric is a little more difficult to assess. Frankly, creating a robust RNA sequencing pipeline that matches the rigor of a biostatistician with an advanced knowledge of computer science, statistics, and bioinformatics would be a multi-year project, perhaps even a PhD thesis. Furthermore, ART is limited by running on a local machine, restricting its computing power and decreasing its ability to analyze a large sample size at once. However, The Volcano Plot visualization produced by ART is characteristic of what would be produced by a biostatistician and provides much insight for the researcher. Thus, I would give ART a **C** for its ability to match that of a biostatistician. 

## Reflection on Learning
Reflecting on the development of the Automated RNA-sequencing Tool (ART), it's clear that this project has been a significant learning experience, particularly in harnessing the capabilities of advanced AI tools like OpenAI's GPT-4. This journey has not only expanded my technical skills but has also reshaped my perspective on the potential of AI in research and development, especially in fields that require complex data processing and visualization, like bioinformatics.

### Enhanced Capabilities as a Creator and Researcher

Utilizing GPT-4 in the creation of ART has been instrumental in broadening my scope as both a creator and a researcher. Before this project, the idea of constructing a comprehensive tool for RNA sequencing analysis seemed impossible, requiring extensive manual coding and a deep understanding of various programming languages and bioinformatics. However, with the assistance of GPT-4, I was able to navigate through these complexities more efficiently. The AI's ability to provide coding guidance and streamline complex processes allowed me to focus more on the application's design and user experience rather than getting bogged down in intricate coding details.

The most significant takeaway from this project is the realization of how AI can be a powerful ally in research. By automating subprocesses like Salmon and integrating an R script for data analysis, ART has made it possible to visualize RNA sequencing results quickly and efficiently. This rapid visualization capability is crucial in bioinformatics, where interpreting vast datasets accurately and expediently can lead to more meaningful research outcomes.

### Product in Beta: A Work in Progress

It's important to note that ART is still very much in its beta phase. This means that while it has shown great potential in streamlining RNA sequencing analysis, there is room for further refinement and development. The current state of ART is a solid foundation, but it's also a starting point for future enhancements. One of the key areas for development is the integration of natural language processing (NLP) to provide more customizable and user-friendly visualizations. This addition could significantly improve the tool's accessibility and utility, making it a more robust research resource. Ideally, the entire process will be integrated with a Large-Language Model and the user will only have to upload files. 

### Future Learning and Application

This project has underscored the importance of staying adaptable and continually learning, especially in fields intersecting with AI. The landscape of AI and machine learning is rapidly evolving, and keeping up with these changes is crucial for leveraging these technologies most effectively.

I plan to build upon the knowledge and experience gained from developing ART in future endeavors. The project has opened up new possibilities in creating tools that are not only functional but also user-centric. The goal is to continue exploring ways in which AI can simplify complex tasks, making advanced research tools more accessible to a broader range of users.

In conclusion, the development of ART has been a valuable exercise in understanding and applying AI in a practical, research-oriented context. It has expanded my capabilities as a researcher and developer, offering insights into the transformative potential of AI in scientific research and tool development. As ART continues to evolve, it stands as a testament to the power of AI in pushing the boundaries of what we can achieve in data analysis and visualization.

## What's Next?
Continuing the development of the Automated RNA-sequencing Tool (ART) is certainly on the horizon, albeit with the understanding that time constraints may slow the pace of progress. The journey thus far has been enriching, and the insights gained will be pivotal in guiding the next steps of the project. I'd like to try to have an LLM such as OpenAI take the results file and produce its visualizations based on the user's suggestions and the model's knowledge of statistics. 

### Expanding Infrastructure

The immediate focus for ART's evolution involves a shift in infrastructure. The current setup, which relies on my personal computer's processing power and storage, is functional but limited in scale. To address this, the plan is to migrate the application to a server-based environment. This transition will not only alleviate the storage burden from my local machine but also set the stage for handling a larger volume of files more efficiently. Such a move is critical for scaling up the application, making it more robust and capable of catering to higher demands.

### Enhancing Processing Power

Another key aspect of the project's next phase is to enhance its processing capabilities. Currently, ART performs RNA sequencing analysis using Salmon, executed on a local machine. The goal is to run Salmon on a computing cluster, significantly boosting processing power. This upgrade will be a game-changer, allowing for the processing of hundreds of files swiftly, which is a substantial step up from the current capacity (4 samples, 8 files). Such an enhancement is crucial for making ART a more powerful and efficient tool for RNA sequencing analysis.

### Integrating Advanced AI Features

Looking further ahead, integrating OpenAI's API, particularly the OpenAI Assistants tool, is a promising avenue. This integration would offer users the ability to guide and customize visualizations according to their specific needs. Moreover, leveraging AI to explain results can greatly enhance the user experience, making the tool not only a processing powerhouse but also an intelligent assistant in data interpretation. This kind of user-centric approach could revolutionize how researchers interact with bioinformatics tools, offering a more intuitive and interactive experience.

### Conclusion

In summary, the path forward for ART is marked by significant upgrades both in infrastructure and capabilities. The next phases of development aim to transform ART into a more powerful, scalable, and user-friendly tool, harnessing the latest advancements in AI and cloud computing. This continued journey promises not only to enhance my skills and knowledge but also to contribute a valuable tool to the field of bioinformatics.
