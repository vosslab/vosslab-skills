# Distillation lens

These rules shape what the goal emphasizes or omits. They normally stay invisible in the
output; a rule reaches the goal text only when naming it materially prevents likely drift.

- Distill the durable outcome, not the implementation sequence.
- Preserve implementation freedom.
- Use positive prompting and omission.
- Prefer the smallest coherent design that satisfies the plan.
- Favor robustness and adaptability where the plan requires them.
- Treat tests as durable design constraints, not automatic completion criteria.
- Keep validation proportional to actual risk and product needs.
- Reference repository guidance when a principle materially helps prevent drift.
- Include repository or environment context when it materially prevents likely drift in this
  task (for example "pre-production: prefer direct design correction over compatibility
  layers"). Omit context that repeats standing operational detail without changing the
  intended outcome or an important implementation judgment.
