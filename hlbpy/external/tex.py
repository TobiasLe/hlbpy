# from matplotlib.backends.backend_agg import FigureCanvasAgg
# from matplotlib.figure import Figure
#
#
# def tex_to_svg(tex_string, save_path):
#     fig = Figure(figsize=(5, 4))
#     fig.text(.5, .5, tex_string, fontsize=40, color="white")
#     fig.savefig(save_path, bbox_inches="tight", facecolor=(1, 1, 1, 0))
#     return save_path


"""Interface for writing, compiling, and converting ``.tex`` files.

The following code is modified version of code from the manim package,
which is provided under the following license:

MIT License

Copyright (c) 2018 3Blue1Brown LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import hashlib
import logging
import os
import re
import unicodedata
from pathlib import Path
import copy
import operator as op
from functools import reduce

logger = logging.getLogger("hlbpy")


class TexTemplate:
    """TeX templates are used for creating Tex() and MathTex() objects.

    Parameters
    ----------
    tex_compiler : Optional[:class:`str`], optional
        The TeX compiler to be used, e.g. ``latex``, ``pdflatex`` or ``lualatex``
    output_format : Optional[:class:`str`], optional
        The output format resulting from compilation, e.g. ``.dvi`` or ``.pdf``
    documentclass : Optional[:class:`str`], optional
        The command defining the documentclass, e.g. ``\\documentclass[preview]{standalone}``
    preamble : Optional[:class:`str`], optional
        The document's preamble, i.e. the part between ``\\documentclass`` and ``\\begin{document}``
    placeholder_text : Optional[:class:`str`], optional
        Text in the document that will be replaced by the expression to be rendered
    post_doc_commands : Optional[:class:`str`], optional
        Text (definitions, commands) to be inserted at right after ``\\begin{document}``, e.g. ``\\boldmath``

    Attributes
    ----------
    tex_compiler : :class:`str`
        The TeX compiler to be used, e.g. ``latex``, ``pdflatex`` or ``lualatex``
    output_format : :class:`str`
        The output format resulting from compilation, e.g. ``.dvi`` or ``.pdf``
    documentclass : :class:`str`
        The command defining the documentclass, e.g. ``\\documentclass[preview]{standalone}``
    preamble : :class:`str`
        The document's preamble, i.e. the part between ``\\documentclass`` and ``\\begin{document}``
    placeholder_text : :class:`str`
        Text in the document that will be replaced by the expression to be rendered
    post_doc_commands : :class:`str`
        Text (definitions, commands) to be inserted at right after ``\\begin{document}``, e.g. ``\\boldmath``
    """

    default_documentclass = r"\documentclass[preview]{standalone}"
    default_preamble = r"""
\usepackage[english]{babel}
\usepackage{amsmath}
\usepackage{amssymb}
\renewcommand*\familydefault{\sfdefault}
\usepackage{sfmath}
%\usepackage[no-math]{fontspec}  % somehow does not work with .dvi output
%\setmainfont{Rubik}
%\usepackage{mathastext}
"""
    default_placeholder_text = "YourTextHere"
    default_tex_compiler = "latex"
    default_output_format = ".dvi"
    default_post_doc_commands = ""

    def __init__(
            self,
            tex_compiler=None,
            output_format=None,
            documentclass=None,
            preamble=None,
            placeholder_text=None,
            post_doc_commands=None,
            **kwargs,
    ):
        self.tex_compiler = (
            tex_compiler
            if tex_compiler is not None
            else TexTemplate.default_tex_compiler
        )
        self.output_format = (
            output_format
            if output_format is not None
            else TexTemplate.default_output_format
        )
        self.documentclass = (
            documentclass
            if documentclass is not None
            else TexTemplate.default_documentclass
        )
        self.preamble = (
            preamble if preamble is not None else TexTemplate.default_preamble
        )
        self.placeholder_text = (
            placeholder_text
            if placeholder_text is not None
            else TexTemplate.default_placeholder_text
        )
        self.post_doc_commands = (
            post_doc_commands
            if post_doc_commands is not None
            else TexTemplate.default_post_doc_commands
        )
        self._rebuild()

    def _rebuild(self):
        """Rebuilds the entire TeX template text from ``\\documentclass`` to ``\\end{document}`` according to all settings and choices."""
        self.body = (
                self.documentclass
                + "\n"
                + self.preamble
                + "\n"
                + r"\begin{document}"
                + "\n"
                + self.post_doc_commands
                + "\n"
                + self.placeholder_text
                + "\n"
                + "\n"
                + r"\end{document}"
                + "\n"
        )

    def add_to_preamble(self, txt, prepend=False):
        """Adds stuff to the TeX template's preamble (e.g. definitions, packages). Text can be inserted at the beginning or at the end of the preamble.

        Parameters
        ----------
        txt : :class:`string`
            String containing the text to be added, e.g. ``\\usepackage{hyperref}``
        prepend : Optional[:class:`bool`], optional
            Whether the text should be added at the beginning of the preamble, i.e. right after ``\\documentclass``. Default is to add it at the end of the preamble, i.e. right before ``\\begin{document}``
        """
        if prepend:
            self.preamble = txt + "\n" + self.preamble
        else:
            self.preamble += "\n" + txt
        self._rebuild()

    def add_to_document(self, txt):
        """Adds txt to the TeX template just after \\begin{document}, e.g. ``\\boldmath``

        Parameters
        ----------
        txt : :class:`str`
            String containing the text to be added.
        """
        self.post_doc_commands += "\n" + txt + "\n"
        self._rebuild()

    def get_texcode_for_expression(self, expression):
        """Inserts expression verbatim into TeX template.

        Parameters
        ----------
        expression : :class:`str`
            The string containing the expression to be typeset, e.g. ``$\\sqrt{2}$``

        Returns
        -------
        :class:`str`
            LaTeX code based on current template, containing the given ``expression`` and ready for typesetting
        """
        return self.body.replace(self.placeholder_text, expression)

    def _texcode_for_environment(self, environment):
        """Processes the tex_environment string to return the correct ``\\begin{environment}[extra]{extra}`` and
        ``\\end{environment}`` strings

        Parameters
        ----------
        environment : :class:`str`
            The tex_environment as a string. Acceptable formats include:
            ``{align*}``, ``align*``, ``{tabular}[t]{cccl}``, ``tabular}{cccl``, ``\\begin{tabular}[t]{cccl}``.

        Returns
        -------
        Tuple[:class:`str`, :class:`str`]
            A pair of strings representing the opening and closing of the tex environment, e.g.
            ``\\begin{tabular}{cccl}`` and ``\\end{tabular}``
        """

        # If the environment starts with \begin, remove it
        if environment[0:6] == r"\begin":
            environment = environment[6:]

        # If environment begins with { strip it
        if environment[0] == r"{":
            environment = environment[1:]

        # The \begin command takes everything and closes with a brace
        begin = r"\begin{" + environment
        if (
                begin[-1] != r"}" and begin[-1] != r"]"
        ):  # If it doesn't end on } or ], assume missing }
            begin += r"}"

        # While the \end command terminates at the first closing brace
        split_at_brace = re.split(r"}", environment, 1)
        end = r"\end{" + split_at_brace[0] + r"}"

        return begin, end

    def get_texcode_for_expression_in_env(self, expression, environment):
        r"""Inserts expression into TeX template wrapped in \begin{environment} and \end{environment}

        Parameters
        ----------
        expression : :class:`str`
            The string containing the expression to be typeset, e.g. ``$\\sqrt{2}$``
        environment : :class:`str`
            The string containing the environment in which the expression should be typeset, e.g. ``align*``

        Returns
        -------
        :class:`str`
            LaTeX code based on template, containing the given expression inside its environment, ready for typesetting
        """
        begin, end = self._texcode_for_environment(environment)
        return self.body.replace(self.placeholder_text, f"{begin}\n{expression}\n{end}")

    def copy(self) -> "TexTemplate":
        return copy.deepcopy(self)


default_template = TexTemplate()


def tex_hash(expression):
    id_str = str(expression)
    hasher = hashlib.sha256()
    hasher.update(id_str.encode())
    # Truncating at 16 bytes for cleanliness
    return hasher.hexdigest()[:16]


def tex_to_svg_file(expression, directory, environment="center", tex_template=None):
    """Takes a tex expression and returns the svg version of the compiled tex

    Parameters
    ----------
    expression : :class:`str`
        String containing the TeX expression to be rendered, e.g. ``\\sqrt{2}`` or ``foo``
    directory

    environment : Optional[:class:`str`], optional
        The string containing the environment in which the expression should be typeset, e.g. ``align*``
    tex_template : Optional[:class:`~.TexTemplate`], optional
        Template class used to typesetting. If not set, use default template set via `config["tex_template"]`

    Returns
    -------
    :class:`str`
        Path to generated SVG file.
    """
    if tex_template is None:
        tex_template = default_template
    tex_path = os.path.join(directory, "tex_to_svg.tex")
    generate_tex_file(expression, tex_path, environment, tex_template)
    dvi_file = compile_tex(
        tex_path,
        tex_template.tex_compiler,
        tex_template.output_format,
    )
    return convert_to_svg(dvi_file, tex_template.output_format)


def generate_tex_file(expression, file_path, environment=None, tex_template=None):
    """Takes a tex expression (and an optional tex environment),
    and returns a fully formed tex file ready for compilation.

    Parameters
    ----------
    expression : :class:`str`
        String containing the TeX expression to be rendered, e.g. ``\\sqrt{2}`` or ``foo``
    file_path
        path of the tex file to create
    environment : Optional[:class:`str`], optional
        The string containing the environment in which the expression should be typeset, e.g. ``align*``
    tex_template : Optional[:class:`~.TexTemplate`], optional
        Template class used to typesetting. If not set, use default template set via `config["tex_template"]`

    Returns
    -------
    :class:`str`
        Path to generated TeX file
    """
    if tex_template is None:
        tex_template = default_template
    if environment is not None:
        output = tex_template.get_texcode_for_expression_in_env(expression, environment)
    else:
        output = tex_template.get_texcode_for_expression(expression)

    if not os.path.exists(file_path):
        logger.info('Writing "{}" to {}'.format("".join(expression), file_path))
        with open(file_path, "w", encoding="utf-8") as outfile:
            outfile.write(output)
    else:
        raise ValueError(f"File already exists! {file_path}")
    return file_path


def tex_compilation_command(tex_compiler, output_format, tex_file, tex_dir):
    """Prepares the tex compilation command with all necessary cli flags

    Parameters
    ----------
    tex_compiler : :class:`str`
        String containing the compiler to be used, e.g. ``pdflatex`` or ``lualatex``
    output_format : :class:`str`
        String containing the output format generated by the compiler, e.g. ``.dvi`` or ``.pdf``
    tex_file : :class:`str`
        File name of TeX file to be typeset.
    tex_dir : :class:`str`
        Path to the directory where compiler output will be stored.

    Returns
    -------
    :class:`str`
        Compilation command according to given parameters
    """
    if tex_compiler in {"latex", "pdflatex", "luatex", "lualatex"}:
        commands = [
            tex_compiler,
            "-interaction=batchmode",
            f'-output-format="{output_format[1:]}"',
            "-halt-on-error",
            f'-output-directory="{tex_dir}"',
            f'"{tex_file}"',
            ">",
            os.devnull,
        ]
    elif tex_compiler == "xelatex":
        if output_format == ".xdv":
            outflag = "-no-pdf"
        elif output_format == ".pdf":
            outflag = ""
        else:
            raise ValueError("xelatex output is either pdf or xdv")
        commands = [
            "xelatex",
            outflag,
            "-interaction=batchmode",
            "-halt-on-error",
            f'-output-directory="{tex_dir}"',
            f'"{tex_file}"',
            ">",
            os.devnull,
        ]
    else:
        raise ValueError(f"Tex compiler {tex_compiler} unknown.")
    return " ".join(commands)


def insight_inputenc_error(match):
    code_point = chr(int(match[1], 16))
    name = unicodedata.name(code_point)
    yield f"TexTemplate does not support character '{name}' (U+{match[1]})"
    yield "See the documentation for manim.mobject.svg.tex_mobject for details on using a custom TexTemplate"


def compile_tex(tex_file, tex_compiler, output_format):
    """Compiles a tex_file into a .dvi or a .xdv or a .pdf

    Parameters
    ----------
    tex_file : :class:`str`
        File name of TeX file to be typeset.
    tex_compiler : :class:`str`
        String containing the compiler to be used, e.g. ``pdflatex`` or ``lualatex``
    output_format : :class:`str`
        String containing the output format generated by the compiler, e.g. ``.dvi`` or ``.pdf``

    Returns
    -------
    :class:`str`
        Path to generated output file in desired format (DVI, XDV or PDF).
    """
    result = tex_file.replace(".tex", output_format)
    result = Path(result).as_posix()
    tex_file = Path(tex_file).as_posix()
    tex_dir = os.path.dirname(tex_file)
    if not os.path.exists(result):
        command = tex_compilation_command(
            tex_compiler,
            output_format,
            tex_file,
            tex_dir,
        )
        exit_code = os.system(command)
        if exit_code != 0:
            log_file = tex_file.replace(".tex", ".log")
            print_all_tex_errors(log_file, tex_compiler, tex_file)
            raise ValueError(
                f"{tex_compiler} error converting to"
                f" {output_format[1:]}. See log output above or"
                f" the log file: {log_file}",
            )
    return result


def convert_to_svg(dvi_file, extension, page=1):
    """Converts a .dvi, .xdv, or .pdf file into an svg using dvisvgm.

    Parameters
    ----------
    dvi_file : :class:`str`
        File name of the input file to be converted.
    extension : :class:`str`
        String containing the file extension and thus indicating the file type, e.g. ``.dvi`` or ``.pdf``
    page : Optional[:class:`int`], optional
        Page to be converted if input file is multi-page.

    Returns
    -------
    :class:`str`
        Path to generated SVG file.
    """
    result = dvi_file.replace(extension, ".svg")
    result = Path(result).as_posix()
    dvi_file = Path(dvi_file).as_posix()
    if not os.path.exists(result):
        commands = [
            "dvisvgm",
            "--pdf" if extension == ".pdf" else "",
            "-p " + str(page),
            f'"{dvi_file}"',
            "-n",
            "-v 0",
            "-o " + f'"{result}"',
            ">",
            os.devnull,
        ]
        os.system(" ".join(commands))

    # if the file does not exist now, this means conversion failed
    if not os.path.exists(result):
        raise ValueError(
            f"Your installation does not support converting {extension} files to SVG."
            f" Consider updating dvisvgm to at least version 2.4."
            f" If this does not solve the problem, please refer to our troubleshooting guide at:"
            f" https://docs.manim.community/en/stable/installation/troubleshooting.html",
        )

    return result


def print_all_tex_errors(log_file, tex_compiler, tex_file):
    if not Path(log_file).exists():
        raise RuntimeError(
            f"{tex_compiler} failed but did not produce a log file. "
            "Check your LaTeX installation.",
        )
    with open(log_file) as f:
        tex_compilation_log = f.readlines()
        error_indices = [
            index
            for index, line in enumerate(tex_compilation_log)
            if line.startswith("!")
        ]
        if error_indices:
            with open(tex_file) as g:
                tex = g.readlines()
                for error_index in error_indices:
                    print_tex_error(tex_compilation_log, error_index, tex)


LATEX_ERROR_INSIGHTS = [
    (
        r"inputenc Error: Unicode character (?:.*) \(U\+([0-9a-fA-F]+)\)",
        insight_inputenc_error,
    ),
]


def print_tex_error(tex_compilation_log, error_start_index, tex_source):
    logger.error(
        f"LaTeX compilation error: {tex_compilation_log[error_start_index][2:]}",
    )

    # TeX errors eventually contain a line beginning 'l.xxx` where xxx is the line number that caused the compilation
    # failure. This code finds the next such line after the error current error message
    line_of_tex_error = (
            int(
                [
                    log_line
                    for log_line in tex_compilation_log[error_start_index:]
                    if log_line.startswith("l.")
                ][0]
                    .split(" ")[0]
                    .split(".")[1],
            )
            - 1
    )
    # our tex error may be on a line outside our user input because of post-processing
    if line_of_tex_error >= len(tex_source):
        return None

    # all lines numbers containing '\begin{' or '\end{' - except the Manim added center and document tags
    env_markers_indices = [
                              idx
                              for idx, log_line in enumerate(tex_source)
                              if any(marker in log_line for marker in [r"\begin{", r"\end{"])
                          ][2:-2]

    context = "Context of error:\n\n"
    if line_of_tex_error in env_markers_indices:
        context += "".join(tex_source[line_of_tex_error - 1: line_of_tex_error + 1])
    else:
        marker_before_error = max(
            idx for idx in env_markers_indices if idx < line_of_tex_error
        )
        marker_after_error = min(
            idx for idx in env_markers_indices if idx > line_of_tex_error
        )
        context += "".join(tex_source[marker_before_error:marker_after_error])
    logger.error(context)

    for prog, get_insight in LATEX_ERROR_INSIGHTS:
        error_end_index = [
            idx
            for idx, _ in enumerate(tex_compilation_log[error_start_index:])
            if _.startswith("l.")
        ][0]
        match = re.search(
            prog,
            "".join(tex_compilation_log[error_start_index:error_end_index]),
        )
        if match is not None:
            for insight in get_insight(match):
                logger.info(insight)


def get_modified_expression(tex_string):
    result = tex_string
    result = result.strip()
    result = modify_special_strings(result)
    return result


def modify_special_strings(tex):
    tex = tex.strip()
    should_add_filler = reduce(
        op.or_,
        [
            # Fraction line needs something to be over
            tex == "\\over",
            tex == "\\overline",
            # Make sure sqrt has overbar
            tex == "\\sqrt",
            tex == "\\sqrt{",
            # Need to add blank subscript or superscript
            tex.endswith("_"),
            tex.endswith("^"),
            tex.endswith("dot"),
        ],
    )

    if should_add_filler:
        filler = "{\\quad}"
        tex += filler

    if tex == "\\substack":
        tex = "\\quad"

    if tex == "":
        tex = "\\quad"

    # To keep files from starting with a line break
    if tex.startswith("\\\\"):
        tex = tex.replace("\\\\", "\\quad\\\\")

    # Handle imbalanced \left and \right
    num_lefts, num_rights = (
        len([s for s in tex.split(substr)[1:] if s and s[0] in "(){}[]|.\\"])
        for substr in ("\\left", "\\right")
    )
    if num_lefts != num_rights:
        tex = tex.replace("\\left", "\\big")
        tex = tex.replace("\\right", "\\big")

    tex = remove_stray_braces(tex)

    for context in ["array"]:
        begin_in = ("\\begin{%s}" % context) in tex
        end_in = ("\\end{%s}" % context) in tex
        if begin_in ^ end_in:
            # Just turn this into a blank string,
            # which means caller should leave a
            # stray \\begin{...} with other symbols
            tex = ""
    return tex


def remove_stray_braces(tex):
    r"""
    Makes :class:`~.MathTex` resilient to unmatched braces.

    This is important when the braces in the TeX code are spread over
    multiple arguments as in, e.g., ``MathTex(r"e^{i", r"\tau} = 1")``.
    """

    # "\{" does not count (it's a brace literal), but "\\{" counts (it's a new line and then brace)
    num_lefts = tex.count("{") - tex.count("\\{") + tex.count("\\\\{")
    num_rights = tex.count("}") - tex.count("\\}") + tex.count("\\\\}")
    while num_rights > num_lefts:
        tex = "{" + tex
        num_lefts += 1
    while num_lefts > num_rights:
        tex = tex + "}"
        num_rights += 1
    return tex
