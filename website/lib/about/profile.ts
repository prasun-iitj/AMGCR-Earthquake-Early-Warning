/** About page content — researcher profile and academic supervision (About page only). */

export const researcher = {
  name: "Prasun Kumar Tripathi",
  rollNumber: "M25AI2151",
  program: "M.Tech in Artificial Intelligence",
  institute: "Indian Institute of Technology Jodhpur",
  instituteShort: "IIT Jodhpur",
  department: "School of Artificial Intelligence and Data Science (AIDE)",
  instituteEmail: "m25ai2151@iitj.ac.in",
  personalEmail: "sanu.prasun@gmail.com",
  linkedIn: "https://www.linkedin.com/in/prasun-kumar-tripathi-70a8b858/",
  github: "https://github.com/prasun-iitj",
} as const;

export const researchArea =
  "Heteroscedastic ensemble deep random vector functional link for Early Peak Ground Acceleration.";

/** From https://anushka-joshi.github.io/ — designation inferred from IIT Jodhpur teaching & contact listing only. */
export const academicSupervisor = {
  name: "Dr. Anushka Joshi",
  profileUrl: "https://anushka-joshi.github.io/",
  department:
    "School of Artificial Intelligence and Data Science (AIDE), Indian Institute of Technology Jodhpur",
  /** Assistant Professor, AIDE, IIT Jodhpur (official faculty profile). */
  designation:
    "Assistant Professor of AI and Data Science, School of Artificial Intelligence and Data Science, IIT Jodhpur",
  researchInterests: [
    "Deep learning and data-driven AI",
    "Multivariate time-series analysis and deep learning for signals",
    "Natural disasters — earthquakes, tsunami, landslide, and sustainability",
    "Real-world applications, innovation, and deployment",
    "Generative AI — diffusion models, tabular data generation, and GANs",
  ],
} as const;

export const researcherBio = [
  "Prasun Kumar Tripathi is an M.Tech Artificial Intelligence scholar (Roll No. M25AI2151) at the School of Artificial Intelligence and Data Science (AIDE), Indian Institute of Technology Jodhpur. His graduate research focuses on machine-learning approaches for earthquake early warning, with particular emphasis on peak ground acceleration prediction using heteroscedastic ensemble deep random vector functional link architectures.",
  "Alongside his degree programme, he develops and documents the AMGCR Earthquake Early Warning Research platform — a reproducible, open pipeline spanning FDSN waveform acquisition, signal analysis, feature engineering, and interactive dissemination of pilot results from Western seismic regions.",
  "He maintains the version-controlled science, validation artefacts and this public research portal for the AMGCR major research project at IIT Jodhpur.",
] as const;

/** Institutional identity and academic background (About page). Wording kept factual; no formal partnership is implied. */
export const projectBackground = {
  heading: "Institutional identity and academic background",
  paragraphs: [
    "AMGCR (Assessment and Management of Geological and Climate Related Risk) is an IIT Jodhpur major research project.",
    "The AMGCR research journey has an academic association with the Swiss Certificate Programme and has evolved into a major research project at IIT Jodhpur. The project brings together seismic data analysis, signal processing and machine-learning-based P-wave detection research.",
    "Switzerland also appears in the research as a data source: Swiss seismic records from the Swiss Seismological Service (SED, ETH Zurich) are used for model development (Set A) and independent evaluation (Set C). This is a data reference, not an institutional affiliation.",
  ],
} as const;

export const researchInterests = [
  {
    title: "Earthquake early warning",
    description:
      "Early estimation of peak ground acceleration and related ground-motion proxies from seismic waveforms.",
  },
  {
    title: "Ensemble deep learning",
    description:
      "Heteroscedastic ensemble deep random vector functional link models for robust, uncertainty-aware prediction.",
  },
  {
    title: "Seismic signal processing",
    description:
      "Feature engineering, preprocessing, and analysis of FDSN/IRIS waveform data using ObsPy-based pipelines.",
  },
  {
    title: "Reproducible AI research",
    description:
      "Open documentation, frozen submission releases, and interactive platforms for transparent scientific communication.",
  },
] as const;

export const researchProject = {
  title: "AMGCR Earthquake Early Warning Research",
  summary:
    "A reproducible research project on AI-assisted seismic signal analysis and P-wave detection. It combines a completed California pilot (Version 1.0), Swiss SED datasets (Set A for development, Set C for independent evaluation), engineered features, Random Forest and XGBoost models with event-grouped cross-validation, and a comparison with STA/LTA detection. It is an offline research benchmark, not an operational early-warning system.",
  highlights: [
    "California IRIS/EarthScope pilot: eight events, 8×18 feature matrix (science frozen v1.0.0)",
    "Swiss SED data: 20 development events (Set A) and 15 independent events (Set C) with manual first-P picks",
    "Workflow: acquisition → preprocessing → manual P labels → candidate windows → features → models → independent evaluation",
    "Documented limitations, data lineage and reproduction guides for academic review",
  ],
} as const;

export const researchTimeline = [
  {
    label: "M.Tech AI programme",
    detail: "IIT Jodhpur · AIDE · Roll M25AI2151",
    status: "current" as const,
  },
  {
    label: "Graduate research topic",
    detail: researchArea,
    status: "current" as const,
  },
  {
    label: "Swiss Certificate Programme association",
    detail: "Academic background of the research; AMGCR v1.0 submission with the California pilot, validation PASS, 2026-07-29",
    status: "complete" as const,
  },
  {
    label: "Swiss datasets and models",
    detail: "SED data (Set A, Set C), engineered features, Random Forest and XGBoost, independent Swiss validation",
    status: "complete" as const,
  },
  {
    label: "Research platform and handover",
    detail: "Documentation portal, data and ML evaluation pages, and academic review package",
    status: "current" as const,
  },
] as const;

export const technologiesUsed = [
  "Python",
  "ObsPy",
  "FDSN / IRIS",
  "NumPy · Pandas · SciPy",
  "Machine learning & feature engineering",
  "Next.js · TypeScript · Tailwind CSS",
  "Markdown documentation pipeline",
  "Git · GitHub",
] as const;

export const acknowledgements = [
  "Dr. Anushka Joshi, School of Artificial Intelligence and Data Science (AIDE), IIT Jodhpur, for academic supervision and research guidance.",
  "The Swiss Certificate Programme, with which the AMGCR research journey has an academic association (no formal partnership or endorsement is implied).",
  "Indian Institute of Technology Jodhpur and the AIDE community for academic support and infrastructure.",
  "Open geophysical data providers (USGS, IRIS/EarthScope, and the Swiss Seismological Service SED/ETH Zurich) and the ObsPy developer community for foundational tooling.",
  "Contributors and reviewers who supported the Version 1.0 submission validation and documentation quality.",
] as const;
