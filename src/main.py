import solution as s
import gradio as gr

inputs = gr.inputs.Image(type="filepath", label="Upload an image of the maze")
outputs = gr.outputs.Image(type="numpy", label="Solved Maze")
examples = [["in/41.png"], ["in/141.png"], ["in/501.png"], ["in/511x257.png"]]
# Create the Gradio interface
gr.Interface(
    fn=s.solve,
    inputs=inputs,
    outputs=outputs,
    title="Maze Solver",
    examples=examples,
).launch(share=True)
