![NORA logo](https://i.ibb.co/0VJCC9Gf/IMG-20260114-WA0008.jpg)
 
# Impact Melt Volume Estimator
 
*For planetary geoscientists and impact specialists: enter crater diameter and target rock type to instantly estimate the volume of impact melt produced.*
 
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
 

## Overview
 
**Industry:** Planetary Geoscience
 
**Inputs:** (1) Crater diameter (D) in kilometers, numeric input with step 0.01 from 0.1 to 1000. (2) Target rock type, a dropdown with options: 'Silicate (e.g. lunar highlands, martian crust)', 'Carbonate-rich (e.g. sedimentary basins)', 'Ice/Snow (e.g. polar caps)'. (3) (Optional) checkbox to include uncertainty bounds.

**Core calculation:** Uses established empirical power-law relations from Grieve & Cintala (1992, 1997) and Pierazzo et al. (1997) for impact melt volume (M, in km³) as a function of D (km):
- Silicate: log₁₀(M) = 0.253 + 2.764 × log₁₀(D)  (σ ~0.2)
- Carbonate: log₁₀(M) = -0.663 + 3.194 × log₁₀(D)
- Ice/Snow: log₁₀(M) = -1.040 + 3.500 × log₁₀(D)  (based on laboratory relations)
If uncertainty checkbox is ticked, the tool also reports the upper/lower bounds using the standard deviation σ. The computed M is checked against a sanity threshold: M should not exceed the crater's excavated volume (approximated as 0.3 × D³). If exceeded, a warning is shown.

**Output:** (1) Numerical value: 'Estimated melt volume: X.XX km³' (with ± bounds if selected). (2) A qualitative classification: Miniscule (<0.1 km³), Small (0.1–10 km³), Moderate (10–1000 km³), Large (1000–10⁵ km³), Basin-scale (>10⁵ km³). (3) A horizontal bar chart showing the melt volume relative to typical lunar and terrestrial impact melts for reference (using sample bodies: Moon, Earth, Mars). The chart is generated using matplotlib. (4) A short interpretive sentence: e.g., 'This melt volume is comparable to the lunar crater Copernicus.' based on simple lookup of reference craters embedded in code.

**UI layout:** Vertical layout: title, then two inputs side-by-side (Diameter and Target type), checkbox, then 'Calculate' button. Output area below displays the numeric result, classification badge, bar chart, and interpretive sentence. Clean, science-report style with a dark background option.

**AI/ML component:** None. Pure empirical geophysical relationships.
 
## Run it
 
```bash
docker build -t impact-melt-volume-estimator .
docker run -p 7860:7860 impact-melt-volume-estimator
```
 
Then open http://localhost:7860 in your browser.
 
## About
 
This tool was generated and published automatically by the **NORA Earth Intelligence**
tool factory, an autonomous pipeline maintained by **NORA Research Lab** that turns
one idea per run into a small, working geoscience tool — end to end, with an
LLM writing and Docker-testing the code, and another model generating the
banner above.
 
- Platform: [https://noraearth.xyz](https://noraearth.xyz)
- Parent lab: [https://noraresearchlab.site](https://noraresearchlab.site)
 
Built 2026-09-30.
 
---
 
### Maintainer
 
**NORA Research Lab**
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
