import os
from re import sub
import subprocess
from shardc.backend.codegen.c import LangC
from shardc.backend.compiler import Compiler
from shardc.backend.generator import CodeGenerator
from shardc.frontend.lexer import ShardLexer
from shardc.frontend.optimizations.content_verifier import ContentVerifier
from shardc.frontend.optimizations.context_checker import ContextChecker
from shardc.frontend.optimizations.symbol_resolver import SymbolResolver
from shardc.frontend.optimizations.type_resolver import TypeResolver
from shardc.frontend.parser import ShardParser
from shardc.frontend.symbols.table import SymbolTable
from shardc.frontend.types.table import TypeTable
from shardc.utils.checkfile import check_file
from spp.preprocessor import ShardPreProcessor

def lex_file(file: str):
    check_file(file)
    lexer = ShardLexer()
    lexer.build()
    with open(file, 'r', encoding="utf-8") as f:
        content = f.read()
    return lexer.lex_code(content)

def parse_file(file: str):
    check_file(file)
    parser = ShardParser()
    parser.build()
    with open(file, 'r', encoding="utf-8") as f:
        content = f.read()
    return parser.parse_code(content)

def preprocess_file(file: str) -> str:
    check_file(file)
    output_filename = f"{file}.sd"
    spp = ShardPreProcessor(file)
    spp.process()
    with open(output_filename, 'w') as f:
        f.write('\n'.join(spp.output))
    return output_filename

def compile_file(file: str, lang: str="c", output: str="output", keep_all: bool=False, main: bool=True, no_std: bool=False) -> str:
    check_file(file)
    preprocessed = preprocess_file(file)
    ast = parse_file(preprocessed)
    if not keep_all:
        os.remove(preprocessed)

    lang_table = {"c": LangC}
    programming_language = lang_table[lang]()

    output_filename = f"{output}{programming_language.file_extension}"

    cv = ContentVerifier()
    cc = ContextChecker()
    tr = TypeResolver(TypeTable())
    sr = SymbolResolver(SymbolTable())
    cg = CodeGenerator(programming_language)
    compiler = Compiler(cg, tr, sr, cc, cv, std=not no_std)

    compiler.add_preamble()
    for node in ast:
        compiler.compile_node(node)

    if main:
        compiler.code.append(
            compiler.code_generator.lang.main_function(
                compiler.code_generator.main_function,
                compiler.code_generator.main_function_params
            )
        )

    with open(output_filename, 'w', encoding="utf-8") as f:
        f.write('\n'.join(compiler.code))

    return output_filename

def compile_file_to_object(file: str, lang: str="c", output: str="output", target: str="clang", exflags: str="", keep_all: bool=False, main: bool=True, no_std: bool=False) -> str:
    check_file(file)
    cfile = compile_file(file, lang, output, keep_all=keep_all, main=main, no_std=no_std)
    base_name = os.path.splitext(cfile)[0]
    output_filename = f"{base_name}.o"

    flags = exflags.split() if isinstance(exflags, str) else exflags
    subprocess.run([target, "-c", cfile, "-o", output_filename, *flags], check=True)

    if not keep_all:
        os.remove(cfile)

    return output_filename

def compile_file_to_executable(file: str, lang: str="c", output: str="output", target: str="clang", exflags: str="", keep_all: bool=False, main: bool=True, no_std: bool=False) -> str:
    check_file(file)
    ofile = compile_file_to_object(file, lang, output, target, exflags, keep_all=keep_all, main=main, no_std=no_std)
    output_filename = os.path.splitext(ofile)[0].replace(".", "")

    flags = exflags.split() if isinstance(exflags, str) else exflags
    subprocess.run([target, ofile, "-o", output_filename, *flags], check=True)

    if not keep_all:
        os.remove(ofile)

    return output_filename