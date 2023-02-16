import instruction_template

CORR_EVENT = [instruction_template.ST, instruction_template.LD, instruction_template.LD]
CORWR_EVENT = [instruction_template.ST, instruction_template.LD, instruction_template.ST, instruction_template.LD]
COWRR_EVENT = [instruction_template.ST, instruction_template.ST, instruction_template.LD, instruction_template.LD]
COWRWR_EVENT = [instruction_template.ST, instruction_template.ST, instruction_template.LD]
NO_THIN_AIR_EVENT = [instruction_template.LD, instruction_template.ST, instruction_template.LD, instruction_template.ST]
SB_EVENT = [instruction_template.ST, instruction_template.FENCE, instruction_template.LD,
            instruction_template.ST, instruction_template.FENCE, instruction_template.LD]
MP_EVENT = [instruction_template.ST, instruction_template.ST, instruction_template.LD, instruction_template.LD]


class LitmusTemplates:

    def __init__(self, instruction_width=None):
        if instruction_width is None:
            self.instruction_width = 50
        else:
            self.instruction_width = instruction_width

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
                          | {instructions[2]} %r2, x
~exists
(P1:%r1 == 1 /\\ P1:%r2 != 1)
"""
        return self._format_litmus(litmus)

    def get_corwr(self, threads, instructions):
        # instructions: store + load + store + load
        thread_declaration = self._get_thread_declaration(threads)
        litmus = f"""PTX CoRWR
"Coherence, Read-Write(-Read)"
{{
x=0;
P1:%r1=0;
P1:%r2=0;
}}
P0@{thread_declaration[0]}| P1@{thread_declaration[1]}
{instructions[0]} x, 1    | {instructions[1]} %r1, x
                          | {instructions[2]} x, 2
                          | {instructions[3]} %r2, x
~exists
(P1:%r1 == 1 /\\ P1:%r2 == 1)
"""
        return self._format_litmus(litmus)

    def get_cowrr(self, threads, instructions):
        # instructions: store + store + load + load
        thread_declaration = self._get_thread_declaration(threads)
        litmus = f"""PTX CoWRR
"Coherence, Write-Read(-Read)"
{{
x=0;
P1:%r1=0;
P1:%r2=0;
}}
P0@{thread_declaration[0]}| P1@{thread_declaration[1]}
{instructions[0]} x, 1    | {instructions[1]} x, 2
                          | {instructions[2]} %r1, x
                          | {instructions[3]} %r2, x
~exists
(P1:%r1 == 1 /\\ P1:%r2 == 2)
"""
        return self._format_litmus(litmus)

    def get_cowrwr(self, threads, instructions):
        # instructions: store + store + load
        thread_declaration = self._get_thread_declaration(threads)
        litmus = f"""PTX CoWRWR
"Coherence, Write(-Read)-Write(-Read)"
{{
x=0;
P0:%r1=0;
}}
P0@{thread_declaration[0]}
{instructions[0]} x, 1
{instructions[1]} x, 2
{instructions[2]} %r1, x                     
~exists
(P0:%r1 == 1)
"""
        return self._format_litmus(litmus)

    def get_no_thin_air(self, threads, instructions):
        # instructions: load + store + load + store
        thread_declaration = self._get_thread_declaration(threads)
        litmus = f"""PTX NoThinAir
"No-Thin-Air"
{{
x=0;
y=0;
P0:%r1=0;
P1:%r2=0;
}}
P0@{thread_declaration[0]}| P1@{thread_declaration[1]}
{instructions[0]} %r1, y  | {instructions[2]} %r2, x
{instructions[1]} x, %r1  | {instructions[3]} y, %r2
~exists
(P0:%r1 == 42 /\\ P1:%r2 == 42)
"""
        return self._format_litmus(litmus)

    def get_sb(self, threads, instructions):
        # instructions: store + fence + load + store + fence + load
        thread_declaration = self._get_thread_declaration(threads)
        litmus = f"""PTX StoreBuffering
"Store Buffering"
{{
x=0;
y=0;
P0:%r1=0;
P1:%r2=0;
}}
P0@{thread_declaration[0]}| P1@{thread_declaration[1]}
{instructions[0]} x, 1    | {instructions[3]} y, 1
{instructions[1]}         | {instructions[4]}
{instructions[2]} %r1, y  | {instructions[5]} %r2, x
~exists
(P0:%r1 == 1 /\\ P1:%r2 == 1)
"""
        return self._format_litmus(litmus)

    def get_mp(self, threads, instructions):
        # instructions: store + store + load + load
        thread_declaration = self._get_thread_declaration(threads)
        litmus = f"""PTX MessagePassing
"Message Passing using acq/rel synchronization should pass"
{{
x=0;
y=0;
P0:%r1=0;
P1:%r2=0;
}}
P0@{thread_declaration[0]}| P1@{thread_declaration[1]}
{instructions[0]} x, 1    | {instructions[2]} %r1, y
{instructions[1]} y, 1    | {instructions[3]} %r2, x
~exists
(P1:%r1 == 1 /\\ P1:%r2 != 1)
"""
        return self._format_litmus(litmus)
