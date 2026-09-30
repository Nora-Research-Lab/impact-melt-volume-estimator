import gradio as gr
from impact_melt_volume_estimator import (
    compute_melt_volume,
    classify_melt_volume,
    generate_reference_sentence,
    generate_bar_chart,
)

def estimate(D, target_type, uncertainty):
    try:
        D = float(D)
        if D < 0.1 or D > 1000:
            raise ValueError("Diameter must be between 0.1 and 1000 km.")
        result = compute_melt_volume(D, target_type, uncertainty)
        M = result["value"]
        logM = result["logM"]
        warning = result["warning"]
        classification = classify_melt_volume(M)
        sentence = generate_reference_sentence(M, D, target_type)
        if uncertainty:
            low = result["bounds"]["low"]
            high = result["bounds"]["high"]
            numeric_out = f"Estimated melt volume: {M:.2f} km³   (± {low:.2f} – {high:.2f} km³)"
        else:
            numeric_out = f"Estimated melt volume: {M:.2f} km³"

        if warning:
            numeric_out += f"\n⚠️ Warning: {warning}"

        fig = generate_bar_chart(M, D, target_type)

        return numeric_out, classification, fig, sentence
    except Exception as e:
        return f"Error: {str(e)}", "", None, ""

target_type_choices = [
    "Silicate (e.g. lunar highlands, martian crust)",
    "Carbonate-rich (e.g. sedimentary basins)",
    "Ice/Snow (e.g. polar caps)",
]

with gr.Blocks(theme="dark", title="Impact Melt Volume Estimator") as demo:
    gr.Markdown(
        """
    # Impact Melt Volume Estimator
    **Empirical relations from Grieve & Cintala (1992, 1997) and Pierazzo et al. (1997)**
    """
    )
    with gr.Row():
        D_input = gr.Number(
            label="Crater Diameter (km)",
            minimum=0.1,
            maximum=1000,
            step=0.01,
            value=10.0,
        )
        target_input = gr.Dropdown(
            label="Target Rock Type",
            choices=target_type_choices,
            value="Silicate (e.g. lunar highlands, martian crust)",
        )
    uncert_input = gr.Checkbox(label="Include uncertainty bounds", value=False)
    calc_btn = gr.Button("Calculate", variant="primary")

    with gr.Column():
        numeric_out = gr.Textbox(label="Melt Volume Estimate")
        class_out = gr.Textbox(label="Classification")
        chart_out = gr.Plot(label="Comparison with Typical Melt Volumes")
        sentence_out = gr.Textbox(label="Interpretive Sentence")

    calc_btn.click(
        fn=estimate,
        inputs=[D_input, target_input, uncert_input],
        outputs=[numeric_out, class_out, chart_out, sentence_out],
    )

demo.launch(server_name="0.0.0.0", server_port=7860)
