# Key API Surface

Use these as primary touchpoints before introducing custom logic.

## biology-problems/bptools.py

Common parser helpers:
- make_arg_parser(...)
- add_choice_args(parser)
- add_hint_args(parser)
- add_question_format_args(parser, ...)
- add_scenario_args(parser, ...)
- add_anticheat_args(parser)
- apply_anticheat_args(args)

Generation/output helpers:
- make_outfile(*parts)
- collect_and_write_questions(write_question, args, outfile, ...)
- collect_question_batches(write_question_batch, args, ...)

Formatting helpers:
- formatBB_MC_Question(...)
- formatBB_MA_Question(...)
- formatBB_MAT_Question(...)
- formatBB_FIB_Question(...)
- formatBB_FIB_PLUS_Question(...)
- formatBB_NUM_Question(...)
- formatBB_ORD_Question(...)

Utility helpers often reused by generators:
- readYamlFile(...)
- is_valid_html(...)
- applyReplacementRulesToText(...)
- applyReplacementRulesToList(...)

## qti_package_maker

High-value modules for behavior tracing:
- qti_package_maker/assessment_items/item_types.py
- qti_package_maker/assessment_items/validator.py
- qti_package_maker/engines/bbq_text_upload/write_item.py
- qti_package_maker/engines/human_readable/write_item.py

When output format behavior changes unexpectedly, trace from `bptools.formatBB_*` into the target engine writer.
