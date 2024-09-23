#In this program we will save the links of the images from wikimedia commons

#En este programa se descargan los paths de las imagenes de wikimedia commons

#____________General libraries______________________________
import os
import spacy 
import numpy as np
from transformers import pipeline
import requests
import argparse

#_____________libraries for wikibot_________________________________
import json
import pywikibot
from pywikibot import pagegenerators
from pathlib import Path
from wikibot import * #importamos todas las funciones del wikibot
import urllib
import PIL.Image 


#___________________Libraries for the progress bar_____________________
import time
from progressbar import ProgressBar


# ___________Accesssing images from the web or the files___________

#Headers for wikimedia

headers = {
  'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI1ZGNmOWIxYTBlNDFmZTE3ZjYxMjYwMTY3NDM2ZmNjYSIsImp0aSI6ImZmMDVkYjIxOWFlMTJhNWRiOWY0ZTU4NTFlNWI3NTEzY2QwM2JhYTkyM2NmZjNkZTdjMWJlYTc4YTUzODg2ZGFkMWZjNjY5Y2EyZGY4Yjc4IiwiaWF0IjoxNzEzODE1Mjk4LjIyNzIwMiwibmJmIjoxNzEzODE1Mjk4LjIyNzIwNSwiZXhwIjozMzI3MDcyNDA5OC4yMjU1OSwic3ViIjoiNzUyMjAwOTQiLCJpc3MiOiJodHRwczovL21ldGEud2lraW1lZGlhLm9yZyIsInJhdGVsaW1pdCI6eyJyZXF1ZXN0c19wZXJfdW5pdCI6NTAwMCwidW5pdCI6IkhPVVIifSwic2NvcGVzIjpbImJhc2ljIiwiY3JlYXRlZWRpdG1vdmVwYWdlIl19.klqz-hpRMnLhqORQAOY7QNxash20FAM9wX3IxsV7_QtLRBLx83VUIb_22oJG9_w-gi0A_cQ9fw8GCKp4Hfp0Z7fJsT9ragbs2bJp6o9ztowx4BrN32QhPEXAU9C-pjC6WsbpnFUzKRnZwz3_Kj4NxCXVQMsB6kKhyjTX-KutdoAE7YVvl-g13AviUhFjitNMVW7KZIJkK9hd1N2GI5gtc75gkjvDSRjr1pTubJXl8lzqWfpi9IjovoujhKe_0N8_i0dOlwLoRhcNaWoTJ22O7o4Fcku4aWFgnlLJF7Q0ZjVsHiCr9h1_OX7xlduApuj0m6qaCokU2PEwKdgfEKHRm1V9mjY7ANl3BJrT9JDMo_BvJiKkuhheyJY6RENEqLwvWinfW87aWPdp-9kn07i6o-vytLnEC093YdwYARdvZhftUHgdsmE0LsMWBWoKIUcux8FXcRtgTKCZ3AHNJ2ik3Gu5vQWzl4jKd6cKuAOp-jvgLkuUUR-ateSFrmx9gyPhjWVPkl4jSekGqRHYJE3no8yAbk4v5yYjRvfWbvYKKLtmQ4GuLMhLxfJX6WOfnzzDHpq2LXKjUpIMhdFxcpebVEKtY7mPfoeZCvYSkMZQB10Kbk4XiWUPUJ125xKr4A3r4Ai8Nxyk-DbJzxjo-POfUSMm9UO_2WLWCIYbCrEahwo',
  'User-Agent': 'MithozZfg'
}



import urllib.parse as parse
import os
# Verify url
def check_url(string):
    try:
        result = parse.urlparse(string)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False


# Load an image
def load_image(image_path):
    if check_url(image_path):
        respuesta = requests.get(image_path, headers=headers, stream=True)#.raw
        return PIL.Image.open(requests.get(image_path, headers=headers, stream=True).raw)
    elif os.path.exists(image_path):
        return PIL.Image.open(image_path)
    

CATEGORY = [ 'Mathematics', 'Philosophy', 'Literature and Art', 'Communication', 'Politics',
            'Law', 'Economics', 'Business', 'Culture', 'Society']

SUBCATEGORY = [["Mathematics", "Algebra", "Calculus", "Geometry", "Statistics", "Probability", "Differential Equations", "Linear Algebra", "Number Theory", "Topology",
"Combinatorics", "Mathematical Logic", "Set Theory", "Complex Numbers", "Real Numbers", "Functions", "Graph Theory", "Discrete Mathematics", "Mathematical Analysis", "Abstract Algebra",
"Statistics", "Probability Theory", "Integral Calculus", "Differential Calculus", "Vectors", "Matrices", "Eigenvalues", "Eigenvectors", "Matrix Theory", "Optimization",
"Numerical Methods", "Mathematical Modeling", "Cryptography", "Operations Research", "Chaos Theory", "Fractals", "Geometry", "Trigonometry", "Arithmetic", "Calculus of Variations",
"Fourier Transform", "Laplace Transform", "Partial Differential Equations", "Functional Analysis", "Game Theory", "Operations Research", "Symbolic Computation", "Boolean Algebra", "Proof Theory", "Number Systems"]


,["Philosophy", "Metaphysics", "Epistemology", "Ethics", "Logic", "Ontology", "Aesthetics", "Philosophy of Mind", "Existentialism",
"Rationalism", "Empiricism", "Utilitarianism", "Deontology", "Virtue Ethics", "Pragmatism", "Determinism", "Free Will", "Nihilism", "Absurdism",
"Stoicism", "Skepticism", "Idealism", "Materialism", "Dualism", "Monism", "Dialectic", "Hermeneutics", "Postmodernism", "Critical Theory",
"Political Philosophy", "Social Philosophy", "Philosophy of Science", "Philosophy of Religion", "Logic", "Critical Thinking", "Reasoning", "Ethical Theory", "Moral Philosophy", "Philosophy of Language",
"Philosophy of History", "Metaphysical Realism", "Nominalism", "Realism", "Relativism", "Objectivism", "Subjectivism", "Theory of Knowledge", "Analytic Philosophy", "Continental Philosophy"]

,["Literature", "Art", "Novel", "Poetry", "Drama", "Prose", "Fiction", "Non-Fiction", "Short Story", "Play",
"Essay", "Literary Criticism", "Narrative", "Theme", "Symbolism", "Metaphor", "Character", "Plot", "Setting", "Genre",
"Artistic Expression", "Painting", "Sculpture", "Drawing", "Printmaking", "Photography", "Installation Art", "Performance Art", "Abstract Art", "Realism",
"Impressionism", "Expressionism", "Cubism", "Surrealism", "Modernism", "Postmodernism", "Renaissance", "Baroque", "Gothic", "Romanticism",
"Literary Device", "Poetic Form", "Dialogue", "Allusion", "Imagery", "Art Criticism", "Art History", "Cultural Heritage", "Visual Arts", "Literary Genre",
"Artistic Movement", "Aesthetic", "Narrator", "Literary Theory", "Artistic Technique", "Canvas", "Muse", "Art Gallery", "Literary Canon", "Craftsmanship"]


,["Communication", "Verbal Communication", "Nonverbal Communication", "Interpersonal Communication", "Mass Communication", "Digital Communication", "Public Speaking", "Listening", "Writing", "Reading",
"Media", "Social Media", "Broadcasting", "Journalism", "Public Relations", "Marketing", "Advertising", "Persuasion", "Message", "Feedback",
"Communication Theory", "Body Language", "Tone", "Context", "Medium", "Channel", "Signal", "Encoding", "Decoding", "Information",
"Speech", "Conversation", "Dialogue", "Negotiation", "Conflict Resolution", "Cultural Communication", "Cross-Cultural Communication", "Intercultural Communication", "Nonverbal Cues", "Facial Expression",
"Gestures", "Communication Skills", "Communication Barriers", "Effective Communication", "Information Technology", "Media Literacy", "Telecommunication", "Virtual Communication", "Network", "Language"
]


,["Politics", "Government", "Democracy", "Republic", "Monarchy", "Dictatorship", "Political Party", "Election", "Legislation", "Policy",
"Constitution", "Parliament", "Congress", "Senate", "Executive", "Judiciary", "Bureaucracy", "Public Administration", "Campaign", "Voting",
"Political Ideology", "Liberalism", "Conservatism", "Socialism", "Communism", "Fascism", "Nationalism", "Populism", "Anarchism", "Totalitarianism",
"Federalism", "State", "Nation", "Diplomacy", "International Relations", "Political Theory", "Political Philosophy", "Civil Rights", "Human Rights", "Social Justice",
"Political Economy", "Corruption", "Lobbying", "Public Policy", "Governance", "Political Science", "Representation", "Sovereignty", "Power", "Constituency"
]


,["Legal Precedent", "Courtroom", "Plea Bargain", "Indictment", "Subpoena", "Affidavit", "Deposition", "Discovery", "Injunction", "Habeas Corpus",
"Plaintiff", "Defendant", "Counsel", "Cross-Examination", "Settlement", "Verdict", "Sentence", "Parole", "Probation", "Alibi",
"Acquittal", "Guilty", "Not Guilty", "Bail", "Custody", "Warrant", "Search Warrant", "Arrest", "Prosecution", "Defense Attorney",
"Public Defender", "Civil Rights", "Human Rights", "Legal Code", "Ordinance", "Statutory Interpretation", "Jurisprudence", "Legal Counsel", "Barrister", "Solicitor",
"Amicus Curiae", "Brief", "Legal Aid", "Case Law", "Administrative Law", "Appellate Court", "Small Claims Court", "Legal Reform", "Criminal Justice", "Forensic Evidence"
]


,["Economics", "Supply and Demand", "Market", "Inflation", "Deflation", "Gross Domestic Product (GDP)", "Unemployment", "Interest Rate", "Monetary Policy", "Fiscal Policy",
"Capitalism", "Socialism", "Free Market", "Trade", "Tariff", "Subsidy", "Exchange Rate", "Budget", "Deficit", "Surplus",
"Recession", "Depression", "Economic Growth", "Development", "Income", "Wealth", "Poverty", "Inequality", "Labor Market", "Productivity",
"Investment", "Stock Market", "Bond", "Currency", "Foreign Exchange", "Balance of Payments", "Economic Indicators", "Consumer Price Index (CPI)", "Purchasing Power", "Economic Theory",
"Microeconomics", "Macroeconomics", "Public Finance", "International Trade", "Supply Chain", "Competition", "Market Structure", "Oligopoly", "Monopoly", "Econometrics"
]


,["Business", "Entrepreneurship", "Start-up", "Corporation", "Partnership", "Sole Proprietorship", "Business Plan", "Revenue", "Profit", "Loss",
"Marketing", "Branding", "Sales", "Customer Service", "Product Development", "Supply Chain", "Inventory Management", "E-commerce", "Retail", "Wholesale",
"Finance", "Investment", "Accounting", "Budgeting", "Cash Flow", "Profit Margin", "Market Research", "Business Strategy", "Human Resources", "Management",
"Leadership", "Organizational Behavior", "Corporate Culture", "Business Ethics", "Corporate Social Responsibility", "Stakeholders", "Shareholders", "Merger", "Acquisition", "Innovation",
"Risk Management", "Operations Management", "Quality Control", "Logistics", "Distribution", "Outsourcing", "Globalization", "Business Law", "Contract", "Negotiation"
]


,["Culture", "Tradition", "Custom", "Heritage", "Values", "Beliefs", "Ritual", "Language", "Art", "Music",
"Dance", "Literature", "Cuisine", "Festivals", "Religion", "Folklore", "Norms", "Social Practices", "Identity", "Ethnicity",
"Traditions", "Cultural Diversity", "Cultural Exchange", "Cultural Heritage", "Artistry", "Craftsmanship", "Symbolism", "Mythology", "Ceremony", "Belief Systems",
"Customs", "Heritage Sites", "Cultural Anthropology", "Cultural Preservation", "Cultural Evolution", "Cultural Adaptation", "Social Norms", "Cultural Values", "Cultural Identity", "Cultural Expression",
"Traditions", "Rituals", "Art Forms", "Social Structure", "Cultural Artifacts", "Music Genres", "Dance Styles", "Cultural Practices", "Storytelling", "Myth"
]


,["Society", "Community", "Social Structure", "Social Norms", "Social Institutions", "Social Interaction", "Social Groups", "Culture", "Social Change", "Social Stratification",
"Social Class", "Inequality", "Demographics", "Population", "Cohesion", "Social Dynamics", "Social Networks", "Social Roles", "Status", "Socialization",
"Family", "Education", "Religion", "Government", "Economy", "Healthcare", "Law", "Public Policy", "Social Services", "Media",
"Social Problems", "Crime", "Homelessness", "Poverty", "Discrimination", "Civil Rights", "Human Rights", "Citizenship", "Identity", "Community Engagement",
"Urbanization", "Rural Areas", "Migration", "Social Movements", "Activism", "Social Welfare", "Social Justice", "Social Capital", "Collective Action", "Social Integration"
]]


ITERATIONS = 200





if __name__=='__main__':

    dict_categ_weights = {}

    for i, categ in enumerate(CATEGORY):
        #Se crea la carpeta de la Categoria de las imagenes
        download_path = "/media/mitos/nuevo ssd/BASE DE DATOS LINKS/" + categ
        Path(download_path).mkdir(parents=True, exist_ok=True)  
        contador_total = 0 #contador de todas las imagenes encontradas

        for subcat in SUBCATEGORY[i]:
                
            site = pywikibot.Site("commons", "commons")
            cat = pywikibot.Category(site, subcat)
            gen = pagegenerators.CategorizedPageGenerator(cat, recurse=True)
            contador1 = 0
            contador2 = 0
            
            filepaths = []

            
            print("START\n")
            #Barra para ir observando el progreso qeu lleva el programa

            barra = ProgressBar(maxval=ITERATIONS).start()  # Inicializar la barra de progreso

            #________________________________________________________________________________
            #________________________________________________________________________________
            #_____aqui se buscarán las imagenes de cada categoría__________
            #________________________________________________________________________________

            for indice, page in enumerate(gen):
                
                if check_format(page.title()):
                    #contador para imagenes con formato correcto y encontradas
                    contador1 = contador1 + 1
                    #En esta parte se obtienen los links de las imagenes
                    try:
                        filepath = page.get_file_url()
                    except:
                        contador2 = contador2 + 1
                        continue
                    
                    #aqui se crea la lista de filepaths
                    filepaths.append(filepath)
                else: 
                    contador2 = contador2 + 1 #contador para formato incorrecto
                

                barra.update(indice) #increment the counter
                if indice>=ITERATIONS:
                    break

            #Aqui se guardan los links encontrados    
            path = download_path + f'/{subcat}.json'
            
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(filepaths, file, ensure_ascii=False, indent=4)

            barra.finish()
            print('\n')
            print(f'Imagenes de la categoria {subcat}')
            print("Imagenes con formato correcto: {}".format(contador1))
            print("Imagenes con formato incorrecto: {}".format(contador2))
            contador_total = contador_total + contador1
        
        print('\n')
        print(f'Imagenes totales encontradas de la categoria {categ}: {contador_total}')
        dict_categ_weights[categ] = contador_total
    
    with open('dict_categ_weights.json', 'w') as file:
        json.dump(dict_categ_weights, file, indent=4)





"""Animals = ["Cats", "Dogs", "Elephants", "Tigers", "Lions", "Bears", "Dolphins", "Whales", "Sharks", "Penguins",
"Kangaroos", "Giraffes", "Pandas", "Zebras", "Wolves", "Foxes", "Deer", "Rabbits", "Squirrels", "Horses",
"Cows", "Sheep", "Goats", "Chickens", "Ducks", "Geese", "Eagles", "Hawks", "Owls", "Parrots",
"Flamingos", "Peacocks", "Turtles", "Crocodiles", "Alligators", "Frogs", "Toads", "Lizards", "Snakes", "Bats",
"Bees", "Butterflies", "Ants", "Spiders", "Crabs", "Lobsters", "Octopuses", "Squids", "Seals", "Otters"]

3901



Astronomy = ["Galaxy", "Nebula", "Star", "Planet", "Asteroid", "Comet", "Meteor", "Black Hole", "Supernova", "Quasar",
"Satellite", "Orbit", "Telescope", "Astronomer", "Constellation", "Light Year", "Exoplanet", "Pulsar", "Red Giant", "White Dwarf",
"Solar System", "Milky Way", "Universe", "Gravity", "Dark Matter", "Dark Energy", "Big Bang", "Cosmos", "Hubble", "Spacecraft",
"Rover", "Mars", "Venus", "Jupiter", "Saturn", "Uranus", "Neptune", "Mercury", "Sunspot", "Solar Flare",
"Aurora", "Eclipse", "Equinox", "Solstice", "Orbit", "Astrobiology", "Space Station", "Rocket", "Astronaut", "Cosmology"]

800

Eviroment Science= ["Geoscience", "Environmental Science", "Erosion", "Sedimentation", "Weathering", "Fossil", "Mineral", "Rock", "Soil", "Plate Tectonics",
"Volcano", "Earthquake", "Tsunami", "Landslide", "Fault Line", "Seismic Wave", "Richter Scale", "Crust", "Mantle", "Core",
"Magma", "Lava", "Glacier", "Iceberg", "Atmosphere", "Climate", "Weather", "Biodiversity", "Ecosystem", "Conservation",
"Pollution", "Deforestation", "Ozone Layer", "Greenhouse Effect", "Carbon Footprint", "Renewable Energy", "Fossil Fuel", "Sustainability", "Recycling", "Water Cycle",
"Hydrology", "Oceanography", "Meteorology", "Geology", "Geomorphology", "Biogeochemistry", "Ecology", "Soil Science", "Natural Resources", "Environmental Impact"]

3016

Biology" y "Life Sciences = ["Biology", "Life Sciences", "Cell", "DNA", "Gene", "Chromosome", "Protein", "Enzyme", "Mitosis", "Meiosis",
"Photosynthesis", "Respiration", "Evolution", "Natural Selection", "Genetics", "Ecology", "Ecosystem", "Biodiversity", "Species", "Habitat",
"Organism", "Population", "Biome", "Adaptation", "Mutation", "Microbiology", "Zoology", "Botany", "Anatomy", "Physiology",
"Immunology", "Neuroscience", "Endocrinology", "Genomics", "Proteomics", "Biotechnology", "Cloning", "Stem Cells", "Embryology", "Virology",
"Bacteriology", "Ecotoxicology", "Parasitology", "Taxonomy", "Evolutionary Biology", "Molecular Biology", "Biochemistry", "Cytology", "Ethology", "Symbiosis"]

3184

Physics = ["Physics", "Quantum Mechanics", "Relativity", "Force", "Energy", "Momentum", "Velocity", "Acceleration", "Gravity", "Mass",
"Weight", "Friction", "Inertia", "Work", "Power", "Kinetic Energy", "Potential Energy", "Thermodynamics", "Entropy", "Heat",
"Temperature", "Pressure", "Wave", "Frequency", "Wavelength", "Amplitude", "Light", "Optics", "Electromagnetism", "Electricity",
"Magnetism", "Circuit", "Voltage", "Current", "Resistance", "Capacitance", "Inductance", "Photon", "Electron", "Proton",
"Neutron", "Atom", "Nucleus", "Particle Physics", "String Theory", "Black Hole", "Singularity", "Dark Matter", "Higgs Boson", "Nuclear Physics"]

1649


Chemistry = ["Chemistry", "Atom", "Molecule", "Compound", "Element", "Periodic Table", "Electron", "Proton", "Neutron", "Isotope",
"Ion", "Covalent Bond", "Ionic Bond", "Metallic Bond", "Chemical Reaction", "Acid", "Base", "pH", "Catalyst", "Enzyme",
"Oxidation", "Reduction", "Electrolysis", "Solvent", "Solute", "Solution", "Mixture", "Alloy", "Polymer", "Crystal",
"Gas", "Liquid", "Solid", "Plasma", "Organic Chemistry", "Inorganic Chemistry", "Biochemistry", "Analytical Chemistry", "Physical Chemistry", "Quantum Chemistry",
"Thermodynamics", "Entropy", "Activation Energy", "Reaction Rate", "Equilibrium", "Molarity", "Avogadro's Number", "Hydrocarbon", "Amino Acid", "Protein"]

615


History = ["History", "Civilization", "Empire", "Dynasty", "Revolution", "War", "Peace Treaty", "Colonization", "Independence", "Monarchy",
"Republic", "Democracy", "Dictatorship", "Constitution", "Archaeology", "Artifacts", "Primary Source", "Secondary Source", "Chronology", "Era",
"Renaissance", "Industrial Revolution", "Middle Ages", "Ancient Egypt", "Greek Mythology", "Roman Empire", "Feudalism", "Crusades", "World War I", "World War II",
"Cold War", "Civil Rights", "Slavery", "Abolition", "Holocaust", "Genocide", "Imperialism", "Nationalism", "Reformation", "Exploration",
"Colonialism", "Enlightenment", "Revolutionary War", "Treaty of Versailles", "Great Depression", "Civil War", "Medieval", "Historical Figure", "Trade Route", "Cultural Heritage"
]

4409


Sociology and Anthropology = ["Sociology", "Anthropology", "Culture", "Society", "Social Structure", "Norms", "Values", "Beliefs", "Ethnography", "Socialization",
"Institutions", "Family", "Religion", "Education", "Economy", "Government", "Social Class", "Inequality", "Race", "Ethnicity",
"Gender", "Sexuality", "Social Identity", "Social Change", "Urbanization", "Rural Sociology", "Cultural Anthropology", "Linguistic Anthropology", "Physical Anthropology", "Archaeology",
"Kinship", "Ritual", "Symbolism", "Globalization", "Migration", "Social Mobility", "Power", "Authority", "Social Networks", "Community",
"Deviance", "Social Norms", "Taboo", "Acculturation", "Assimilation", "Ethnocentrism", "Cultural Relativism", "Rites of Passage", "Myth", "Social Theory"]

3438


Engineering = ["Engineering", "Design", "Innovation", "Technology", "Mechanics", "Dynamics", "Statics", "Thermodynamics", "Fluid Mechanics", "Materials Science",
"Electrical Engineering", "Civil Engineering", "Mechanical Engineering", "Chemical Engineering", "Aerospace Engineering", "Structural Engineering", "Environmental Engineering", "Computer Engineering", "Biomedical Engineering", "Robotics",
"Automation", "Simulation", "Prototyping", "CAD", "CAM", "Manufacturing", "Process Control", "Instrumentation", "Thermal Analysis", "Control Systems",
"Project Management", "Feasibility Study", "Engineering Ethics", "Safety Engineering", "Reliability", "Efficiency", "Optimization", "Load Analysis", "Stress Testing", "Vibration Analysis",
"Energy Systems", "Renewable Energy", "Electronics", "Power Systems", "Signal Processing", "Embedded Systems", "Communication Systems", "Software Engineering", "Engineering Mechanics", "Geotechnical Engineering"]

1949



Computer Science and Informatics = ["Computer Science", "Informatics", "Algorithm", "Data Structure", "Programming", "Software", "Hardware", "Database", "Networking", "Operating System",
"Artificial Intelligence", "Machine Learning", "Deep Learning", "Big Data", "Data Analysis", "Cybersecurity", "Cryptography", "Cloud Computing", "Software Engineering", "Systems Design",
"Object-Oriented Programming", "Functional Programming", "Computer Architecture", "Compilers", "Operating Systems", "Networking Protocols", "Web Development", "User Interface", "User Experience", "Human-Computer Interaction",
"Software Development Life Cycle", "Agile Methodology", "Version Control", "Debugging", "Testing", "Information Systems", "Distributed Systems", "Parallel Computing", "Data Mining", "Database Management System",
"Information Retrieval", "Natural Language Processing", "Robotics", "Embedded Systems", "Internet of Things", "Network Security", "Ethical Hacking", "Programming Languages", "Source Code", "Algorithmic Complexity"]

597


Energy and Resources = ["Energy", "Resources", "Renewable Energy", "Non-Renewable Energy", "Solar Power", "Wind Power", "Hydropower", "Geothermal Energy", "Biomass", "Fossil Fuels",
"Oil", "Natural Gas", "Coal", "Energy Efficiency", "Energy Conservation", "Energy Storage", "Battery", "Grid", "Power Plant", "Transmission",
"Distribution", "Nuclear Energy", "Radioactive Waste", "Energy Policy", "Sustainability", "Carbon Footprint", "Climate Change", "Greenhouse Gases", "Energy Audit",
"Renewable Resources", "Natural Resources", "Water Resources", "Mineral Resources", "Resource Management", "Resource Depletion", "Recycling", "Waste Management", "Energy Demand", "Energy Supply",
"Hydraulic Fracturing", "Energy Transition", "Smart Grid", "Energy Management", "Conservation Practices", "Environmental Impact", "Energy Independence", "Resource Efficiency", "Sustainable Development", "Energy Regulation"]

1397


Geography and Earth Sciences = ["Geography", "Earth Sciences", "Geology", "Geography", "Plate Tectonics", "Erosion", "Sedimentation", "Volcano", "Earthquake", "Landform",
"Topography", "Climate", "Weather", "Atmosphere", "Hydrology", "Soil Science", "Oceanography", "Glaciology", "Paleontology", "Mineralogy",
"Petrology", "Geomorphology", "Cartography", "Map", "Latitude", "Longitude", "Altitude", "Continents", "Oceans", "Rivers",
"Lakes", "Deserts", "Mountains", "Plains", "Fault Line", "Seismic Activity", "Hydrosphere", "Biosphere", "Lithosphere", "Stratigraphy",
"Volcanology", "Seismology", "Remote Sensing", "Geospatial Analysis", "Geographic Information System (GIS)", "Land Use", "Resource Management", "Natural Hazards", "Environmental Change", "Sustainable Land Management"]

4545


Environmental Sciences = ["Environmental Sciences", "Ecosystem", "Biodiversity", "Conservation", "Pollution", "Climate Change", "Sustainability", "Greenhouse Gases", "Renewable Energy", "Natural Resources",
"Ecology", "Habitat", "Deforestation", "Water Cycle", "Soil Erosion", "Waste Management", "Recycling", "Environmental Impact", "Air Quality", "Water Quality",
"Environmental Policy", "Carbon Footprint", "Global Warming", "Energy Efficiency", "Environmental Regulation", "Sustainable Development", "Climate Modeling", "Environmental Monitoring", "Land Degradation", "Urban Planning",
"Environmental Education", "Ecotoxicology", "Environmental Justice", "Resource Management", "Ecosystem Services", "Pollutant", "Chemical Waste", "Bioremediation", "Sustainable Agriculture", "Green Technology",
"Environmental Assessment", "Natural Disasters", "Ecosystem Restoration", "Marine Conservation", "Wetlands", "Forest Management", "Climate Adaptation", "Energy Conservation", "Soil Management", "Water Conservation"]

1496


Medicine = ["Medicine", "Healthcare", "Diagnosis", "Treatment", "Therapy", "Pharmacology", "Surgery", "Anatomy", "Physiology", "Pathology",
"Immunology", "Epidemiology", "Internal Medicine", "Pediatrics", "Cardiology", "Neurology", "Oncology", "Orthopedics", "Gynecology", "Dermatology",
"Radiology", "Gastroenterology", "Endocrinology", "Rheumatology", "Urology", "Pulmonology", "Psychiatry", "Anesthesiology", "Emergency Medicine", "Public Health",
"Clinical Trials", "Medical Research", "Genetics", "Biotechnology", "Pharmacotherapy", "Infectious Diseases", "Chronic Illness", "Acute Care", "Health Promotion", "Preventive Medicine",
"Medical Imaging", "Patient Care", "Rehabilitation", "Health Records", "Medical Ethics", "Medical Technology", "Vaccines", "Medical Diagnosis", "Surgical Procedures", "Health Assessment"]

3169


Biotechnology = ["Biotechnology", "Genetic Engineering", "Genomics", "Proteomics", "Bioinformatics", "Biochemical Engineering", "Molecular Biology", "Cloning", "Stem Cells", "Recombinant DNA",
"CRISPR", "Gene Therapy", "Biopharmaceuticals", "Bioprocessing", "Cell Culture", "Enzyme Technology", "Bioreactors", "Synthetic Biology", "Pharmacogenomics", "Drug Development",
"Biomarkers", "Biomaterials", "Tissue Engineering", "Vaccine Development", "Microbial Biotechnology", "Plant Biotechnology", "Agricultural Biotechnology", "Environmental Biotechnology", "Industrial Biotechnology", "Bioengineering",
"Metabolomics", "Proteins", "Antibodies", "Biosensors", "Biodegradation", "Bioremediation", "Functional Genomics", "Transcriptomics", "Bioethics", "Biotech Startups", "Clinical Trials",
"Biological Systems", "Genetic Modification", "GMO", "Pharmacology", "Biotech Innovations", "Cell Therapy", "Systems Biology", "Biosecurity", "Viral Vectors", "Gene Editing"]
1587


Mathematics = ["Mathematics", "Algebra", "Calculus", "Geometry", "Statistics", "Probability", "Differential Equations", "Linear Algebra", "Number Theory", "Topology",
"Combinatorics", "Mathematical Logic", "Set Theory", "Complex Numbers", "Real Numbers", "Functions", "Graph Theory", "Discrete Mathematics", "Mathematical Analysis", "Abstract Algebra",
"Statistics", "Probability Theory", "Integral Calculus", "Differential Calculus", "Vectors", "Matrices", "Eigenvalues", "Eigenvectors", "Matrix Theory", "Optimization",
"Numerical Methods", "Mathematical Modeling", "Cryptography", "Operations Research", "Chaos Theory", "Fractals", "Geometry", "Trigonometry", "Arithmetic", "Calculus of Variations",
"Fourier Transform", "Laplace Transform", "Partial Differential Equations", "Functional Analysis", "Game Theory", "Operations Research", "Symbolic Computation", "Boolean Algebra", "Proof Theory", "Number Systems"]
897



Philosophy = ["Philosophy", "Metaphysics", "Epistemology", "Ethics", "Logic", "Ontology", "Aesthetics", "Philosophy of Mind", "Existentialism", "Phenomenology",
"Rationalism", "Empiricism", "Utilitarianism", "Deontology", "Virtue Ethics", "Pragmatism", "Determinism", "Free Will", "Nihilism", "Absurdism",
"Stoicism", "Skepticism", "Idealism", "Materialism", "Dualism", "Monism", "Dialectic", "Hermeneutics", "Postmodernism", "Critical Theory",
"Political Philosophy", "Social Philosophy", "Philosophy of Science", "Philosophy of Religion", "Logic", "Critical Thinking", "Reasoning", "Ethical Theory", "Moral Philosophy", "Philosophy of Language",
"Philosophy of History", "Metaphysical Realism", "Nominalism", "Realism", "Relativism", "Objectivism", "Subjectivism", "Theory of Knowledge", "Analytic Philosophy", "Continental Philosophy"]

3822


Literature and Art = ["Literature", "Art", "Novel", "Poetry", "Drama", "Prose", "Fiction", "Non-Fiction", "Short Story", "Play",
"Essay", "Literary Criticism", "Narrative", "Theme", "Symbolism", "Metaphor", "Character", "Plot", "Setting", "Genre",
"Artistic Expression", "Painting", "Sculpture", "Drawing", "Printmaking", "Photography", "Installation Art", "Performance Art", "Abstract Art", "Realism",
"Impressionism", "Expressionism", "Cubism", "Surrealism", "Modernism", "Postmodernism", "Renaissance", "Baroque", "Gothic", "Romanticism",
"Literary Device", "Poetic Form", "Dialogue", "Allusion", "Imagery", "Art Criticism", "Art History", "Cultural Heritage", "Visual Arts", "Literary Genre",
"Artistic Movement", "Aesthetic", "Narrator", "Literary Theory", "Artistic Technique", "Canvas", "Muse", "Art Gallery", "Literary Canon", "Craftsmanship"]

4317


Communication = ["Communication", "Verbal Communication", "Nonverbal Communication", "Interpersonal Communication", "Mass Communication", "Digital Communication", "Public Speaking", "Listening", "Writing", "Reading",
"Media", "Social Media", "Broadcasting", "Journalism", "Public Relations", "Marketing", "Advertising", "Persuasion", "Message", "Feedback",
"Communication Theory", "Body Language", "Tone", "Context", "Medium", "Channel", "Signal", "Encoding", "Decoding", "Information",
"Speech", "Conversation", "Dialogue", "Negotiation", "Conflict Resolution", "Cultural Communication", "Cross-Cultural Communication", "Intercultural Communication", "Nonverbal Cues", "Facial Expression",
"Gestures", "Communication Skills", "Communication Barriers", "Effective Communication", "Information Technology", "Media Literacy", "Telecommunication", "Virtual Communication", "Network", "Language"
]

2578

Politics = ["Politics", "Government", "Democracy", "Republic", "Monarchy", "Dictatorship", "Political Party", "Election", "Legislation", "Policy",
"Constitution", "Parliament", "Congress", "Senate", "Executive", "Judiciary", "Bureaucracy", "Public Administration", "Campaign", "Voting",
"Political Ideology", "Liberalism", "Conservatism", "Socialism", "Communism", "Fascism", "Nationalism", "Populism", "Anarchism", "Totalitarianism",
"Federalism", "State", "Nation", "Diplomacy", "International Relations", "Political Theory", "Political Philosophy", "Civil Rights", "Human Rights", "Social Justice",
"Political Economy", "Corruption", "Lobbying", "Public Policy", "Governance", "Political Science", "Representation", "Sovereignty", "Power", "Constituency"
]
3198

Law = ["Legal Precedent", "Courtroom", "Plea Bargain", "Indictment", "Subpoena", "Affidavit", "Deposition", "Discovery", "Injunction", "Habeas Corpus",
"Plaintiff", "Defendant", "Counsel", "Cross-Examination", "Settlement", "Verdict", "Sentence", "Parole", "Probation", "Alibi",
"Acquittal", "Guilty", "Not Guilty", "Bail", "Custody", "Warrant", "Search Warrant", "Arrest", "Prosecution", "Defense Attorney",
"Public Defender", "Civil Rights", "Human Rights", "Legal Code", "Ordinance", "Statutory Interpretation", "Jurisprudence", "Legal Counsel", "Barrister", "Solicitor",
"Amicus Curiae", "Brief", "Legal Aid", "Case Law", "Administrative Law", "Appellate Court", "Small Claims Court", "Legal Reform", "Criminal Justice", "Forensic Evidence"
]

607

Economics = ["Economics", "Supply and Demand", "Market", "Inflation", "Deflation", "Gross Domestic Product (GDP)", "Unemployment", "Interest Rate", "Monetary Policy", "Fiscal Policy",
"Capitalism", "Socialism", "Free Market", "Trade", "Tariff", "Subsidy", "Exchange Rate", "Budget", "Deficit", "Surplus",
"Recession", "Depression", "Economic Growth", "Development", "Income", "Wealth", "Poverty", "Inequality", "Labor Market", "Productivity",
"Investment", "Stock Market", "Bond", "Currency", "Foreign Exchange", "Balance of Payments", "Economic Indicators", "Consumer Price Index (CPI)", "Purchasing Power", "Economic Theory",
"Microeconomics", "Macroeconomics", "Public Finance", "International Trade", "Supply Chain", "Competition", "Market Structure", "Oligopoly", "Monopoly", "Econometrics"
]

1329

Business = ["Business", "Entrepreneurship", "Start-up", "Corporation", "Partnership", "Sole Proprietorship", "Business Plan", "Revenue", "Profit", "Loss",
"Marketing", "Branding", "Sales", "Customer Service", "Product Development", "Supply Chain", "Inventory Management", "E-commerce", "Retail", "Wholesale",
"Finance", "Investment", "Accounting", "Budgeting", "Cash Flow", "Profit Margin", "Market Research", "Business Strategy", "Human Resources", "Management",
"Leadership", "Organizational Behavior", "Corporate Culture", "Business Ethics", "Corporate Social Responsibility", "Stakeholders", "Shareholders", "Merger", "Acquisition", "Innovation",
"Risk Management", "Operations Management", "Quality Control", "Logistics", "Distribution", "Outsourcing", "Globalization", "Business Law", "Contract", "Negotiation"
]

2107

Culture = ["Culture", "Tradition", "Custom", "Heritage", "Values", "Beliefs", "Ritual", "Language", "Art", "Music",
"Dance", "Literature", "Cuisine", "Festivals", "Religion", "Folklore", "Norms", "Social Practices", "Identity", "Ethnicity",
"Traditions", "Cultural Diversity", "Cultural Exchange", "Cultural Heritage", "Artistry", "Craftsmanship", "Symbolism", "Mythology", "Ceremony", "Belief Systems",
"Customs", "Heritage Sites", "Cultural Anthropology", "Cultural Preservation", "Cultural Evolution", "Cultural Adaptation", "Social Norms", "Cultural Values", "Cultural Identity", "Cultural Expression",
"Traditions", "Rituals", "Art Forms", "Social Structure", "Cultural Artifacts", "Music Genres", "Dance Styles", "Cultural Practices", "Storytelling", "Myth"
]

3199

Society = ["Society", "Community", "Social Structure", "Social Norms", "Social Institutions", "Social Interaction", "Social Groups", "Culture", "Social Change", "Social Stratification",
"Social Class", "Inequality", "Demographics", "Population", "Cohesion", "Social Dynamics", "Social Networks", "Social Roles", "Status", "Socialization",
"Family", "Education", "Religion", "Government", "Economy", "Healthcare", "Law", "Public Policy", "Social Services", "Media",
"Social Problems", "Crime", "Homelessness", "Poverty", "Discrimination", "Civil Rights", "Human Rights", "Citizenship", "Identity", "Community Engagement",
"Urbanization", "Rural Areas", "Migration", "Social Movements", "Activism", "Social Welfare", "Social Justice", "Social Capital", "Collective Action", "Social Integration"
]


2828
"""
