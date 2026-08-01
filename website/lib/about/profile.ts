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
  "He contributes to certificate-grade reproducible research workflows, maintaining version-controlled science, validation artefacts, and this public-facing research portal as part of the Swiss certificate programme (AMGCR).",
] as const;

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
    "A reproducible research programme aligned with the Swiss certificate project (AMGCR), combining a completed California FDSN pilot (Version 1.0) with an interactive documentation and exploration platform (Version 2.0). The work connects literature-aligned AI methodology with open, auditable geophysical data processing.",
  highlights: [
    "California IRIS/EarthScope pilot — eight events, 8×18 ML-ready feature matrix (science frozen v1.0.0)",
    "End-to-end workflow: acquisition → EDA → signal analysis → preprocessing → features → interpretation",
    "Europe-focused long-term direction with California as the methods laboratory",
    "Public report, presentation, and validation PASS submission package (D-F1–F4)",
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
    label: "AMGCR v1.0 submission",
    detail: "California pilot · reproducible pipeline · validation PASS · 2026-07-29",
    status: "complete" as const,
  },
  {
    label: "Interactive platform v2.0",
    detail: "Documentation portal, explorers, and public research dashboard",
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
  "The Swiss certificate programme (AMGCR) framework that structures the reproducible earthquake early warning research deliverables.",
  "Indian Institute of Technology Jodhpur and the AIDE community for academic support and infrastructure.",
  "Open geophysical data providers (USGS, IRIS/EarthScope) and the ObsPy developer community for foundational tooling.",
  "Contributors and reviewers who supported the Version 1.0 submission validation and documentation quality.",
] as const;
