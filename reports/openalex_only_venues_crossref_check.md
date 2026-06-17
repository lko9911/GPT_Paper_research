# OpenAlex-only Venue Analysis with Crossref Journal Lookup

## Scope
- Source data: `reports/source_overlap_venues.csv` and `reports/source_overlap_records_all_3075.csv`
- Dataset scope: 3,075 collected candidates from the current tracker data
- Venues observed only through OpenAlex in this dataset: 428
- Crossref journal lookup used `/journals?query=...&rows=20`.

## Important Interpretation
- `OpenAlex-only in dataset` means the venue appeared only on records whose stored source included OpenAlex but not Crossref.
- It does **not** automatically mean Crossref has no journal record for that venue.
- Exact title matches are stronger evidence of Crossref venue coverage than possible matches.

## Crossref Lookup Result Counts
- no_crossref_journal_match: 93
- possible_crossref_journal_match: 3
- exact_crossref_journal_match: 332
- lookup_error: 0

## Top OpenAlex-only Venues With No Crossref Journal Match
| Venue | Records | Curated | Archived | Example titles |
|---|---:|---:|---:|---|
| Zenodo (CERN European Organization for Nuclear Research) | 76 | 9 | 67 | Sharp Dual-Regime Transition Driven by Bead Morphology in Metal Fused Filament Fabrication: Bead-Resolved Digital Twin Analysis / Binary Thermal Regime Transition Driven by Bead Morphology in Metal Fused Filament Fabrica |
| ArXiv.org | 48 | 12 | 36 | i-Tac: Inverse Design of 3D-Printed Tactile Elastomers with Scalable and Tunable Optical and Mechanical Properties / Environment-Aware Path Generation for Robotic Additive Manufacturing of Structures / Self-locking non-v |
| arXiv (Cornell University) | 46 | 20 | 26 | Towards Active Real-to-Twin Inspection: A New Paradigm for Zero-Shot Anomaly Detection / Too Big, Too Small, Too $O_2$: The Pandoro Effect from Oxygen Gradients in Tomographic Volumetric Additive Manufacturing / Scale-in |
| Figshare | 23 | 2 | 21 | Lensless and Lossless HoloVAM / High-Strength andFast-Response Liquid Crystal ElastomerFiber and Fabric Actuators / Smart manufacturing: MLOps-enabled event-driven architecture for enhanced control in steel production |
| Springer Link (Chiba Institute of Technology) | 9 | 4 | 5 | Transitioning from Industry 4.0 to Industry 5.0: A Review and Analysis of Future Research Directions / Semi-analytical Timoshenko beam model for symmetrical 1D acoustic black holes: Efficient quantification of the influe |
| ACS Applied Materials & Interfaces | 6 | 4 | 2 | Emerging Trends in Additive Manufacturing for Thermoelectric Devices: Materials, Structures, and Engineering Approaches / High-Strength and Fast-Response Liquid Crystal Elastomer Fiber and Fabric Actuators / Hot Fingers: |
| Materials & Design | 4 | 3 | 1 | Interfacial structure − property relationships in additively manufactured WC-Co/316L multi-material systems / Machine learning-aided lattice optimization for ultra-lightweight 3D-printed aligners / 4D printing of semi-cr |
| VTechWorks (Virginia Tech) | 4 | 1 | 3 | Advancing New Material and Process Capabilities for Multi-Material High Performance Thermoset Additive Manufacturing / Rapid Characterization of Material Heterogeneity through Acoustic Resonance and Physics-informed Arti |
| bioRxiv (Cold Spring Harbor Laboratory) | 3 | 3 | 0 | Shaping hydrogel bioinks into 3D, multiscale, perfusable models using multimodal printing / Tomographic Printing in a Chip: A Versatile Platform for Biomimetic 3D Organ-on-Chip / Optical Properties of Gelatin Methacrylat |
| Espace ÉTS (ETS) | 3 | 3 | 0 | Meltpool temperature measurement and monitoring during wire-DED via optical thermal devices / Digital twin modeling for defect detection in LPBF parts / Resin properties and part size interrelationships in computed tomog |
| Microsystems & Nanoengineering | 3 | 3 | 0 | Proximal sound printing: direct 3D printing of microstructures on polymers / Electrohydrodynamic printed ultra-high performance liquid metal strain sensor / Micro-spring force sensors using conductive photosensitive resi |
| Repository KITopen (Karlsruhe Institute of Technology) | 3 | 1 | 2 | Enhancing mechanical performance of elastomeric vat-photopolymerized resins via functionalized cellulose nanocrystals / Wavelength‐Dependent 3D Printing: Introducing 3D Printed Action Plots / Novel Photoinitiators for Tw |
| Texas Digital Library (University of Texas) | 3 | 2 | 1 | Replication Data for: Hybrid epoxy–acrylate resins for wavelength-selective multimaterial 3D printing / Engineering soft materials across length scales for programmable performance / Oxygen Saturation as a Strategy to Mi |
| TU/e Research Portal | 3 | 1 | 2 | NURBS-Based Ray Tracer Modeling of Tomographic Volumetric Additive Manufacturing / Edge-Cloud-Assisted Real-Time Cyber-Physical Systems / Data-Driven Optimization for City Logistics |
| ACS Sustainable Chemistry & Engineering | 2 | 2 | 0 | Thiol–Yne Photocurable Isosorbide-Derived Networks: Formulation and 3D Printing / Sustainable 3D Printing of Transparent SiO<sub>2</sub> Glass Components by a Photocurable Aqueous Suspension Design |
| Advances in geospatial technologies book series | 2 | 0 | 2 | Energy Mapping and Resource Efficiency Using Geospatial Tools / An Adaptive Geo-Intelligent System Integrating AI and IoT for Sustainable Smart Manufacturing |
| DergiPark (Istanbul University) | 2 | 2 | 0 | An Investigation -into the Use of Digital Technologies to Promote Circularity in the Construction Industry / Üç Boyutlu Yazıcı Teknolojileri ve Diş Hekimliğinde Uygulama Alanları: Güncel Yaklaşımlar ve Gelecek Perspektif |
| Digital Access to Scholarship at Harvard (DASH) (Harvard University) | 2 | 1 | 1 | Programmable Assembly of Genetically Engineered Human Tissues / Architected Liquid Crystal Elastomers with Spatially Programmed Alignment, Shape Morphing, and Mechanics |
| DOAJ (DOAJ: Directory of Open Access Journals) | 2 | 1 | 1 | Recent Advances and Development Trends of Global Top Drive Drilling Systems / Construction of an industrial digital twin platform for multi-robot arm collaborative control |
| Linköping studies in science and technology. Dissertations | 2 | 1 | 1 | Adaptive Automation Strategies for Increasing Variability in Design and Production / Digital Twins and Explainable AI for Decision Support in Port and Maritime Operations |
| LUTPub (LUT University) | 2 | 1 | 1 | Experimental and numerical study of the Poynting effect in additively manufactured TPU components for soft robotic applications / Performance management with novel technologies : integrating sustainability performance in |
| TSpace | 2 | 1 | 1 | Mechanics and Modeling of 3D Printed Metamaterials for Energy Absorption / Using Multi-Material Additive Manufacturing and Targeting Active Applications in the Design and Development of Hydrophobic Surfaces |
| Veredas do Direito Direito Ambiental e Desenvolvimento Sustentável | 2 | 0 | 2 | ENHANCING OPERATIONAL EFFICIENCY IN NATURAL GAS DISTRIBUTION THROUGH - AUTOMATION AND SMART CONTROL SYSTEMS / DIGITAL SUPPLY CHAIN TRANSFORMATION IN SAUDI INDUSTRIAL MANUFACTURING UNDER VISION 2030 |
| American University of Bahrain | 1 | 0 | 1 | Smart manufacturing: MLOps-enabled event-driven architecture for enhanced control in steel production |
| AMS Degree Thesis (University of Bologna) | 1 | 1 | 0 | Il ruolo del Digital Twin nell'Additive Manufacturing: opportunità e prospettive per l'ingegneria industriale |
| Applied Cybersecurity & Internet Governance | 1 | 0 | 1 | A Cybersecurity Digital Twin Architecture for Modelling Threats in Interconnected Systems |
| Biomedical Journal of Scientific & Technical Research | 1 | 1 | 0 | "Guidelines for Biomimetic 3D/4D Printing in Soft Tissues Biomaterials" |
| CINECA IRIS Institutial Research Information System (University of Genoa) | 1 | 1 | 0 | DIVENIRE Metodo, processo e progetto di un sistema di facciata dinamico realizzato tramite stampa 3D e 4D - Method, process and design of a dynamic facade system created using 3D and 4D printing |
| Communications in computer and information science | 1 | 1 | 0 | FPGA-Driven Nonlinear Analogue Networks for Deterministic Machine Learning |
| Complex & Intelligent Systems | 1 | 1 | 0 | Multi-domain fusion meta-model for digital twin in precision manufacturing: design, implementation and verification |

## Top OpenAlex-only Venues That Do Have Exact Crossref Journal Matches
| Venue | Records | Crossref title | ISSN | Crossref total DOIs |
|---|---:|---|---|---:|
| Open MIND | 12 | Open Mind | 2470-2986 | 295 |
| Biomimetics | 8 | Biomimetics | 2313-7673 | 3222 |
| Sensors | 7 | Sensors | 1424-8220 | 78573 |
| ACS Applied Polymer Materials | 5 | ACS Applied Polymer Materials | 2637-6105; 2637-6105 | 7628 |
| ACS Polymers Au | 4 | ACS Polymers Au | 2694-2453; 2694-2453 | 375 |
| Nano-Micro Letters | 4 | Nano-Micro Letters | 2311-6706; 2150-5551 | 2547 |
| Sustainability | 4 | Sustainability | 2071-1050 | 105718 |
| Bioengineering | 3 | Bioengineering | 2306-5354 | 6409 |
| Communications Materials | 3 | Communications Materials | 2662-4443 | 1215 |
| Exploring Science Academic Conference Series | 3 | Exploring Science Academic Conference Series | 3105-0514; 3105-0522 | 239 |
| International Journal for Research in Applied Science and Engineering Technology | 3 | International Journal for Research in Applied Science and Engineering Technology | 2321-9653 | 40225 |
| International Journal of Drug Delivery Technology | 3 | International Journal of Drug Delivery Technology | 0975-4415; 0975-4415 | 8064 |
| Journal of Applied Polymer Science | 3 | Journal of Applied Polymer Science | 0021-8995; 1097-4628 | 67947 |
| Macromolecules | 3 | Macromolecules | 0024-9297; 1520-5835 | 52155 |
| Molecules | 3 | Molecules | 1420-3049; 1420-3049 | 64474 |
| Nature | 3 | Nature | 0028-0836; 1476-4687 | 446174 |
| Proceedings of the National Academy of Sciences | 3 | Proceedings of the National Academy of Sciences | 0027-8424; 1091-6490 | 170469 |
| Sustainable materials and technologies | 3 | Sustainable Materials and Technologies | 2214-9937 | 2086 |
| Acta Biomaterialia | 2 | Acta Biomaterialia | 1742-7061 | 11078 |
| Advanced Composites and Hybrid Materials | 2 | Advanced Composites and Hybrid Materials | 2522-0128; 2522-0136 | 1879 |
| Advanced Engineering Informatics | 2 | Advanced Engineering Informatics | 1474-0346 | 4504 |
| Advanced Healthcare Materials | 2 | Advanced Healthcare Materials | 2192-2640; 2192-2659 | 9767 |
| Architectural Intelligence | 2 | Architectural Intelligence | 2731-6726 | 120 |
| Automation | 2 | Automation | 2673-4052 | 297 |
| Clean Technologies | 2 | Clean Technologies | 2571-8797 | 542 |
| Composites Part C Open Access | 2 | Composites Part C Open Access | 2666-6820 | 737 |
| EAI Endorsed Transactions on Digital Transformation of Industrial Processes | 2 | EAI Endorsed Transactions on Digital Transformation of Industrial Processes | 3106-0536 | 49 |
| Engineering Research | 2 | Engineering Research | 3091-3306 | 13 |
| Heritage | 2 | Heritage | 2571-9408 | 2295 |
| Iconic Research and Engineering Journals | 2 | Iconic Research and Engineering Journals | 2456-8880 | 3788 |

## Notable Example
- `Nature` is OpenAlex-only in the current dataset, but Crossref journal lookup returns an exact `Nature` match with ISSN `0028-0836; 1476-4687` and `446174` total DOIs. This means Nature is not absent from Crossref; the current pipeline simply collected those Nature records through OpenAlex.

## Output Files
- `reports/openalex_only_venues_crossref_check.csv`: full venue-level table.
- `reports/openalex_only_venues_crossref_check.xlsx`: Excel version of the same table plus summary.

## Recommendation
- Use `no_crossref_journal_match` venues as candidates for removal if you want a Crossref-centered, journal-focused tracker.
- Review `exact_crossref_journal_match` venues carefully: these are not truly absent from Crossref; they were only OpenAlex-only in the current collection pipeline.
- For high-value venues such as `Nature`, DOI-level Crossref enrichment can move them from OpenAlex-only to both-source without relying on Crossref keyword search.
