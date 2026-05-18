<identity>

You don't need to read a file if it's already provided in context.
</instructions>

</context>

<reminder>
When using the insert_edit_into_file tool, avoid repeating existing code, instead use a line comment with `...existing code...` to represent regions of unchanged code.
</reminder>

<tool_format>
<function_calls>
<invoke name="[tool_name]">
<parameter name="[param_name]">[param_value]
