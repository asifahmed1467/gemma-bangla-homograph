r"""A small web page to try the model: type a Bangla sentence, see the answer.

Run:  python app.py                              (uses the adapter folder gemma_cpu_lora next to this file)
      python app.py --adapter D:\path\to\gemma_cpu_lora
      python app.py --fake                       (no model: stand-in answers, only to look at the page)
Then open the address it prints (http://127.0.0.1:7860) in your browser.
"""
import argparse
import gradio as gr
from homograph_lookup import WORDS_CSV, TAG, load_words, fix_sentence, get_generate

ap = argparse.ArgumentParser()
ap.add_argument("--adapter", default="gemma_cpu_lora", help="folder made by train_cpu.py")
ap.add_argument("--words", default=str(WORDS_CSV), help="CSV with a 'homograph' column")
ap.add_argument("--fake", action="store_true", help="stand-in instead of Gemma (page check only)")
ap.add_argument("--port", type=int, default=7860)
a = ap.parse_args()

words, said = load_words(a.words)
generate = get_generate(a.adapter, a.fake, said)

EXAMPLES = [
    "আমি কেন যাব?",
    "আজ গল্পের আসর বেশ জমে উঠেছে।",
    "কাঠমিস্ত্রি করাত দিয়ে কাঠ কাটছেন।",
    "আমি প্রতিদিন সকালে এক কাপ চা খাই।",
]


def run(sentence):
    if not sentence.strip():
        return "", "", "type a sentence first"
    r = fix_sentence(sentence, words, generate)
    if r["called_model"]:
        status = "homograph found: " + ", ".join(r["found"]) + "  → model was called"
    else:
        status = "no homograph from the list  → model was NOT called, sentence returned unchanged"
    return r["tagged"], r["output"], status


with gr.Blocks(title="Bangla homograph fixer") as demo:
    gr.Markdown(f"# Bangla homograph fixer\nWords in the list: {', '.join(sorted(words))}\n\n"
                f"The page puts `{TAG}` in front of each listed word, then asks the model. "
                "Sentences without a listed word are returned unchanged." + ("\n\n**STAND-IN MODE: not Gemma.**" if a.fake else ""))
    box = gr.Textbox(label="Sentence", lines=2)
    btn = gr.Button("Run", variant="primary")
    tagged = gr.Textbox(label="Input sent to the model", interactive=False)
    out = gr.Textbox(label="Output", interactive=False)
    status = gr.Textbox(label="What happened", interactive=False)
    gr.Examples(EXAMPLES, inputs=box)
    btn.click(run, box, [tagged, out, status])
    box.submit(run, box, [tagged, out, status])

demo.launch(server_name="127.0.0.1", server_port=a.port)
