class LitmusTemplates:

    def __init__(self, instruction_width=None):
        if instruction_width:
            self.instruction_width = instruction_width
        else:
            self.instruction_width = 50

    @staticmethod
    def _get_location_declaration(locations):
        location_declarations = "".join([str(i) + "=0;\n" for i in locations])

        return "{\n" + location_declarations + "}"

    @staticmethod
    def _get_thread_declaration(threads):
        result = []

        for ind_comb in threads:
            result.append(f"cta {ind_comb[0]}, gpu {ind_comb[1]}")

        return result

    def _pad_string(self, instruction):
        current_width = len(instruction)

        while current_width < self.instruction_width:
            instruction += " "
            current_width += 1

        return instruction

    def _format_litmus(self, litmus):
        rows = litmus.split("\n")

        for (i, row) in enumerate(rows):
            if "|" in row:
                instructions = row.split("|")
                format_instructions = [self._pad_string(i.strip()) for i in instructions]
                format_row = "|".join(format_instructions)
                rows[i] = f" {format_row};"

        return "\n".join(rows)

    def get_corr(self, threads, instructions):
        # instructions: store + 2 load
        thread_declaration = self._get_thread_declaration(threads)
        litmus = f"""PTX CoRR
"Coherence, Read-Read"
{{
x=0;
P1:%r1=0;
P1:%r2=0;
}}
P0@{thread_declaration[0]}| P1@{thread_declaration[1]}
{instructions[0]} x, 1    | {instructions[1]} %r1, x
                          | {instructions[1]} %r2, x
~exists
(P1:%r1 == 1 /\\ P1:%r2 != 1)
"""
        return self._format_litmus(litmus)
