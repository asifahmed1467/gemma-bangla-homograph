---
title: Bangla Homograph Fixer
emoji: 📝
sdk: gradio
sdk_version: 6.30.0
app_file: app.py
pinned: false
---

# Bangla homograph fixer

Gemma 3 270M with a LoRA adapter. If the sentence has one of the 8 trained words
(আসর, আসরে, আসরের, আসল, কর, করাত, কেন, কেবলা), `<hg>` is put in front of it and the fine-tuned
model rewrites it with the right pronunciation spelling. Otherwise the adapter is switched off and plain Gemma answers.

Put your trained adapter folder here as `gemma_cpu_lora/` (adapter_config.json, adapter_model.safetensors,
base_model.txt, tokenizer files).
